"""
@author: A. Falco

Logging module, copied from TauREX 3 (https://github.com/ucl-exoplanets/TauREx3_public/tree/master/taurex/log).
"""

import logging
from pytmosph3r.util.util import get_methods
from pytmosph3r.util.memory import MemoryUtils

__all__ = ['Logger']

root_logger = logging.getLogger('pytmosph3r')
root_logger.propagate = False
"""Root logger for pytmosph3r"""

class LogHandler(logging.StreamHandler,):
    """
    Logging Handler for Pytmosph3R. Prevents other
    MPI threads from writing to log unless they are in trouble (>=ERROR)

    Parameters
    ----------
    stream : stream-object , optional
        Stream to write to otherwise defaults to ``stderr``
    """

    def __init__(self, stream=None):
        from pytmosph3r.mpi import get_rank
        super().__init__(stream=stream)

        self._rank = get_rank()

    def emit(self, record):
        if self._rank == 0 or record.levelno >= logging.ERROR:
            return super(LogHandler, self).emit(record)
        else:
            pass

rh = LogHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
rh.setFormatter(formatter)
rh.setLevel(logging.DEBUG)
root_logger.handlers = []
root_logger.addHandler(rh)
root_logger.setLevel(logging.INFO)

class Logger(MemoryUtils):
    """
    Standard logging using logger library

    Parameters
    -----------
    name : str
        Name used for logging
    """
    verbose = 0

    def __init__(self, name):
        self._log_name = 'pytmosph3r.{}'.format(name)

        self._logger = logging.getLogger('pytmosph3r.{}'.format(name))

    def info(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.warning(message, *args, **kwargs)

    def debug(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.debug(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.error(message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        """ See :class:`logging.Logger` """
        self._logger.critical(message, *args, **kwargs)

    def isEnabledFor(self, level):
        return self._logger.isEnabledFor(level)

    def search_path(self, filename):
        """Search for filename in current folder, then in :attr:`~pytmosph3r.relative_dir`, and finally in the `examples/` folder of the `pytmosph3r` code. It then set the attribute :attr:`filename` to its path.
        """
        self.filename = None
        if filename:
            import os
            self.filename = filename
            if not os.path.isfile(filename):
                import pytmosph3r as p3
                self.filename = os.path.realpath(os.path.join(p3.relative_dir, filename))
                if os.path.exists(self.filename):
                    self.warning("File ./%s doesn't exist. Using %s"%(filename, self.filename))
                else:
                    relative_filename = self.filename
                    self.filename = os.path.realpath(os.path.join(p3.root_dir, "examples", filename))
                    if os.path.exists(self.filename):
                        self.warning("File ./%s and %s don't exist. Using %s"%(filename, relative_filename, self.filename))
                    else:
                        raise IOError("Couldn't find file %s"%(filename))
        return self.filename

    def __repr__(self) -> str:
        if not ("inputs" in get_methods(self) or "outputs" in get_methods(self)):
            return super().__repr__()
        msg = "The attributes of "+ self.__class__.__name__ + "() are:\n"
        if "inputs" in get_methods(self):
            msg += "- Inputs: %s\n"%self.inputs()
        if "outputs" in get_methods(self):
            msg += "- Outputs: %s\n"%self.outputs()
        return msg