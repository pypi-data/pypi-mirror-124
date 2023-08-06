import os
import sys
import numpy as np
from pytmosph3r.util.util import get_attributes, get_methods, retrieve_name
from pytmosph3r.log import Logger
from pytmosph3r.mpi import get_rank, only_master_rank

class Input(Logger):
    """Base class to read input data.
    :class:`~pytmosph3r.interface.HDF5Input` and
    :class:`~pytmosph3r.interface.ncInput` inherit from it.
    """
    def __init__(self, filename):
        super().__init__('Input')
        self.filename = filename
        self.f = None
        self.variable = None

    def open(self):
        if get_rank() == 0:
            self._openFile()

    def _openFile(self):
        raise NotImplementedError

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    @only_master_rank
    def __getitem__(self, path):
        if self.f is None:
            self._openFile()
        return self.f[path]

    def keys(self, path="."):
        if self.f is None:
            self._openFile()
        return self.f[path].keys()

    def get(self, path):
        raise NotImplementedError

    def getclass(self, path):
        raise NotImplementedError

    @only_master_rank
    def read(self, path, class_obj=None):
        """Read a class (class_obj) from path in HDF5.
        The keys in `path` have to match the class arguments.

        Args:
            path (string): Path to class
            class_obj (Class): Class to read
        """
        if self.f is None:
            self._openFile()
        obj = self._read(path, class_obj)
        self.close()
        return obj

    def _read(self, path, class_obj=None):
        if not class_obj:
            try:
                class_obj = getattr(sys.modules["pytmosph3r"],self.getclass(path))
            except:
                if isinstance(self.f[path], self.variable):
                    return self.get(path)
                else:
                    class_obj=dict
        params = {}
        for key in self.keys(path):
            try:
                key = int(key)
                class_obj = list
            except:
                pass
            params[key] = self.read(path+"/"+str(key))
        try:
            if class_obj == list:
                return class_obj(list(params.values()))
            return class_obj(**params)
        except:
            try:
                obj = class_obj()
                inputs={key:params[key] for key in obj.inputs()}
                return class_obj(**inputs)
            except:
                self.warning("Reading %s as dict."%path)
                return params

class Output(Input):
    """Base class to write outputs.
    :class:`~pytmosph3r.interface.HDF5Output` and
    :class:`~pytmosph3r.interface.ncOutput` inherit from it.
    """
    def __init__(self, filename, append=False):
        Logger.__init__(self, 'Output')
        self.filename = filename
        folder = os.path.dirname(filename)
        if not len(folder):
            folder = "."
        os.makedirs(folder, exist_ok=True)
        self._append = append
        self.f = None
        self.group_func = None
        """Function pointer to the method creating a group"""
        self.group_class = None
        """Class pointer to the subclass handling groups"""

    def create_group(self, group_name):
        group = None
        if self.f:
            group = self.group_func(self.f, str(group_name))
        return self.group_class(group)

    def createGroup(self, group_name):
        return self.create_group(group_name)

    def close(self):
        if self.f:
            self.f.close()

    def write_list(self, list_array, list_name=None, metadata=None):
        arr = np.array(list_array)
        return self.write_item(list_name, arr)

    @only_master_rank
    def write_item(self, item, key=None, metadata=None, to_write='inputs', verbose=False):
        ds = None
        if key is None:
            key = retrieve_name(item, up=2) #2 because of wrapper
        if not isinstance(key,(str,)):
            key = str(key)
        if isinstance(item,(str,)) or isinstance(item, (float,int,np.int64,np.float64,)):
            ds = self.f.create_dataset(key, data=item)
        elif isinstance(item,(np.ndarray,)):
            try:
                ds = self.f.create_dataset(key, data=item, shape=item.shape, dtype=item.dtype)
            except TypeError:
                group = self.create_group(key)
                for idx,val in enumerate(item):
                    group.write_item(val, idx)
                ds = group
        elif isinstance(item,(list,tuple,)):
            if isinstance(item,tuple):
                item = list(item)
            if True in [isinstance(x,str) for x in item]:
                ds = self.write_string_array(item, key)
            else:
                try:
                    arr_item=np.array(item)
                    ds = self.f.create_dataset(key, data=arr_item, shape=arr_item.shape, dtype=arr_item.dtype)
                except TypeError:
                    group = self.create_group(key)
                    for idx,val in enumerate(item):
                        group.write_item(val, idx)
                    ds = group

        elif isinstance(item, dict):
                group = self.create_group(key)
                ds = group.write_dictionary(item)
        else:
            try:
                group = self.create_group(key)
                ds = group.write_obj(item, to_write=to_write)
            except:
                self.warning("Couldn't write %s"% key)
        if metadata:
            for k, v in metadata.items():
                ds.attrs[k] = v
        return ds


    @only_master_rank
    def write_dictionary(self, dic):
        """Recursively write a dictionary into output."""
        for key, item in dic.items():
            try:
                self.write_item(item, key)
            except TypeError:
                raise ValueError('Cannot save %s type'%type(item))
        return self

    @only_master_rank
    def write_obj(self, obj, to_write='inputs', items=None):
        """Write an object."""
        self.attrs['class'] = obj.__class__.__name__
        if to_write in get_methods(obj):
            items = getattr(obj, to_write)() # let object decide what to write
        elif items is None:
            items = obj.__dict__.keys() # by default, write all attrs
        for key, item in get_attributes(obj):
            if key in items:
                self.write_item(item, key, to_write=to_write)
        return self

    @only_master_rank
    def write_output(self, obj, items=None):
        """Write outputs."""
        return self.write_obj(obj, to_write='outputs', items=items)

class Group(Output):
    def __init__(self, f):
        super().__init__('Group')
        self.f = f

def write_spectrum(output_file="pytmosph3r_spectrum.dat", model=None):
    """Save a spectrum to a .dat file using a :attr:`model`.
    The first column lists the wavelengths, the second the value of the flux, the third the noise errorbar, and the fourth the widths of the wavelength edges.
    """
    folder = os.path.dirname(output_file)
    if not len(folder):
            folder = "."
    os.makedirs(folder, exist_ok=True)
    wl_width = np.abs(np.diff(model.spectrum.wledges))
    noise = np.full_like(model.spectrum.value, model.noise)
    np.savetxt(output_file, np.stack((model.spectrum.wls, model.spectrum.value, noise, wl_width)).T[::-1])
    try:
        if model.noise == 0:
            return # no need to write noised spectrum
        noised_file = "pytmosph3r_noised_spectrum.dat"
        if output_file.endswith(".dat"):
            noised_file = output_file[:-4]+"_noised.dat"
        np.savetxt(noised_file, np.stack((model.noised_spectrum.wls, model.noised_spectrum.value, noise, wl_width)).T[::-1])
    except:
        pass