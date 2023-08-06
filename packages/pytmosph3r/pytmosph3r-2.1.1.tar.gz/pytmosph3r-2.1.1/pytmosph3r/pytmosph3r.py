import datetime
import logging
import os
from pytmosph3r.log.logger import root_logger, Logger
from pytmosph3r.log import setLogLevel
from pytmosph3r.config import Config
from pytmosph3r.mpi import get_rank
from pytmosph3r.interface.io import write_spectrum
from pytmosph3r.interface.hdf5 import write_hdf5
from pytmosph3r.interface.netcdf import write_netcdf
from pytmosph3r.parser import pytmosph3r_parser
from . import __version__ as version

"""The entry point to Pytmosph3R"""

def main():
    """Reads a config file and runs Pytmosph3R"""

    root_logger.info('Welcome to Pytmosph3R %s'%version)
    root_logger.info("\n"\
    "         ,MMM8&&&.\n"\
    "    _...MMMMM88&&&&..._\n"\
    " .::'''MMMMM88&&&&&&'''::.\n"\
    "::     MMMMM88&&&&&&     ::\n"\
    "'::....MMMMM88&&&&&&....::'\n"\
    "   `''''MMMMM88&&&&''''`\n"\
    "         'MMM8&&&'\n")

    parser = pytmosph3r_parser()

    args = parser.parse_args()
    if args.all:
        if args.verbose is None:
            args.verbose = 2
        if args.h5_output is None:
            args.h5_output = "output_pytmosph3r.h5"
        if args.nc_output is None:
            args.nc_output = "output_pytmosph3r.nc"
        if args.spectrum_dat_output is None:
            args.spectrum_dat_output = "spectrum_pytmosph3r.dat"
    elif args.verbose is None:
        args.verbose = 0

    start_time = datetime.datetime.now()
    root_logger.info('Pytmosph3R PROGRAM START AT %s', start_time)
    Logger.verbose = args.verbose

    if args.debug:
        import cProfile
        pr = cProfile.Profile()
        pr.enable()
        setLogLevel(logging.DEBUG)

        import ntpath
        def path_leaf(path):
            head, tail = ntpath.split(path)
            return tail or ntpath.basename(head)

        prefix = "%s_"%args.debug
        stats_file = prefix+path_leaf(args.input_file)
        stats_file = os.path.join(args.output_folder, stats_file)
        stats_file = os.path.splitext(stats_file)[0]+".prof"

    # Parse the input file
    config = Config()
    config.search_path(args.input_file)
    config.read(config.filename)

    # Setup global parameters
    config.setup_globals()
    # Generate a model from the input
    model = config.generate_model()

    if get_rank(): # MPI "slaves" just wait for transmittance data
        model.radiative_transfer.compute(model)
        if args.debug:
            pr.disable()
            pr.create_stats()
            stats_file = os.path.splitext(stats_file)[0]+"_"+str(get_rank())+".prof"
            pr.dump_stats(stats_file)
        return

    model.build()

    os.makedirs(args.output_folder, exist_ok=True)
    h5_output = os.path.join(args.output_folder, args.h5_output)
    # Write model parameters
    if h5_output and not args.light_output:
        root_logger.info('Saving model into %s ...', h5_output)
        write_hdf5(h5_output, model)
        root_logger.info('Save - DONE')

    model.run()

    if args.spectrum_dat_output:
        spectrum_dat_output = os.path.join(args.output_folder, args.spectrum_dat_output)
        write_spectrum(spectrum_dat_output, model)

    if h5_output and not args.light_output:
        root_logger.info('Saving output into %s (verbose = %s) ...', h5_output, args.verbose)
        write_hdf5(h5_output, model, "Output")
        root_logger.info('Save - DONE')

    if args.nc_output:
        nc_output = os.path.join(args.output_folder, args.nc_output)
        root_logger.info('Creating netCDF file at %s ...', nc_output)
        write_netcdf(nc_output, model, args.radius_scale)

    end_time = datetime.datetime.now()
    root_logger.info('Pytmosph3R PROGRAM END AT %s s', end_time)
    total_time = end_time - start_time
    root_logger.info('Pytmosph3R run in %.2f s', total_time.total_seconds())

    if args.debug:
        pr.disable()
        pr.create_stats()
        root_logger.info('Recording stats in %s', stats_file)
        pr.dump_stats(stats_file)
        root_logger.info('Stats - DONE')

    if get_rank() == 0:
        from pytmosph3r.plot import Plot
        plot = Plot(model=model, out_folder=args.output_folder)
        if args.plot:
            plot.interactive = True
        plot.plot_spectrum(legend=False)
    else:
        root_logger.warning("More than 1 MPI process: no plot")

if __name__ == "__main__":
    main()
