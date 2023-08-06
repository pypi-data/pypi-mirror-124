import numpy as np
from pytmosph3r.util.util import prop

class Grid:
    @prop
    def ndim(self):
        return len(self.shape)

    def walk(self, dims=None):
        """Return iterator over multiple dimensions.

        Args:
            dims (:obj:`array`): List of dimensions to iterate over. By default iterates over all dimensions (defined in the attribute `shape` of the current object.)
        """
        from itertools import product
        if dims is None:
            dims = range(len(self.shape))
        return product(*[range(self.shape[i]) for i in dims])

class Grid3D(Grid):
    """ Simple 3D grid based on a 2D longitude/latitude grid
        and an (abstract) vertical axis. You can overwrite the latitudes and longitudes of your grid points with the :attr:`mid_latitudes` and :attr:`mid_longitudes` parameters. Note that :attr:`latitudes` and :attr:`longitudes` are derived from these and return the boundaries of each cell of the grid.

    Args:
        n_vertical (int) : Number of vertical points in the grid.
        n_latitudes (int) : Number of latitudinal points in the grid.
        n_longitudes (int) : Number of longitudinal points in the grid.
    """

    def __init__(self, n_vertical=None, n_latitudes=None, n_longitudes=None, mid_latitudes=None, mid_longitudes=None):
        self.n_vertical = int(n_vertical) if n_vertical else None
        self.n_latitudes = int(n_latitudes) if n_latitudes else None
        self.n_longitudes = int(n_longitudes) if n_longitudes else None
        self._to_east = True  # going towards the east by default
        self._to_north = True  # going towards the south by default
        if mid_latitudes is not None: self.mid_latitudes = mid_latitudes
        if mid_longitudes is not None: self.mid_longitudes = mid_longitudes

    @prop
    def to_east(self):
        """True if longitude is in increasing order."""
        if not hasattr(self, "_to_east") or self._to_east is None:
            self._to_east = (np.diff(self.mid_longitudes) > 0).all()
        return self._to_east
    @prop
    def to_north(self):
        """True if latitude is in increasing order."""
        if not hasattr(self, "_to_north") or self._to_north is None:
            self._to_north = (np.diff(self.mid_latitudes) > 0).all()
        return self._to_north

    @prop
    def shape(self):
        """Shape of arrays in this grid."""
        return (self.n_vertical, self.n_latitudes, self.n_longitudes)

    def index_pole(self, pole_angle):
        """Returns index corresponding to an angle with the pole 0 (by convention, north)."""
        if pole_angle < 0:
            return self.index_pole(-pole_angle)
        elif pole_angle < self.lat_angle/2:
            return 0
        elif pole_angle > self.lat_angle * (self.n_latitudes-3/2):
            return self.n_latitudes-1
        else:
            return int(pole_angle/self.lat_angle +1/2)

    def index_latitude(self, latitude):
        """Gives the index of the latitude interval containing a `latitude` (given in `radians`)."""
        return self.index_pole(latitude + np.pi/2)

    def latitude(self, i):
        "Boundary angles in `rad` of latitude box with index `i`."
        try:
            return [self.latitudes[i], self.latitudes[i+1]]
        except IndexError as e:
            if i == self.n_latitudes:
                return [self.latitudes[i], None]
            raise e

    @prop
    def latitudes(self):
        """Latitudinal boundaries (deduced from :attr:`mid_latitudes`)."""
        if not hasattr(self,"_latitudes") or self._latitudes is None:
            self._latitudes = self.mid_latitudes[:-1]+np.diff(self.mid_latitudes)/2
            if self.to_north: # going up
                self._latitudes = np.insert(self._latitudes, 0, -np.pi/2)
                self._latitudes = np.append(self._latitudes, np.pi/2)
            else: # going down
                self._latitudes = np.insert(self._latitudes, 0, np.pi/2)
                self._latitudes = np.append(self._latitudes, -np.pi/2)
        return self._latitudes
    @latitudes.setter
    def latitudes(self, value):
        self._latitudes = value

    @prop
    def positive_latitudes(self):
        """Positive latitudinal boundaries (deduced from :attr:`mid_latitudes`)."""
        if not hasattr(self,"_positive_latitudes") or self._positive_latitudes is None:
            self._positive_latitudes = self.latitudes[np.where(self.latitudes >= 0)]
        return self._positive_latitudes

    @prop
    def mid_latitudes(self):
        """Latitudes in the \"middle\" of each latitude box."""
        if not hasattr(self,"_mid_latitudes") or self._mid_latitudes is None:
            if self.n_latitudes > 1:
                self._mid_latitudes = np.asarray([i*self.lat_angle-np.pi/2 for i in range(0, self.n_latitudes)])
            else:
                self._mid_latitudes = np.asarray([0]) # equator if only one latitude
        return self._mid_latitudes
    @mid_latitudes.setter
    def mid_latitudes(self, value):
        """Overwrite latitudes in the middle of each box."""
        self._mid_latitudes = np.asarray(value)
        # force recomputations of other variables that depend on mid_latitudes
        self._to_north = None
        self._positive_latitudes = None
        self._latitudes = None

    @prop
    def lat_angle(self):
        "Angle between two latitudes."
        if not hasattr(self,"_latitude_angle") or self._latitude_angle is None:
            try:
                self._latitude_angle = np.pi/(self.n_latitudes-1) # poles cover only half an angle
            except:
                self._latitude_angle = np.pi
        return self._latitude_angle

    def index_longitude(self, longitude):
        """Gives the index of the longitude interval containing a `longitude` (given in `radians`)."""
        if self.to_east:
            if longitude < self.all_longitudes[0]:
                return self.index_longitude(longitude+2*np.pi)
            elif longitude > self.all_longitudes[-1]:
                return self.index_longitude(longitude-2*np.pi)
            else:
                return int((longitude-self.all_longitudes[0])/self.lon_angle) % self.n_longitudes
        else:
            if longitude < self.all_longitudes[-1]:
                return self.index_longitude(longitude+2*np.pi)
            elif longitude > self.all_longitudes[0]:
                return self.index_longitude(longitude-2*np.pi)
            else:
                return (self.n_longitudes - int((longitude-self.all_longitudes[0])/self.lon_angle)) % self.n_longitudes

    def longitude(self, i):
        "Boundary angles in `rad` of longitude box with index `i`."
        return [self.all_longitudes[i], self.all_longitudes[i+1]]

    @prop
    def longitudes(self):
        """Longitudinal boundaries (unique). Deduced from :attr:`mid_longitudes`."""
        if not hasattr(self,"_longitudes") or self._longitudes is None:
            if self.to_east: # going up
                last = self.mid_longitudes[0]+2*np.pi
            else: # going down
                last = self.mid_longitudes[0]-2*np.pi
            self._longitudes = self.mid_longitudes-np.diff(np.concatenate([self.mid_longitudes,[last]]))/2
        return self._longitudes
    @longitudes.setter
    def longitudes(self, value):
        self._longitudes = value

    @prop
    def half_longitudes(self):
        """Half-list of longitudinal boundaries to avoid duplication. Deduced from :attr:`all_longitudes`."""
        if not hasattr(self,"_half_longitudes") or self._half_longitudes is None:
            self._half_longitudes = self.all_longitudes[:int(self.n_longitudes/2)]
        return self._half_longitudes

    @prop
    def all_longitudes(self):
        """Longitudinal boundaries (first longitude duplicated to make a full circle). Deduced from :attr:`longitudes`."""
        if not hasattr(self,"_all_longitudes") or self._all_longitudes is None:
            if self.to_east: # going up
                self._all_longitudes = np.concatenate([self.longitudes, [self.longitudes[0]+2*np.pi]])
            else: # going down
                self._all_longitudes = np.concatenate([self.longitudes, [self.longitudes[0]-2*np.pi]])
        return self._all_longitudes
    @all_longitudes.setter
    def all_longitudes(self, value):
        """Overwrite longitudinal boundaries."""
        self._all_longitudes = value

    @prop
    def mid_longitudes(self):
        """List of longitudes (in the \"middle\" of each longitude box). By default, start at -Pi."""
        if not hasattr(self,"_mid_longitudes") or self._mid_longitudes is None:
            self._mid_longitudes = np.asarray([self.lon_angle * i for i in range(self.n_longitudes)]) - np.pi
        return self._mid_longitudes
    @mid_longitudes.setter
    def mid_longitudes(self, value):
        """Overwrite longitudes in the middle of each box."""
        self._mid_longitudes = np.asarray(value)
        # force recomputations of other variables that depend on mid_longitudes
        self._to_east = None
        self._all_longitudes = None
        self._half_longitudes = None
        self._longitudes = None

    @prop
    def night_longitudes(self):
        """List of longitudinal indices on the `night` side.
        The night side is here defined as the first quarter of longitudinal indices and the last one.
        """
        return list(range(int(self.n_longitudes/4)))+ list(range(int(self.n_longitudes*3/4), self.n_longitudes))

    @prop
    def day_longitudes(self):
        """List of longitudinal indices on the `day` side.
        The day side is here defined as the second and third quarters of longitudinal indices.
        """
        return list(range(int(self.n_longitudes/4), int(self.n_longitudes*3/4)))

    @prop
    def lon_angle(self):
        "Angle between two longitudes."
        if not hasattr(self,"_longitude_angle") or self._longitude_angle is None:
            self._longitude_angle = 2*np.pi/(self.n_longitudes)
        return self._longitude_angle

    def make_3D(self, array):
        """This function will try to transform :attr:`array` from whatever dimension it is in to a 3D array of the same shape as the grid.

        Args:
            array (ndarray): 1, 2 or 3 dimensional array.

        Returns:
            (ndarray): 3D array.
        """
        if array.shape == self.shape:
            return array
        else:
            indices = np.arange(len(self.shape))
            axis = indices[np.isin(self.shape, array.shape)]
            new_axis = tuple([i for i, s in enumerate(self.shape) if i not in axis])
            return np.ones(self.shape) *np.expand_dims(array, axis=new_axis)

    def horizontal_walk(self, *args):
        """Iterator over horizontal grid (latitude, longitude)."""
        return self.walk([1, 2])

    def horizontal_run(self, function, *args, **kwargs):
        """Run a function over horizontal grid (latitude, longitude)."""
        for lat, lon in self.walk([1, 2]):
            function(lat, lon, *args, **kwargs)

    def inputs(self):
        return ['n_vertical', 'n_latitudes', 'n_longitudes']
    def outputs(self):
        return self.inputs()+['mid_latitudes','mid_longitudes']
