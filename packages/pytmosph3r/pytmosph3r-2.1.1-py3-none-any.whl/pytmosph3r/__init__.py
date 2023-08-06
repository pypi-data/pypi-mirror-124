from ._version import __version__
import os

pkg_name = "Pytmosph3R"
pkg_dir = os.path.dirname(os.path.abspath(__file__))
"""Directory containing sources of Pytmosph3R module"""
root_dir = os.path.join(pkg_dir,"..")
"""Root directory of Pytmosph3R repository"""
relative_dir = root_dir
"""Directory relative to root directory, for simpler paths in configuration file"""

from .planet import Planet
from .star import Star
from .chemistry import *
from .model import Model, HDF5Model, DiagfiModel
from .atmosphere import AltitudeAtmosphere, InputAtmosphere
from .grid import Grid3D
from .rays import Rays, Observer
from .opacity import Opacity
from .transmission import Transmission
from .emission import Emission
from .plot import Plot
from .interface import HDF5Input, HDF5Output, ncInput, ncOutput
from .util.memory import MemoryUtils
from .interface.io import write_spectrum
from .interface.hdf5 import write_hdf5
from .interface.netcdf import write_netcdf