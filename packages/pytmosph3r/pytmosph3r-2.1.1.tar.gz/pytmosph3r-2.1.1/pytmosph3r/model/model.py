import numpy as np
import exo_k as xk
from copy import copy
from pytmosph3r.constants import *
from pytmosph3r.log import Logger
from pytmosph3r.rays import Observer
from pytmosph3r.opacity import Opacity
from pytmosph3r.transmission import Transmission
from pytmosph3r.util.util import get_attributes, mol_key, update_dict, prop
from pytmosph3r.parallel import *

class Model(Logger):
    """Main model structure which plays the role of the puppeteer.

    All 'prop' attributes are derived from :class:`~pytmosph3r.AltitudeAtmosphere`.

    Args:
        n_vertical (int) : Number of vertical layers for the altitude-based  :py:attr:`atmosphere` (100 by default).
        noise (float, array) : If a float, it gives the width of the errorbar (the output spectrum will be noised with a normal distribution scaled with this value). if an array, the noise is simply added to the spectrum. 0 by default.
        interp : Interpolation of the pressure in the transformation of the input atmosphere into the altitude-based :py:attr:`atmosphere`. It may be either one the parameters to pass to scipy.interpolate.interp1d function (see 'kind' parameters) or False (default option). If it is set to false, the pressure will be recomputed using :class:`~pytmosph3r.atmosphere.AltitudeAtmosphere.compute_pressure`.
        gas_dict : Dictionary containing the names of the gas and the keys to find them in the input file (diagfi, hdf5). Defaults to {'H2O': 'h2o_vap'}.
        aerosols_dict : Similar to :py:attr:`gas_dict`, it's a dictionary containing the names of the aerosols (and their characteristics) and the keys to find them in the input file (diagfi, hdf5). If only the name of the molecule is given, the key is assumed to represent the MMR (mass molecular ratio in kg/kg). Example : {'H2O': 'h2o_ice', 'H2O_reff': 'H2Oice_reff'}.
        planet (:class:`~pytmosph3r.planet.Planet`) : Planet object.
        star (:class:`~pytmosph3r.star.Star`) : Star object (not optional).
        input_atmosphere (:class:`~pytmosph3r.atmosphere.inputatmosphere.InputAtmosphere`) : Input atmospheric grid based on levels (and inter-layers).
        observer (:class:`~pytmosph3r.rays.Observer`) : Position of the observer (latitude, longitude).
        opacity (:class:`~pytmosph3r.opacity.Opacity`) : Opacity parameters.
        radiative_transfer (:class:`~pytmosph3r.transmission.Transmission` or :class:`~pytmosph3r.emission.Emission`) : Radiative transfer parameters (see associated classes).
    """
    def __init__(self, name=None,
                 n_vertical=None,
                 noise=None,
                 interp=None,
                 gas_dict=None,
                 aerosols_dict=None,
                 planet=None,
                 star=None,
                 input_atmosphere=None,
                 observer=None,
                 opacity=None,
                 radiative_transfer=None,
                 parallel=None,
                 ):
        name = name or self.__class__.__name__
        super().__init__(name)
        self.filename = None
        self.planet = planet
        self.star = star
        self.noise = noise
        self.input_atmosphere = input_atmosphere
        self.observer = observer
        if isinstance(observer, dict):
            self.observer = Observer(**observer)
        elif not isinstance(observer, Observer):
                self.error("Observer object is not from pytmosph3r. Proceed with care...")
        self.opacity = opacity
        self._surface = None
        """Only used in Emission."""
        self.radiative_transfer = radiative_transfer
        """Choose among Transmission or Emission."""
        self.spectrum = None
        """Noiseless spectrum."""
        self.noised_spectrum = None
        self.atmosphere = None
        """Atmosphere based on an altitude grid (:class:`~pytmosph3r.atmosphere.AltitudeAtmosphere`), computed through :class:`altitude_grid()`"""

        self.n_vertical = n_vertical
        self.interp = interp
        self.gas_dict = gas_dict
        self.aerosols_dict = aerosols_dict

        self.parallel = parallel
        if self.parallel is None and mpi.nprocs() > 1:
            self.parallel = MpiTransit()

    @prop
    def default_values(self):
        return {
            'n_vertical': 100,
            'noise': 0,
            'interp': 'log',
            'gas_dict': {},
            'aerosols_dict': {},
            'observer': Observer(),
            'opacity': Opacity(),
            'radiative_transfer': Transmission(),
        }

    def inputs(self):
        return ["n_vertical", "noise", "interp", "gas_dict", "aerosols_dict", "planet", "star", "input_atmosphere", "observer", "opacity", "radiative_transfer", "parallel"]

    def outputs(self):
        outputs = ["input_atmosphere", "atmosphere", "radiative_transfer", "spectrum_value", "wns", "wnedges", "spectrum_noised"]
        return outputs

    @prop
    def grid(self):
        try:
            return self.atmosphere.grid
        except:
            return self.input_atmosphere.grid
    @prop
    def shape(self):
        return (self.n_layers, self.n_latitudes, self.n_longitudes)
    @prop
    def n_latitudes(self):
        return self.grid.n_latitudes
    @prop
    def n_longitudes(self):
        return self.grid.n_longitudes
    @prop
    def n_layers(self):
        return self.grid.n_vertical
    @prop
    def n_levels(self):
        return self.atmosphere.n_levels
    @prop
    def altitude(self):
        return self.atmosphere.altitude
    @prop
    def pressure(self):
        return self.atmosphere.pressure
    @prop
    def temperature(self):
        return self.atmosphere.temperature
    @prop
    def molar_mass(self):
        return self.atmosphere.molar_mass
    @prop
    def gas_mix_ratio(self):
        return self.atmosphere.gas_mix_ratio
    @prop
    def aerosols(self):
        return self.atmosphere.aerosols
    def Rp(self):
        return self.planet.radius
    @prop
    def Rs(self):
        return self.star.radius
    @prop
    def surface(self):
        """Surface area at each latitude x longitude."""
        if not hasattr(self,"_surface") or self._surface is None:
            # if self.atmosphere is None:
            #     raise AttributeError("The model needs an atmosphere to compute a surface. Set the 'atmosphere' attribute by using build().")
            self._surface = np.zeros((self.n_latitudes, self.n_longitudes))
            self._surface[:] = np.abs((2*np.pi*self.planet.radius**2
            * (np.sin(self.grid.latitudes[1:])-np.sin(self.grid.latitudes[:-1])) / self.grid.n_longitudes))[:, None]
            assert np.isclose(np.sum(self._surface), 4*np.pi*self.planet.radius**2), "Total surface is not equal to the sum of the surfaces of each grid point (%g != %g)... Report this as a bug."%(np.sum(self._surface), 4*np.pi*self.planet.radius**2)
        return self._surface
    @surface.setter
    def surface(self, value):
        self._surface = value

    def gas(self, gas):
        """Return the key corresponding to :attr:`gas` using user dictionary :attr:`gas_dict`."""
        return mol_key(self.gas_dict, gas, "vap")

    def aerosol(self, aerosol):
        """Return the key corresponding to :attr:`aerosol` using user dictionary :attr:`aerosols_dict`."""
        return mol_key(self.aerosols_dict, aerosol, "ice")

    def read_data(self):
        if self.filename:
            self.warning("%s does not read any data file. %s is ignored."%(self.__class__.__name__, self.filename))

    def merge_data_config(self, variables):
        """This method allows subclasses to merge config file data to the data read from data file (HDF5, diagfi, ...)
        """
        self.info("Loading model attributes from config file...")
        for key, value in variables.items():
            self.merge_config_into(key, value)

    def merge_config_into(self, data_name, config):
        """Override elements read from data file by config file

        Args:
            data_name (string): name of attribute to override
            config (object): object read from config file
        """
        if data_name not in self.__dict__:
            self.error("%s is not initialized in model. Maybe set it to None before calling this method."%data_name)

        if isinstance(config, (int, float, str, list, np.ndarray, tuple)):
            self.__dict__[data_name] = config
            return

        data = self.__dict__[data_name]
        if config is None:
            # if data is None:
            #     self.error("%s needs to be defined at least in data or config file"%data_name)
            return
        if data is None: # no data: take config value
            self.__dict__[data_name] = config
        else:
            for attr, val in get_attributes(config):
                if val is not None:
                    if isinstance(val, dict) and attr in data.__dict__.keys() and isinstance(data.__dict__[attr], dict):
                        try:
                            update_dict(data.__dict__[attr], val)
                        except:
                            self.error("Couldn't override original %s - not same shape."%attr)
                    else:
                        data.__dict__[attr] = val
                    if isinstance(val, (float, int)):
                        self.warning("%s: Config file overrides %s = %s"%(data_name, attr, val))
                    elif hasattr(val, "__len__"):
                        self.warning("%s: Config file overrides %s (length = %s)"%(data_name, attr, len(val)))
                    else:
                        self.warning("%s: Config file overrides %s"%(data_name, attr))

    def default_value(self, data_name, value):
        if self.__dict__[data_name] is None:
            self.warning("Using default %s (%s)."% (data_name, value))
            self.__dict__[data_name] = value

    def build(self):
        """Initialize the model once all the parameters have been set. Set default values if needed.
        """
        if 't' not in self.__dict__:
            self.t = 0

        if self.filename is not None and self.input_atmosphere is not None:
            if self.input_atmosphere.grid:
                self.warning("Ignoring Grid from .cfg file since we have an input file.")
                self.input_atmosphere.grid = None
            if self.input_atmosphere.max_pressure:
                self.warning("Ignoring max_pressure from .cfg file since we have an input file.")
                self.input_atmosphere.max_pressure = None


        # Save variables to possibly overwrite configuration file
        self.variables = {
            'filename': copy(self.filename),
            'n_vertical': copy(self.n_vertical),
            'interp': copy(self.interp),
            'gas_dict': copy(self.gas_dict),
            'aerosols_dict': copy(self.aerosols_dict),
            'planet': copy(self.planet),
            'star': copy(self.star),
            'input_atmosphere': copy(self.input_atmosphere),
            'observer': copy(self.observer),
            'opacity': copy(self.opacity),
            'radiative_transfer': copy(self.radiative_transfer),
        }
        if self.gas_dict is None:
            self.gas_dict = {}
        self.read_data()
        self.merge_data_config(self.variables)

        for parameter in self.default_values.items():
            self.default_value(*parameter)
        self.n_vertical = int(self.n_vertical)
        del self.variables # don't keep duplicates

        if self.input_atmosphere.grid is None:
            raise NameError("Grid is not defined. Please set one in your input.")

        if self.input_atmosphere.grid.n_vertical is None:
            self.warning("Setting input grid n_vertical to %s (nb of levels)"%(self.n_vertical+1))
            self.input_atmosphere.grid.n_vertical = self.n_vertical+1

        assert self.planet, "Planet not defined!"
        assert self.star, "Star not defined!"
        assert self.input_atmosphere, "Input atmosphere not defined!"

        self.input_atmosphere.build(self)
        self.radiative_transfer.build(self) # creates 'atmosphere' attribute

    def run(self):
        """Run Pytmosph3R, i.e., compute the spectrum of a built model
        (the function :py:attr:`build` (or an equivalent) should have been called).
        """
        self.info("Running model...")
        if self.atmosphere is None:
            self.error("Altitude Grid not computed. Call build() first.")

        self.opacity.load_gas_database(self) # includes clip spectral range
        self.spectrum = self.radiative_transfer.compute(self)

        if self.noise is not None and self.noise is not False:
            noise = self.noise
            if isinstance(noise, (float, int)):
                # create a normal distribution around the spectrum values
                noise = np.random.normal(0, self.noise, self.opacity.k_data.Nw)
                noise_spectrum = xk.Spectrum(noise, wns=self.wns, wnedges=self.wnedges)
            self.noised_spectrum = self.spectrum + noise_spectrum

    @prop
    def wns(self):
        return self.spectrum.wns
    @prop
    def wnedges(self):
        return self.spectrum.wnedges
    @prop
    def spectrum_value(self):
        return self.spectrum.value
    @prop
    def spectrum_noised(self):
        try:
            return self.noised_spectrum.value
        except:
            return None
