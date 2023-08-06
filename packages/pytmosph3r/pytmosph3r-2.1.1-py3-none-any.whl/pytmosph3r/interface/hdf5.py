import h5py
from packaging import version
from pytmosph3r.util.util import retrieve_name, prop
from pytmosph3r.log import Logger
from pytmosph3r.mpi import only_master_rank
from pytmosph3r import __version__
import datetime
from .io import Input, Output

class HDF5Input(Input):
    def __init__(self, filename):
        super().__init__(filename)
        Logger.__init__(self, "HDF5Input")
        self.variable = h5py.Dataset

    @prop
    def attrs(self):
        return self.f.attrs

    def _openFile(self):
        self.f = h5py.File(self.filename, mode='r')

    def getclass(self, path):
        return self.f[path].attrs["class"]

    def get(self, path):
        if self.f is None:
            self._openFile()
        value = self.f[path][...]
        if value.ndim == 0:
            try:
                return float(value)
            except:
                if version.parse(h5py.version.version) >=  version.parse("3"):
                    try:
                        return self.f[path].asstr()[()]
                    except:
                        return str(value)
                return str(value)
        if version.parse(h5py.version.version) >=  version.parse("3"):
            try:
                return self.f[path].asstr()[()]
            except:
                return value
        return value

class HDF5Output(Output, HDF5Input):
    def __init__(self, filename, append=False):
        Output.__init__(self, filename, append)
        Logger.__init__(self, 'HDF5Output')
        self.group_func = h5py.Group.create_group
        self.group_class = HDF5Group

    def _openFile(self):
        mode = 'w'
        if self._append:
            mode = 'a'
        self.f = h5py.File(self.filename, mode=mode)
        self.f.attrs['file_name'] = self.filename
        self.f.attrs['file_time'] = datetime.datetime.now().isoformat()
        self.f.attrs['creator'] = self.__class__.__name__
        self.f.attrs['HDF5_Version'] = h5py.version.hdf5_version
        self.f.attrs['h5py_version'] = h5py.version.version
        self.f.attrs['program_name'] = 'Pytmosph3R'
        self.f.attrs['program_version'] = __version__

    @only_master_rank
    def write_string_array(self, string_array, string_name=None, metadata=None):
        if string_name is None:
            key = retrieve_name(string_array, up=2) #2 because of wrapper
        asciiList = [n.encode("ascii", "ignore") for n in string_array]
        return self.f.create_dataset(
            str(string_name), (len(asciiList)), 'S64', asciiList)

class HDF5Group(HDF5Output):
    def __init__(self, f):
        super().__init__('HDF5Group')
        self.f = f

def write_hdf5(h5_output, model, group_name="Model"):
    """Write :attr:`model` into group `group_name` in HDF5 `h5_output`.

    Args:
        h5_output (string): Name of HDF5 output file.
        model (:class:`~pytmosph3r.model.model.Model`):  Model to write.
        group_name (str, optional): Either "Model" or "Outputs". Decides which data to write to :attr:`group_name` (model or outputs). Defaults to "Model".
    """
    append=False
    if group_name != "Model":
        if group_name != "Outputs":
            Logger("HDF5Output").debug("Does not know group %s. Will consider it as outputs." % group_name)
        append=True
    with HDF5Output(h5_output, append=append) as o:
        group = o.create_group(group_name)
        if append:
            group.write_obj(model, to_write="outputs")
        else:
            group.write_obj(model)