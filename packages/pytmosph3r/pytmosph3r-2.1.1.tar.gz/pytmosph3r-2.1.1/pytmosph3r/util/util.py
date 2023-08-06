import numpy as np
import inspect
import warnings
import datetime
from functools import wraps

def get_attributes(obj):
    """Returns attributes of an object if they do not start nor end with an underscore.
    """
    members = inspect.getmembers(obj, lambda a:not(inspect.isroutine(a)))
    return [a for a in members if not(a[0].startswith('_') or a[0].endswith('_'))]

def get_methods(obj):
    """Returns methods of an object.
    """
    return [m[0] for m in inspect.getmembers(obj, lambda a:inspect.ismethod(a))]

def retrieve_name(var, up=0):
    """Retrieve the name of a variable :py:attr:`var` as a string. For example if :py:attr:`var` is named \'temperature\', the function will return \"temperature\".
    Example::
        def test(hello, up=0):
            return retrieve_name(hello, up)
        bonjour = \"bonjour\"
        test(bonjour) # returns \"hello\"
        test(bonjour, up=1) # returns \"bonjour\"

    Args:
        var: Variable
        up: context to retrieve from (default is the current context, i.e., the function in which the function has been called)
    """
    if up == 0:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    elif up == 1:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    elif up == 2:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def get_altitude_index(altitude, n_vertical):
    """Return altitude index associated with keyword `altitude` (within \"surface\",\"top\",\"middle\"). If not among this keyword,
    """
    if altitude == "surface":
        return 0
    elif altitude == "top":
        return n_vertical-1
    elif altitude == "middle":
        return int(n_vertical/2)
    if not isinstance(altitude, (int, list, np.ndarray)):
        raise TypeError("Altitude %s not recognized." % altitude)
    return altitude

def get_latitude_index(latitude, n_latitudes=None):
    """Return latitude index associated with keyword `latitude` (within \"north\",\"pole\",\"equator\").
    """
    if latitude == "north":
        return 0
    elif latitude == "south":
        return n_latitudes-1
    elif latitude == "equator":
        return int(n_latitudes/2)
    try:
        latitude=int(latitude)
    except:
        raise TypeError("Latitude %s not recognized." % latitude)
    return latitude

def get_longitude_index(longitude, n_longitudes=None):
    """Return longitude index associated with keyword `longitude` (within \"day\",\"night\",\"terminator\").
    The keywords refer to the position of the star if the direction of the rays has been defined as (latitude, longitude) = (0,0).
    """
    if longitude == "day":
        return int(n_longitudes/2)
    elif longitude == "night":
        return 0
    elif longitude == "terminator":
        return int(n_longitudes/4)
    try:
        longitude = int(longitude)
    except:
        raise TypeError("Longitude %s not recognized." % longitude)
    return longitude

def get_index(array, location, dim="altitude"):
    """Return the index of `location` in `array` at the dimension `dim` (altitude/latitude/longitude). For example, if `dim` is 'altitude' and `location` is 'surface', it will return 0."""
    if isinstance(array, (float, str)) or array.ndim != 3:
        warnings.warn("%s doesn't have 3 dimensions"% type(array))
        return array
    if dim == "altitude":
        return get_altitude_index(location, array.shape[0])
    elif dim == "latitude":
        return get_latitude_index(location, array.shape[1])
    elif dim == "longitude":
        return get_longitude_index(location, array.shape[2])
    else:
        warnings.warn("Dimension '%s' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. Returning 0..."% dim)
        return 0

def get_2D(array, location, dim="altitude"):
    """Return a 2D slice of array `array` at the dimension `dim` (among altitude, latitude and longitude). For example if `dim` is 'altitude', it will return the 2D array of all latitudes and longitudes at this altitude."""
    if isinstance(array, (float, str)) or array.ndim != 3:
        warnings.warn("%s doesn't have 3 dimensions"% type(array))
        return array
    if dim == "altitude":
        return array[get_altitude_index(location, array.shape[0])]
    elif dim == "latitude":
        return array[:, get_latitude_index(location, array.shape[1])]
    elif dim == "longitude":
        return array[:, :, get_longitude_index(location, array.shape[2])]
    else:
        warnings.warn("Dimension '%s' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. Returning whole array but the program will be probably fail..."% dim)
        return array

def get_column(array, latitude, longitude):
    """Return a vertical column of array `array` at the position (`latitude`, `longitude`).
    """
    if isinstance(array, (float, str)) or array.ndim != 3:
        return array
    return array[:, get_latitude_index(latitude, array.shape[1]), get_longitude_index(longitude, array.shape[2])]

def convert_log(array, units):
    """Convert :attr:`array` from log space to normal space. :attr:`units`  determines if the space is log or ln."""
    if units is None:
        return array
    if "log" in units:
        array = np.power(10, array)
    elif "ln" in units:
        array = np.exp(array)
    return array


def mol_key(mol_dict, mol, mol_type="vap", data=""):
    """Returns the key corresponding to `mol` in `mol_dict`.
    """
    key = mol + data
    if mol_dict is not None and key in mol_dict.keys():
        return mol_dict[key]
    else:
        return mol.lower() + "_" + mol_type + data

def aerosols_array_iterator(dictionary):
    """Returns an iterator over arrays of an aerosols dictionary.
    For example, if the dictionary looks like this:
    :code:`{'H2O':{'mmr':np.array([1, 2]), 'reff':1e-5}}`.
    The code will iterate over the mmr (array) but not reff (float).
    """
    for element, value in dictionary.items():
        for key_element, element_val in value.items():
            if isinstance(element_val, np.ndarray):
                yield element, key_element

def arrays_to_zeros(dictionary, shape):
    """Returns a copy of `dictionary` of which subarrays are initialized as an array of shape `shape` filled with zeros. Used for aerosols, to initialize the arrays before interpolating.
    """
    new_dict = dictionary.copy()
    for element, value in dictionary.items():
        new_dict[element] = value.copy()
        for key_element, element_val in value.items():
            if isinstance(element_val, np.ndarray):
                new_dict[element][key_element] = np.zeros(shape)
    return new_dict

def init_array(obj, size):
    """Returns `obj` if float, else array of size `size`."""
    if isinstance(obj, (float)):
        return obj
    else:
        return np.full((size), np.nan)

def get(obj, i):
    """Returns obj if float, else return the value of obj at `i`"""
    try:
        return obj[i]
    except:
        return obj

def update_dict(d, u):
    """Recursive update of nested dictionaries."""
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def spectral_chunks(k_database, n):
    chunk_size = len(k_database.wns)/n
    wn_ranges = []
    for chunk in range(n):
        try:
            wn_range = [k_database.wnedges[int((chunk * chunk_size)-1)], k_database.wnedges[int(min(len(k_database.wnedges)-1 , (chunk+1)*chunk_size))]]
            if chunk == 0:
                wn_range[0] = -1
            wn_ranges.append(wn_range)
        except IndexError:
            pass # Outside of wns range now
    return wn_ranges

def get_chunk(i, n, size):
    """Get i-th chunk out `n` chunks dividing `size`."""
    if hasattr(size, "__len__") and len(size) == 2: # 2 dimension
        chunk_size = size[0] * size[1]/n
        idx = int(i * chunk_size), int(min(int((i+1)*chunk_size), size[0] * size[1]))
        chunk_0 = [idx[0]%size[0], idx[1]%size[0]] # chunk in 1st  dimension
        chunk_1 = [int(idx[0]/size[0]), int(idx[1]/size[0])]  # chunk in 2nd dimension
        if idx[1] == size[0] * size[1]:
            chunk_0[1] = size[0]
            chunk_1[1] = size[1]-1
        chunk = [chunk_0, chunk_1]
    else:
        chunk_size = size/n
        chunk = [int(i * chunk_size), min(int((i+1)*chunk_size), size)]
    return chunk

def get_chunk_size(chunk, chunk_size, total_size):
    start = chunk*chunk_size # start of chunk
    end = min((chunk+1)*chunk_size, total_size) # last chunk may be shorter
    return end - start

def make_array(lis):
    """Get array from a list of lists. Missing data is replaced with -1."""
    n = len(lis)
    lengths = np.array([len(x) for x in lis])
    max_len = np.max(lengths)
    try:
        shape_element = lis[0][0].shape
        arr = np.full((n, max_len) + shape_element, -1.)
    except:
        arr = np.full((n, max_len), -1.)

    for i in range(n):
        arr[i, :lengths[i]] = lis[i]
    return np.array(arr)

def timer(f):
    """A decorator to try if function failed and issue a warning if it did."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = f(*args, **kwargs)
        end_time = datetime.datetime.now()
        total_time = end_time - start_time
        args[0].debug("%s run in %.2fs"%(f.__name__, total_time.total_seconds()))
        return result
    return wrapper

def prop(f):
    """A decorator to try if function failed and issue a warning if it did."""
    @property
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except:
            return None
    return wrapper
