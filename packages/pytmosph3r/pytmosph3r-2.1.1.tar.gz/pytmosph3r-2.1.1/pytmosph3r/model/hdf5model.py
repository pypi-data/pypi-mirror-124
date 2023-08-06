from pytmosph3r.model import Model
from pytmosph3r.log import Logger
from pytmosph3r.interface.hdf5 import HDF5Input

class HDF5Model(Model):
    """Model reading from HDF5. Same parameters as :class:`~pytmosph3r.model.model.Model`, with the addition of a :attr:`filename`."""
    def __init__(self, filename=None, *args, **kwargs):
        Logger.__init__(self, self.__class__.__name__)
        if filename is None:
            raise FileNotFoundError("No input file given. "+self.__class__.__name__+ " takes a 'filename' parameter")
        self.filename = filename

        Model.__init__(self, *args, **kwargs)

        self.search_path(filename)

    def read_data(self, *args, **kwargs):
        """This method is automated (see :func:`~pytmosph3r.interface.io.Input.read`).
        """
        self.info("Reading model from %s"% self.filename)
        model = {}
        with HDF5Input(self.filename) as f:
            model = f.read("Model")
        self.__dict__.update(model.__dict__)

    def inputs(self):
        return super().inputs() + ["filename"]