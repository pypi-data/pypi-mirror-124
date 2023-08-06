#!/usr/bin/env python
from setuptools import find_packages

from numpy.distutils.core import setup, Extension
from numpy.distutils import log
import os
import glob

packages = find_packages(exclude=('tests', 'doc'))
provides = ['pytmosph3r', ]

requires = []

install_requires = ['numpy',
                    'gitpython',
                    'packaging',
                    'cython',
                    'configobj',
                    'scipy',
                    'exo_k>=1.1.1',
                    'numba>=0.49',
                    'astropy',
                    'netCDF4',
                    'h5py',
                    'psutil',
                    'ai.cs',
                    'pandas',
                    'tqdm',
                    'mpi4py',
                    ]

console_scripts = ['pytmosph3r=pytmosph3r.pytmosph3r:main',
                   'pytmosph3r-nc-to-h5=pytmosph3r.interface.nc_to_h5:nc_to_h5',
                   'pytmosph3r-h5-to-nc=pytmosph3r.interface.h5_to_nc:h5_to_nc',
                   'pytmosph3r-nc-to-nc=pytmosph3r.interface.nc_to_nc:nc_to_nc',
                   'pytmosph3r-plot=pytmosph3r.plot.plot:main [Plot]']

def build_fastchem():
    return Extension("pytmosph3r.external.fastchem",
                        sources=["pytmosph3r/external/fastchem.pyx"]+glob.glob(os.environ['FASTCHEM_DIR']+"/fastchem_src/*.cpp"),
                        extra_compile_args=["-Wall","-std=gnu++11","--fast-math","-O3","-march=native","-MMD", "-I"+os.environ['FASTCHEM_DIR']+"/fastchem_src/"],
                        language="c++")

def _have_c_compiler():
    from distutils.errors import DistutilsExecError, DistutilsModuleError, \
                             DistutilsPlatformError, CompileError
    from numpy.distutils import customized_ccompiler
    log.info('---------Detecting C compilers-------')
    try:
        c = customized_ccompiler()
        v = c.get_version()
        return True
    except (DistutilsModuleError, CompileError, AttributeError) as e:
        return False

def create_extensions():
    try:
        from Cython.Build import cythonize
    except ImportError:
        log.warn('Could not import cython,')
        log.warn('FastChem will not be installed')
        return []

    extensions = []

    if _have_c_compiler():
        log.info('Detected C compiler')
        try:
            extensions.append(build_fastchem())
            log.info('FastChem will be installed')
        except:
            log.warn('FastChem will not be installed. If you really need to install it, set FASTCHEM_DIR to its location.')
    else:
        log.warn('No suitable C compiler')
        log.warn('FastChem will not be installed')

    if len(extensions) > 0:
        extensions = cythonize(extensions, language_level=3)

    return extensions

extensions = create_extensions()

entry_points = {'console_scripts': console_scripts, }

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
    'Topic :: Scientific/Engineering :: Astronomy',
    'Topic :: Scientific/Engineering :: Atmospheric Science',
]

# Handle versioning
version = '2.1.1'

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='pytmosph3r',
      author='Aurélien Falco',
      author_email='aurelien.falco@u-bordeaux.fr',
      license="BSD",
      version=version,
      description='Pytmosph3Rn, generating transmission spectra from 3D atmospheric simulations',
      classifiers=classifiers,
      packages=packages,
      long_description=long_description,
      url='https://forge.oasu.u-bordeaux.fr/LAB/whiplash/pytmosph3r-2',
      long_description_content_type="text/markdown",
      keywords = ['exoplanet','simulation','pytmosph3r','spectra','atmosphere','atmospheric'],
      include_package_data=True,
      entry_points=entry_points,
      provides=provides,
      requires=requires,
      setup_requires=["numpy"],
      install_requires=install_requires,
      tests_require=install_requires,
      test_suite="tests",
      extras_require={
        'Plot':  ["matplotlib"], },
      ext_modules=extensions
      )
