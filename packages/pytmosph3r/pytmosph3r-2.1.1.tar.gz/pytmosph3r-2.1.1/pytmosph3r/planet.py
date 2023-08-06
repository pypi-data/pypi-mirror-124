from pytmosph3r.log import Logger
from pytmosph3r.constants import G, RJUP, MJUP
from pytmosph3r.util.util import prop
import astropy.units as u

class Planet(Logger):
    """ Planet properties.

        Args:
            surface_gravity (float): Surface gravity of the planet.
            radius (float): Radius of the planet (by default in meters, see :py:attr:`r_units` for changing the units).
            r_units (str, optional): Length unit for the radius ('m' for meters, 'Rjup' for Jupiter radius, i.e., 71492000 m, ...). See https://docs.astropy.org/en/stable/units/index.html#module-astropy.units for more units.
    """

    def __init__(self, surface_gravity=None, radius=None, r_units='m'):
        Logger.__init__(self, 'Planet')
        if surface_gravity is None:
            self.error("No surface gravity. Set it in the config file.")
        if radius is None:
            self.error("No planet radius. Set it in the config file.")
        self.surface_gravity = surface_gravity
        """ Surface gravity (:math:`m\cdot s^{-2}`)."""
        try:
            to_meters = u.Unit(r_units).to(u.m)
        except:
            to_meters = u.Unit(r_units, format="cds").to(u.m)
        self.radius = radius
        """ Planet radius (in `m`)."""
        if radius:
            self.radius = radius * to_meters
        self.r_units = 'm'

    @prop
    def mass(self):
        """Planet mass (:math:`kg`)."""
        return self.surface_gravity*(self.radius**2)/G

    @prop
    def mass_jup(self):
        """ Planet mass (in `Jupiter mass`)."""
        return self.mass/MJUP

    @prop
    def radius_jup(self):
        """ Planet radius (in `Jupiter radii`)."""
        return self.radius/RJUP

    def gravity(self, height):
        r"""Gravity (:math:`m\cdot s^{-2}`) at height (:math:`m`) from planet."""
        try:
            return self.surface_gravity * ((self.radius)**2) / ((self.radius+height)**2)
        except:
            return None

    def inputs(self):
        return ['surface_gravity', 'radius', 'r_units']