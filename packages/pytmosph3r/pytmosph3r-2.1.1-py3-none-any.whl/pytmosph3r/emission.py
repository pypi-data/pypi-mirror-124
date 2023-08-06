import numba
import numpy as np
from math import ceil
from tqdm.auto import tqdm
import exo_k as xk
from pytmosph3r.log import Logger
from pytmosph3r.aerosols import PrepareAerosols

@numba.njit(cache=True)
def surface_projection(local_latitudes, n_per_latitudes, local_longitudes, n_per_longitudes, n_total_longitudes, obs_latitude, obs_longitude, planet_radius, local_projection):
    """Compute surface projection of :attr:`local_latitudes` and :attr:`local_longitudes` on the plane of the sky (as seen from the observer). :attr:`local_projection` is the output of the function."""
    for i in range(n_per_latitudes):
        lat_bounds = np.array([local_latitudes[i], local_latitudes[i+1]])
        latitude = np.mean(lat_bounds)
        surface = (2*np.pi*planet_radius**2
            * (np.sin(lat_bounds[1])-np.sin(lat_bounds[0])) / n_total_longitudes)

        for j in range(n_per_longitudes):
            long_bounds = np.array([local_longitudes[j], local_longitudes[j+1]])
            longitude = np.mean(long_bounds)

            # phi = central angle between (lat, lon) and observer (@ infinite distance)
            cos_phi = (np.sin(latitude)*np.sin(obs_latitude)
                    + np.cos(obs_latitude) * np.cos(latitude)
                    * np.cos(longitude - obs_longitude))
            local_projection[i,j] = cos_phi * surface

class Emission(Logger):
    """The emission module computes the flux emitted by a body by iterating over the latitudes and longitudes of the model. It relies on `Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html?highlight=emission#exo_k.atm.Atm.emission_spectrum_2stream>`_ for the computation of the 1D flux in each column.
    The flux is then scaled with respected to the surface of the atmosphere projected onto the plane of the sky.
    A phase curve mode can be activated, in which case, we iterate over :attr:`n_phases` longitudes for the observer and scale the flux using the projection of the surface onto that direction.

    Args:
        planet_to_star_flux_ratio (bool): The output spectrum will be a ratio between the flux of the planet and that of the star (instead of the flux of the planet).
        phase_curve (bool) : Activates the computation of the phase curve.
        n_phases (int) : Number of phases for the pĥase curve. Defaults to 100.
        surface_resolution (int) : Number of grid points to calculate projected surface (the more points, the more accurate). Defaults to 500.
        store_raw_flux (bool) : Whether or not to store raw flux (over each (latitude, longitude)).
        kwargs (dict): See `documentation of Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html?highlight=emission#exo_k.atm.Atm.emission_spectrum_2stream>`_ to see what other options are available.

    Returns:
        (Spectrum): If :attr:`planet_to_star_flux_ratio` is True, the planet to star flux ratio (:math:`F_P/F_S * (R_P/R_S)^2`), else the planet flux (in :math:`W/m^2/cm^{-1}`).
    """
    def __init__(self, planet_to_star_flux_ratio=None, phase_curve=None, n_phases=None, surface_resolution=None, store_raw_flux=None, **kwargs):
        super().__init__(self.__class__.__name__)
        self.planet_to_star_flux_ratio = planet_to_star_flux_ratio
        """Returns the planet to star flux ratio instead of the planet flux."""
        self.phase_curve_mode = phase_curve
        """Activates the computation of the phase curve."""
        self.n_phases = n_phases
        """Number of phases in the phase curve."""
        self.flux = None
        """Output spectrum (Exo_k object)."""
        self.surface_resolution = surface_resolution
        """Number of grid points to calculate projected surface."""
        self.store_raw_flux = store_raw_flux
        """Whether or not to store raw flux (over each (latitude, longitude))."""
        self.kwargs = kwargs
        self.model = None

    def build(self, model):
        """No need for an altitude-based grid (as done in transmission), so we just copy the input grid.
        """
        self.model = model
        self.model.atmosphere = model.input_atmosphere # simple copy
        self.observer = model.observer
        if self.surface_resolution is None:
            self.surface_resolution = 500

        if self.n_phases is not None:
            self.info("Phase curve mode activated.")
            self.phase_curve_mode = True

        if self.phase_curve_mode:
            if self.store_raw_flux is None:
                self.store_raw_flux = True
            if self.n_phases is None:
                self.n_phases = 100
                self.warning("Number of phases set to 100.")
            self.n_phases = int(self.n_phases)

    def compute_projection(self):
        """Compute the projection surface of the grid cells over the plane of the sky."""
        obs = self.model.observer
        self.projected_surface = np.zeros(self.model.shape[1:])
        latitudes = self.model.grid.latitudes
        longitudes = self.model.grid.all_longitudes

        n_per_longitudes = int(ceil(self.surface_resolution/self.model.grid.n_longitudes))
        n_total_longitudes = n_per_longitudes * self.model.grid.n_longitudes
        n_per_latitudes = int(ceil(self.surface_resolution/self.model.grid.n_latitudes))
        n_total_latitudes = n_per_latitudes * max(self.model.grid.n_latitudes-2, 1)

        # discretize surface among n_total_{latitudes, longitudes} (for better accuracy)
        surface_longitudes = np.linspace(longitudes[0], longitudes[-1], n_total_longitudes+1)
        surface_latitudes = np.linspace(latitudes[1],latitudes[-2],n_total_latitudes+1) # except poles, since they're halved
        for lat, lon in self.model.grid.walk([1,2]):
            # Create local subdivisions of latitude and longitude to compute surface projection with a better accuracy.
            if lat == 0 or lat == self.model.n_latitudes-1:
                # exception for the poles, because they're halved
                local_latitudes = np.linspace(latitudes[lat],latitudes[lat+1],n_per_latitudes+1)
            else:
                local_latitudes = surface_latitudes[(lat-1) * n_per_latitudes:(lat) * n_per_latitudes+1]
                assert np.isclose(local_latitudes[-1], latitudes[lat+1]), "Local latitude (%s) is not correct (%s). Report this as a bug." % (local_latitudes[-1], latitudes[lat+1])
                assert np.isclose(local_latitudes[0], latitudes[lat]), "Local latitude is not correct. Report this as a bug."
            local_longitudes = surface_longitudes[lon * n_per_longitudes:(lon+1) * n_per_longitudes+1]
            local_projection = np.zeros((n_per_latitudes, n_per_longitudes))

            surface_projection(local_latitudes, n_per_latitudes, local_longitudes, n_per_longitudes, n_total_longitudes, obs.latitude, obs.longitude, self.model.planet.radius, local_projection)

            # local_projection is a 2D array of projected surfaces of the local subdivisions, we sum it to get the projected surface of the current cell
            self.projected_surface[lat, lon] = np.sum(local_projection[np.where(local_projection>0)])

    def compute(self, model):
        """Iterate over vertical columns (lat/lon) of the model, in which we use the exo_k 1D two-stream emission function (emission_spectrum_2stream() for the `Atm` class). Then integrate the output flux in the direction of the observer.
        For that, we compute the solid angle associated to the position of the observer, projecting the visible surface of the atmosphere onto the plane of the sky.
        The flux is scaled with respect to that projected surface.
        If :attr:`planet_to_star_flux_ratio` is True, the flux is scaled to the flux of the star (a blackbody).
        If the phase curve mode is activated, this function also computes a :attr:`phase_curve` object with the spectrum associated to all :attr:`n_phases` phase/observer longitudes (see :func:`compute_phase_curve`).

        Args:
            model (:class:`~pytmosph3r.model.model.Model`): Model in which to read latitudes, longitudes, pressure, etc.

        Returns:
            Spectrum (exo_k object): Spectrum (either planet flux or planet-to-star flux ratio, following if :attr:`planet_to_star_flux_ratio` is activated).
        """
        if model.parallel:
            model = model.parallel.synchronize(model) # get model from P0
        self.model = model
        opacity = self.model.opacity
        self.compute_projection()

        self.flux = xk.Spectrum(0, model.opacity.k_data.wns, model.opacity.k_data.wnedges)

        self.info("Computing output flux...")

        if self.store_raw_flux:
            self.raw_flux = np.zeros((self.model.n_latitudes, self.model.n_longitudes, model.opacity.k_data.Nw))

        longitudes = self.model.grid.mid_longitudes
        if self.model.n_latitudes < 2 and self.model.n_longitudes > 1:
            longitudes = tqdm(self.model.grid.mid_longitudes, leave=False)
        for lat, latitude in enumerate(tqdm(self.model.grid.mid_latitudes, leave=False, )):
            for lon, longitude in enumerate(longitudes):
                if not self.store_raw_flux and self.projected_surface[lat, lon] <= 0:
                    continue # skip this cell: not visible by observer
                # The data should go from the top to the bottom in Exo_k (+ pressure in log10)
                layers = slice(None, None,-1)
                coordinates = (layers, lat, lon)

                logplay = np.log10(self.model.pressure[coordinates])
                tlay = self.model.temperature[coordinates]
                gas_vmr = {}
                for gas, vmr in self.model.gas_mix_ratio.items():
                    if isinstance(vmr, (str, int, float)):
                        gas_vmr[gas] = vmr
                    else:
                        gas_vmr[gas] = vmr[coordinates]

                prepare_aerosols = PrepareAerosols(self.model, self.model.n_layers)
                aer_reff_densities = prepare_aerosols.compute(slice(None, None), coordinates)

                # Effectively compute the flux via the 2stream function from exo_k
                atm = xk.Atm(logplay=logplay,tlay=tlay,grav=self.model.planet.surface_gravity,
                            composition=gas_vmr, aerosols=aer_reff_densities,
                            k_database=opacity.k_data, cia_database=opacity.cia_data, a_database=opacity.aerosol_data)
                flux = atm.emission_spectrum_2stream(rayleigh=opacity.rayleigh, log_interp=False, **self.kwargs)
                if self.store_raw_flux:
                    self.raw_flux[lat, lon] = flux.value # * self.model.surface[lat, lon] / (np.pi*self.model.planet.radius ** 2)
                flux *= self.projected_surface[lat, lon]
                self.flux += flux

        factor = np.pi*self.model.planet.radius ** 2
        if self.planet_to_star_flux_ratio:
            # Normalize with star flux
            star_flux = opacity.k_data.blackbody(self.model.star.temperature)
            factor = star_flux * factor * (self.model.star.radius/self.model.planet.radius)**2

        if self.phase_curve_mode:
            self.compute_phase_curve()
            try:
                self.phase_curve /= factor.value
            except:
                self.phase_curve /= factor # float case

        self.info("DONE")

        return self.flux / factor

    def compute_phase_curve(self):
        """Computation of a phase curve, along :attr:`n_phases` observer longitudes. This function is called by :func:`compute`."""
        self.info("Computing phase curve with %s points..."%(self.n_phases))

        self.observer_longitudes = np.linspace(0, 2*np.pi, self.n_phases)
        self.phase_curve = np.zeros((self.n_phases,self.model.opacity.k_data.Nw))
        initial_longitude = self.model.observer.longitude # save longitude since we're going to overwrite it during the phase curve

        for i, observer_longitude in enumerate(tqdm(self.observer_longitudes)):
            self.model.observer.longitude = observer_longitude
            self.compute_projection()
            self.phase_curve[i] = np.sum(self.raw_flux * self.projected_surface[..., None], axis=(0,1))

        self.model.observer.longitude = initial_longitude # resurrect initial setup

    def inputs(self):
        return ["integral", "planet_to_star_flux_ratio", "surface_projection", "store_raw_flux"]
    def outputs(self):
        outputs = ["raw_flux" , "projected_surface"]
        if self.phase_curve_mode:
            outputs += ["n_phases", "phase_curve", "observer_longitudes"]
        return outputs
