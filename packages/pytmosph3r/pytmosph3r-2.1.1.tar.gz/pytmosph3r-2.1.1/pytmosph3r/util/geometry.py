import math as m
import numpy as np
import numba
from .math import roots
from ai import cs
from pytmosph3r.util.util import prop


class PointCircle:
    """2D polar coordinates."""
    def __init__(self, radius, angle):
        self.radius = radius
        self.angle = angle

    @prop
    def coords(self):
        return (self.radius, self.angle)

class PointSpherical:
    """3D spherical coordinates."""
    def __init__(self, radius, latitude, longitude):
        self.radius = radius
        self.latitude = latitude
        self.longitude = longitude % (2*np.pi)

    @prop
    def coords(self):
        return (self.radius, self.latitude, self.longitude)

class PointCartesian:
    """3D Cartesian coordinates."""
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @prop
    def coords(self):
        return (self.x, self.y, self.z)

    @prop
    def norm(self):
        return m.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __sub__(self, other):
        return PointCartesian(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, other):
        return PointCartesian(other*self.x, other*self.y, other*self.z)

@numba.njit()
def fast_solve_latitude(x, latitudes, z_ray, norm_ray, dir_latitude):
    for i in range(len(latitudes)):
        a = m.sin(latitudes[i])**2 - m.sin(dir_latitude)**2
        b = - 2 * m.sin(dir_latitude) * z_ray
        c = ((norm_ray * m.sin(latitudes[i]))**2 - z_ray**2)

        sol = roots(a,b,c)
        if len(sol) > 0:
            x[i] = sol[0]
        if len(sol) > 1:
            x[len(latitudes)+i] = sol[1]

class CoordinateSystem:
    """Computes the intersection of a ray going through :py:attr:`ray_origin` following the direction :py:attr:`direction`.

    Args:
        direction (:class:`PointCartesian`): Direction (x,y,z) of the ray.
        ray_origin (:class:`PointCartesian`): Cartesian coordinates (x,y,z) of the ray intersection point with the terminator.
    """

    def __init__(self, direction, ray_origin=None):
        self.direction = direction
        self.ray_origin = ray_origin

    def radius(self, x):
        return np.sqrt(self.ray_origin.norm**2 + x**2 )

    def latitude(self, x):
        with np.errstate(invalid='ignore'):
            return -np.arcsin((self.ray_origin.z + x * self.direction.z) /
                    self.radius(x))

    def longitude(self, x):
        with np.errstate(all='ignore'):
            longitude = np.arctan((self.ray_origin.y + x * self.direction.y) /
                        (self.ray_origin.x + x * self.direction.x) )
            # tan(x) is defined only between -pi/2 and pi/2, so here is a fix for our definition
            longitude[self.ray_origin.x + x * self.direction.x < 0] += np.pi
            numerator_sign = np.sign(self.ray_origin.y + x * self.direction.y)[self.ray_origin.x + x * self.direction.x == 0]
            longitude[self.ray_origin.x + x * self.direction.x == 0] = numerator_sign * np.pi/2
        return longitude

    def solve_radius(self, radii):
        with np.errstate(invalid='ignore'):
            x = np.sqrt(radii**2 - self.ray_origin.norm**2 )
        x = np.concatenate([-x, x]) # doubled because of symmetry before and after the ray origin point
        return x, self.latitude(x), self.longitude(x)

    def solve_latitude(self, latitudes):
        x = np.full(2*len(latitudes), np.nan)
        fast_solve_latitude(x, latitudes, self.ray_origin.z, self.ray_origin.norm, self.spherical_direction.latitude) # numba call
        return x, self.radius(x), self.latitude(x), self.longitude(x)

    def solve_longitude(self, longitudes):
        x = ((self.ray_origin.y - self.ray_origin.x * np.tan(longitudes)) /
             (self.direction.x * np.tan(longitudes) - self.direction.y))
        if np.isclose(self.ray_origin.y, 0) and np.isclose(self.direction.y, 0):
            # special case when formula above is independent from longitudes
            x = np.full(longitudes.shape, np.nan)
        return x, self.radius(x), self.latitude(x), self.longitude(x)

class CartesianCoordinateSystem(CoordinateSystem):
    """Same as :class:`CoordinateSystem`, but initialize the system with a direction and an ray origin given in spherical and polar coordinates, respectively.
    """

    def __init__(self, latitude, longitude):
        self.spherical_direction = PointSpherical(1, latitude, longitude)
        x,y,z = cs.sp2cart(1, latitude, longitude)
        system_direction = PointCartesian(np.float(x),np.float(y),np.float(z))
        super().__init__(system_direction)

    @prop
    def y_coeff(self):
        #  y**2 + b * y + c
        dir_lat = self.spherical_direction.latitude
        dir_lon = self.spherical_direction.longitude
        b = 2 * m.sin(dir_lat) * m.tan(dir_lon) * m.cos(self._point.angle)
        c = m.cos(self._point.angle)**2 * ((m.sin(dir_lat)**2 / m.cos(dir_lon)**2) + m.cos(dir_lat)**2) -1
        return [1, b, c]

    def coordinates(self, radius, angle):
        """Returns coordinates in Cartesian coordinate `system` of point at (`radius`, `angle`) """
        self._point = PointCircle(radius, angle)
        z = radius * m.cos(self.spherical_direction.latitude) * m.cos(angle)
        if np.isclose(self.spherical_direction.longitude, np.pi/2) or np.isclose(self.spherical_direction.longitude, 3*np.pi/2):
            y = -self.direction.z*z/self.direction.y
        else:
            y_sol = roots(*self.y_coeff) # two solutions
            y_r = y_sol[0]
            if angle > np.pi: # cos(angle)**2 == cos(-angle)**2
                y_r = y_sol[1]
            y = y_r * self._point.radius * m.cos(self.spherical_direction.longitude)
        if np.isclose(self.direction.x, 0):
            with np.errstate(all='ignore'):
                x = np.sqrt(radius**2 - y**2 - z**2)
                if (angle < np.pi and self.direction.y > 0) or (angle > np.pi and self.direction.y < 0):
                    x = -x
            if np.isnan(x):
                x = 0 # handle rounding error that makes sqrt negative
        else:
            x = (- (y * self.direction.y) - ( z * self.direction.z )) / self.direction.x
        return PointCartesian(x, y, z) #, PointCartesian(x, y[1], z)

    def add_ray_origin(self, radius, angle):
        self.ray_origin = self.coordinates(radius, angle)
        try:
            assert np.isclose(self.ray_origin.norm, radius)
        except:
            raise ArithmeticError("Radius (%s) doesn't match norm of ray origin point (%s). Check the formulas or report as a bug!"%(radius, self.ray_origin.norm))
