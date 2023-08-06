from tqdm.auto import tqdm
from pytmosph3r.util.util import get_chunk, spectral_chunks, get_chunk_size
import numpy as np
from pytmosph3r.log import Logger
from pytmosph3r import mpi
import multiprocessing as mp
from multiprocessing import Pool

def transit_depth_angle(transmission, rk, nprocs, *args, **kwargs):
    integrals = []
    iterations = range(*get_chunk(rk, nprocs, transmission.rays.n_angular))
    if rk == 0:
        iterations = tqdm(iterations, leave=False)
    for i in iterations:
        transmission.per_angle = True
        transmission.rays.angle_idx = i
        integrals.append(transmission.angle_to_integral())
    return integrals

def transit_depth_grid(transmission, rk, nprocs, *args, **kwargs):
    # raise NotImplementedError # not functional yet
    rays = transmission.rays
    bounds = get_chunk(rk, nprocs, rays.shape)
    return transmission.grid_to_transmittance(bounds)

def transit_depth_wn(transmission, rk, nprocs, *args, **kwargs):
    # raise NotImplementedError  # not functional yet
    chunk = get_chunk(rk, nprocs, transmission.opacity.k_data.Nw)
    wn_range = [transmission.opacity.k_data.wnedges[chunk[0]-1],
                transmission.opacity.k_data.wnedges[chunk[1]]]
    if rk == 0:
        wn_range[0] = -1
    return transmission.wn_to_integral(wn_range=wn_range, *args, **kwargs)

def transit_depth_i(transmission, rk, nprocs, dimension, *args, **kwargs):
    """Returns a list of integrals that will be concatenated/stacked together with the rest."""
    if dimension == "angles":
        return transit_depth_angle(transmission, rk, nprocs, *args, **kwargs)
    if dimension == "rays":
        return transit_depth_grid(transmission, rk, nprocs, *args, **kwargs)
    if dimension == "spectral":
        return transit_depth_wn(transmission, rk, nprocs, *args, **kwargs)

class Parallel(Logger):
    """
    Base class for a parallel version of the transit depth (see :class:`~pytmosph3r.transmission.Transmission`).

    Args:
        nprocs (int): number of procs (by default, maximum).
        dimension (str): Dimension to subdivide among workers. Possible values are `spectral`, `angles`, or `rays`. A `spectral` subdivision shares the spectral range among the workers, `angles` means the angular points of the rays grid are used, while `rays` means all of the rays grid is shared among the workers.
    """
    nprocs = None
    def __init__(self, name, nprocs=None, dimension="rays"):
        name =  self.__class__.__name__ if name is None else name
        super().__init__(name)
        Parallel.nprocs = nprocs
        if nprocs:
            Parallel.nprocs = int(nprocs)
        else:
            Parallel.nprocs = mp.cpu_count()
        self.dimension = dimension

    def synchronize(self, model):
        self.info("Running on %s procs. (on %s dimension)"%(Parallel.nprocs, self.dimension))
        self.model = model
        return model

    def compute_integral(self, transmission, *args, **kwargs):
        """Compute integral over :attr:`nprocs` processes by subdividing the work along the spectral dimension (if :attr:`dimension` is "spectral) or rays dimension(s).
        """
        self.transmission = transmission
        self.model = transmission.model
        integrals = self._compute_integral(transmission, *args, **kwargs)
        integral = self.retrieve_results(integrals)
        return integral


    def retrieve_results(self, results):
        if mpi.get_rank(): # only P0 retrieves results
            return results
        results = [result for result in results if len(result)] # if too many workers, some may have not worked at all! :-O
        if self.dimension == "rays":
            transmittance = np.concatenate(results)
            transmittance = transmittance.reshape(self.transmission.rays.shape+ (self.transmission.opacity.k_data.Nw,))
            # this mode's only computed transmittance for now
            return self.transmission.transmittance_to_integral(transmittance)
        return np.concatenate(results)

class MultiProcTransit(Parallel):
    def __init__(self, nprocs=None, *args, **kwargs):
        super().__init__(self.__class__.__name__, nprocs, *args, **kwargs)
        self.rk = 0

    def _compute_integral(self, transmission, *args, **kwargs):
        with Pool(Parallel.nprocs) as p:
            integrals = p.starmap(transit_depth_i, tqdm([(transmission, rk, self.nprocs, self.dimension, *args, *kwargs) for rk in range(self.nprocs)], total=self.nprocs, leave=False))
        return integrals

class MpiTransit(Parallel):
    max_size = 1000
    """Maximum message size."""
    def __init__(self, slaves=False, *args, **kwargs):
        Logger.__init__(self, self.__class__.__name__)
        if 'nprocs' in kwargs.keys():
            self.error("'nprocs' declared in config file (%s). MPI parameter (%s) will be used instead."%(kwargs["nprocs"], mpi.nprocs()))
        kwargs.update(nprocs=mpi.nprocs())

        super().__init__(self.__class__.__name__, *args, **kwargs)
        self.slaves = slaves
        self.rk = mpi.get_rank()

    def synchronize(self, model):
        model = mpi.broadcast(model)
        mpi.barrier()
        model.parallel = self # do not get rk from P0
        return super().synchronize(model)

    def _compute_integral(self, transmission, *args, **kwargs):
        # transmission = mpi.broadcast(transmission)
        self.transmission = transmission
        self.Nw = source_Nw = transmission.opacity.k_data.Nw
        reqs = []
        local_rk = rk = mpi.get_rank()
        nprocs = mpi.nprocs()
        if self.slaves and nprocs: # if at least one other worker, enslave it!
            nprocs -= 1
            local_rk -= 1
        if self.dimension == "spectral":
            spectral_chunk = get_chunk(rk, mpi.nprocs(), transmission.opacity.k_data.Nw)
            self.Nw = spectral_chunk[1] - spectral_chunk[0] # in spectral division, it may change from worker to worker

        n_msg = 1
        if self.Nw > self.max_size:
            n_msg = int(np.ceil(self.Nw/self.max_size))
        msg_size = int(np.ceil(self.Nw/n_msg))
        self.debug("Nw = %s; n_msg %s"% (self.Nw, n_msg))

        if self.dimension != "spectral" and rk == 0:
            self.info("P0 computing its part...")

        integral_local = transit_depth_i(transmission, rk, self.nprocs, self.dimension, *args, **kwargs)

        if rk:
            for i, integral_chunk in enumerate(integral_local):
                for msg in range(n_msg): # divide the message because of MPI limit
                    tag = msg + i*n_msg
                    if self.dimension == "spectral":
                        tag *= transmission.rays.n_angular
                        tag += transmission.rays.angle_idx
                    end = min((msg+1)*msg_size, len(integral_chunk))
                    data = integral_chunk[msg*msg_size:end]
                    req = mpi.comm.isend(data, dest=0, tag=tag)
                    reqs.append(req)
        for req in reqs:
            req.wait()

        # Get back the results from other workers
        results = [integral_local]
        if rk == 0:
            sources = range(self.nprocs)
            if self.dimension != "spectral":
                self.info("Retrieving results from other workers...")
                sources = tqdm(sources, leave=False)
            for source in sources:
                if self.dimension == "spectral":
                    spectral_chunk = get_chunk(source, mpi.nprocs(), transmission.opacity.k_data.Nw)
                    source_Nw = spectral_chunk[1] - spectral_chunk[0] # in spectral division, it may change from worker to worker
                if self.slaves:
                    source += 1
                if source:
                    integral_source = []
                    for i, value in enumerate(self.list_chunks(source)):
                        integral_source.append(np.zeros(source_Nw))
                        for msg in range(n_msg):
                            tag = i*n_msg+msg
                            if self.dimension == "spectral":
                                tag *= transmission.rays.n_angular
                                tag += transmission.rays.angle_idx
                            end = min((msg+1)*msg_size, source_Nw)
                            req = mpi.comm.irecv(source=source, tag=tag)
                            data = req.wait()
                            integral_source[i][msg*msg_size:end] = data
                        self.debug("P%s: received %s from P%s"% (rk, value, source))
                    if self.dimension == "spectral":
                        integral_source = np.concatenate(integral_source)
                    results.append(integral_source)
        return results

    def list_chunks(self, source):
        if self.dimension == "angles":
            return range(*get_chunk(source, mpi.nprocs(), self.transmission.rays.n_angular))
        elif self.dimension == "spectral":
            return [get_chunk(source, mpi.nprocs(), self.transmission.opacity.k_data.Nw)]
        elif self.dimension == "rays":
            return range(*get_chunk(source, mpi.nprocs(), self.transmission.rays.n_radial*self.transmission.rays.n_angular))
