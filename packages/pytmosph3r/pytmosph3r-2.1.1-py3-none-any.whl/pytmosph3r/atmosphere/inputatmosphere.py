import numpy as np
from .atmosphere import Atmosphere
from pytmosph3r.config.factory import create_obj

class InputAtmosphere(Atmosphere):
    """
    Atmospheric model with a (level+layer, latitude, longitude) coordinate system.

    Args:
        grid (:class:`~pytmosph3r.grid.Grid3D`): Grid representing the coordinate system (level+layer, latitude, longitude).
        pressure (float, :obj:`array`, optional): Pressure for each point in :py:attr:`grid`. Incompatible with :py:attr:`max_pressure`.
        max_pressure (float) : Maximum pressure (at the surface). Incompatible with :py:attr:`pressure`.
        min_pressure (float) : Minimum pressure to use in the highest column of the model.
        temperature (float, :obj:`array`, dict): Temperature for each point in :py:attr:`grid`. If it is an array or a float, it will simply define the temperature over the whole grid. If used as a dictionary, it can configure :class:`~pytmosph3r.atmosphere.simple2d.Simple2DTemperature`.
        gas_mix_ratio (float, :obj:`array`): Volume Mixing Ratio of gases (dictionary :code:`{'H2O': array, ...}`.
        transparent_gases (list, optional): Gases considered transparent (not taken into account for the contributions).
        aerosols (float, :obj:`array`): Aerosols: number density of particles (in number per unit volume).
        chemistry (:class:`pytmosph3r.chemistry`): Chemistry module. Either a class of :class:`pytmosph3r.chemistry` or your personal module (which should probably inherit from :class:`pytmosph3r.Chemistry`, or at least change the gas mix ratio of the atmosphere).

    Attributes:
        grid (:class:`~pytmosph3r.grid.Grid3D`): Grid representing the coordinate system (level+layer, latitude, longitude).
        pressure (float, :obj:`array`, optional): Pressure for each point in :py:attr:`grid`. Incompatible with :py:attr:`max_pressure`.
        max_pressure (float) : Maximum pressure (at the surface). Incompatible with :py:attr:`pressure`.
        min_pressure (float) : Minimum pressure to use in the highest column of the model.
        temperature (float, :obj:`array`, dict): Temperature for each point in :py:attr:`grid`. If it is an array or a float, it will simply define the temperature over the whole grid. If used as a dictionary, it can configure :class:`~pytmosph3r.atmosphere.simple2d.Simple2DTemperature`.
        gas_mix_ratio (float, :obj:`array`): Volume Mixing Ratio of gases (dictionary :code:`{'H2O': array, ...}`.
        transparent_gases (list, optional): Gases considered transparent (not taken into account for the contributions).
        aerosols (float, :obj:`array`): Dictionary of aerosols. Each aerosol is itself a dictionary of which the keys are the following: 'mmr' for mass mixing ratios (in :math:`kg/kg`), 'reff' for effective radii (in :math:`meters`), `p_min` for the pressure limit (in :math:`Pa`) under which all MMRs are set to 0, and 'condensate_density' for the density of the constituent of the condensed particles (in :math:`kg/m^3`). Example of a dense layer of aerosols for pressure higher than 1000 Pa: :code:`{'H2O': {'mmr':1e-1, 'reff': 1e-5, 'p_min':1000, 'condensate_density':940}}`.
        chemistry (:class:`pytmosph3r.chemistry`): Either a class of :class:`pytmosph3r.chemistry` or your personal module (which should probably inherit from :class:`pytmosph3r.Chemistry`, or at least change the gas mix ratio of the atmosphere).
    """
    def __init__(self,
                 grid=None,
                 pressure=None,
                 max_pressure=None,
                 min_pressure=None,
                 temperature=None,
                 gas_mix_ratio={},
                 transparent_gases = None,
                 aerosols={},
                 chemistry=None,
                 ):
        super().__init__(self.__class__.__name__)
        self.grid = grid
        self.pressure = pressure
        self.max_pressure = max_pressure
        self.min_pressure = min_pressure
        self.temperature = temperature
        self.gas_mix_ratio = gas_mix_ratio
        self.transparent_gases = transparent_gases
        self.aerosols = aerosols
        self.altitude = None ## Altitude for each point in :py:attr:`grid`.
        if chemistry is None or (isinstance(chemistry, dict) and not len(chemistry)):
            self.chemistry = None
        elif isinstance(chemistry, dict):
            self.chemistry = create_obj({"Chemistry":chemistry}, "Chemistry")
        else:
            self.chemistry = chemistry

    def inputs(self):
        return ["grid", "pressure", "max_pressure", "min_pressure", "temperature", "gas_mix_ratio", "transparent_gases", "aerosols", "chemistry"]
    def outputs(self):
        return ["altitude"]
