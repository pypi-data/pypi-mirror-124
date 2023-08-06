import sys
import re
import numpy as np
import psutil
from .util import retrieve_name
import platform

class MemoryUtils:
    """This class is inherited from :class:`Logger`."""

    margin = 1
    """Margin (in ratio wrt available memory) that we can allow to allocate (to avoid swapping)."""

    def check_memory(self, to_check, name=None, obj_type=float):
        """Check if memory of :py:attr:`to_check` is lower than available memory.

        Args:
            to_check (array, int): If an array, calculate its theoretical memory based on its shape and dtype. If the number of elements (for example before creating an array), multiply by the size of :py:attr:`obj_type`
            name (str, optional): Name to print in message. Defaults to None. If :py:attr:`to_check` is an array, it will try to retrieve the variable name.
            obj_type (type, optional): Type of :py:attr:`to_check` (to use only if it's a number, not an array). Defaults to `float`.
        """
        if name is None:
            try:
                name = retrieve_name(to_check, 1)
            except:
                name = "Object"
        mem, mem_available = self.available_memory(to_check)
        if mem > MemoryUtils.margin * mem_available:
            raise MemoryError("%s (%s GB) won't fit in memory (%s GB available). You can release some RAM (preferrable) or try to increase pytmosph3r.MemoryUtils.margin (= %s), if you are not afraid of swapping or crashing..."%(name, mem/1e9, mem_available/1e9, MemoryUtils.margin))
        else:
            self.debug("%s will use as much as %s MB"%(name, mem/1e6))

    def available_memory(self, to_check, name=None, obj_type=float):
        """Returns how much of the available memory an object is consuming.

        Args:
            to_check (array, int): If an array, calculate its theoretical memory based on its shape and dtype. If the number of elements (for example before creating an array), multiply by the size of :py:attr:`obj_type`
            name (str, optional): Name to print in message. Defaults to None. If :py:attr:`to_check` is an array, it will try to retrieve the variable name.
            obj_type (type, optional): Type of :py:attr:`to_check` (to use only if it's a number, not an array). Defaults to `float`.
        """
        if isinstance(to_check, np.ndarray):
            mem = np.prod(to_check.shape) * to_check.dtype.itemsize
        else:
            mem = to_check * sys.getsizeof(obj_type())
        mem_available = dict(psutil.virtual_memory()._asdict())['available']
        return mem, mem_available

def memory_usage(pattern="VmR"):
    """Returns overall memory usage of process. (Linux only)"""
    if platform.system() != "Linux":
        return
    file=open("/proc/self/status")
    for line in file:
        if re.search(pattern, line):
            return " ".join(line.split()[1:]).strip()