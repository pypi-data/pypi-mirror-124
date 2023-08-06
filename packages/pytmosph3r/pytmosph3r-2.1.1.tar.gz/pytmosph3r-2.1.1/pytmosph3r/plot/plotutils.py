import os
import warnings
import numpy as np
import ntpath
from functools import wraps
from pytmosph3r.log import Logger
import matplotlib.pyplot as plt
import exo_k as xk
from pytmosph3r.emission import Emission
from pytmosph3r.util.util import get_column, prop

def clippedcolorbar(CS, **kwargs):
    from matplotlib.cm import ScalarMappable
    from numpy import arange, floor, ceil
    fig = CS.ax.get_figure()
    vmin = CS.get_clim()[0]
    vmax = CS.get_clim()[1]
    m = ScalarMappable(cmap=CS.get_cmap())
    m.set_array(CS.get_array())
    m.set_clim(CS.get_clim())
    step = CS.levels[1] - CS.levels[0]
    cliplower = CS.zmin<vmin
    clipupper = CS.zmax>vmax
    noextend = 'extend' in kwargs.keys() and kwargs['extend']=='neither'
    # set the colorbar boundaries
    boundaries = arange((floor(vmin/step)-1+1*(cliplower and noextend))*step, (ceil(vmax/step)+1-1*(clipupper and noextend))*step, step)
    kwargs['boundaries'] = boundaries
    # if the z-values are outside the colorbar range, add extend marker(s)
    # This behavior can be disabled by providing extend='neither' to the function call
    if not('extend' in kwargs.keys()) or kwargs['extend'] in ['min','max']:
        extend_min = cliplower or ( 'extend' in kwargs.keys() and kwargs['extend']=='min' )
        extend_max = clipupper or ( 'extend' in kwargs.keys() and kwargs['extend']=='max' )
        if extend_min and extend_max:
            kwargs['extend'] = 'both'
        elif extend_min:
            kwargs['extend'] = 'min'
        elif extend_max:
            kwargs['extend'] = 'max'
    return fig.colorbar(m, **kwargs)

def warning(f):
    """A decorator to try if function failed and issue a warning if it did."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if BasePlot.debug:
            return f(*args, **kwargs)
        try:
            return f(*args, **kwargs)
        except Exception as e:
            warnings.warn("%s() failed with: %s"%(f.__name__, e))
    return wrapper

def path_leaf(path):
    head, tail = ntpath.split(path)
    if (tail == "output_pytmosph3r.h5" or "output_pytmosph3r.h5") and head not in (".", ""):
        return head # they all have the same name anyway
    return tail or ntpath.basename(head)

class BasePlot(Logger):
    x_colors = {'H2O': 'red', 'CO': '#BFFF00','H2': 'black',  'He': 'blue', 'TiO': 'green', 'VO': 'purple',
                'H': '#ff69b4', 'K': 'cyan', 'CH4': 'cyan', 'NH3': 'magenta', 'N2': '#faebd7',
                'PH3': '#2e8b57', 'H2S': '#eeefff', 'Fe': '#da70d6', 'FeH': '#ff7f50',
                'CrH': '#cd853f', 'Na': '#bc8f8f', 'CO2': '#5f9ea0', 'HCN': '#daa520'}
    debug = False

    def __init__(self, name, *args, **kwargs):
        """Default values for plots."""
        self.altitudes = ["surface", "middle", "top"]
        """Altitudes to plot. Possible values are indices or :attr:`surface`, :attr:`top` or :attr:`middle`."""
        self.latitudes = ["north", "equator", "south"]
        """Latitudes to plot. Possible values are indices or :attr:`north`, :attr:`south` or :attr:`equator`. :attr:`north` is latitude :attr:`0`."""
        self.latitude = "north"
        self.longitudes = ["day", "terminator", "night"]
        """Longitudes to plot. Possible values are indices or :attr:`day`, :attr:`night` or :attr:`terminator`. :attr:`night` is longitude :attr:`0`."""
        self.longitude = "day"
        super().__init__(name or self.__class__.__name__)

    """Base class for plotting."""
    def plot_columns(self, func, title="plot", legend=None, figsize=None, *args, **kwargs):
        """Iterate over vertical columns (lat,lon)."""
        nrows = len(self.latitudes)
        ncols = len(self.longitudes)
        if figsize is None:
            figsize = (3.2*(ncols+1), 3.2*(nrows))
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey=True, figsize=figsize)
        axes = np.reshape(axes, (nrows, ncols))

        for i, lat in enumerate(self.latitudes):
            for j, lon in enumerate(self.longitudes):
                self.latitude = lat
                self.longitude = lon
                results = func(ax=axes[i,j], *args, **kwargs)

        ax = fig.add_subplot(111, frame_on=False)
        plt.tick_params(labelcolor="none", bottom=False, left=False)
        if legend is not None:
            legend(axes, fig, results)
        self.save_plot(title)

    def plot_column(self, ax, x, y, *args, **kwargs):
        """Plot something at column (lat,lon)."""
        hx = get_column(x, self.latitude, self.longitude)
        hy = get_column(y, self.latitude, self.longitude)
        if isinstance(hx, (float, str)):
            hx = np.full(hy.shape, hx)
        elif isinstance(hy, (float, str)):
            hy = np.full(hx.shape, hy)
        ax.plot(hx, hy, *args, **kwargs)

    def legend(self):
        legend = plt.legend(loc='upper left', ncol=1, prop={'size':11})
        legend.get_frame().set_facecolor('white')
        legend.get_frame().set_edgecolor('white')
        legend.get_frame().set_alpha(0.8)

    def save_plot(self, name="plot", suffix=None):
        if suffix == None:
            suffix = self.suffix
        filename = os.path.join(self.out_folder, '%s_%s.pdf' % (name, suffix))
        plt.savefig(filename)
        print("Saved %s"%filename)
        if self.interactive:
            plt.show()
        else:
            plt.close('all')


class LoadPlot:
    """Class to load HDF5 file or :attr:`model` attribute. Inherited by :class:`~pytmosph3r.plot.plot.Plot`.
    """
    @prop
    def model(self):
        if not hasattr(self, "_model") or self._model is None:
            if self.f:
                self._model = self.f.read('Model')
                self._model.build()
                # self._model.atmosphere = AltitudeAtmosphere(self._model)
                self._model.atmosphere.__dict__.update(self.atmosphere.__dict__)
        return self._model
    @model.setter
    def model(self, value):
        self._model = value
    @prop
    def atmosphere(self):
        """Dict."""
        if not hasattr(self, "_atmosphere") or self._atmosphere is None:
            if self.f:
                self._atmosphere = self.f.read('Model/input_atmosphere')
                atmosphere = self.f.read('Output/atmosphere')
                try:
                    self._atmosphere.__dict__.update(atmosphere.__dict__)
                except:
                    self._atmosphere.__dict__.update(atmosphere)
            else:
                self._atmosphere = self.model.atmosphere
        return self._atmosphere
    @prop
    def radiative_transfer(self):
        """Dict."""
        if not hasattr(self, "_radiative_transfer") or self._radiative_transfer is None:
            if self.f:
                self._radiative_transfer = self.f.read('Model/radiative_transfer')
                try:
                    self._radiative_transfer.__dict__.update(self.f.read('Output/radiative_transfer'))
                except:
                    pass
            else:
                self._radiative_transfer = self.model.radiative_transfer
        return self._radiative_transfer
    @prop
    def spectrum_value_angles(self):
        return self.radiative_transfer.spectrum_value_angles
    @prop
    def spectrum(self):
        if not hasattr(self, "_spectrum") or self._spectrum is None:
            if self.f:
                value = self.f.read('Output/spectrum_value')
                wns = self.f.read('Output/wns')
                wnedges = self.f.read('Output/wnedges')
                self._spectrum = xk.Spectrum(value, wns, wnedges)
            else:
                self._spectrum = self.model.spectrum
        return self._spectrum
    @spectrum.setter
    def spectrum(self, value):
        self._spectrum = value
    @prop
    def noised_spectrum(self):
        if not hasattr(self, "_noised_spectrum") or self._noised_spectrum is None:
            if self.f:
                self._noised_spectrum = self.spectrum.copy()
                self._noised_spectrum.value = self.f.read('Output/spectrum_noised')
            else:
                self._noised_spectrum = self.model.noised_spectrum
        return self._noised_spectrum
    @prop
    def noise(self):
        """Planet radius."""
        if self.f:
            return self.f.read('Model/noise')
        else:
            return self.model.noise
    @prop
    def transmittance(self):
        if not hasattr(self, "_transmittance") or self._transmittance is None:
            try:
                self._transmittance = self.radiative_transfer.transmittance
            except:
                self._transmittance = None
        return self._transmittance
    @prop
    def grid(self):
        if not hasattr(self, "_grid") or self._grid is None:
            self._grid = self.atmosphere.grid
        return self._grid
    @prop
    def n_layers(self):
        return self.grid.n_vertical
    @prop
    def n_levels(self):
        return self.n_layers+1
    @prop
    def n_longitudes(self):
        return self.grid.n_longitudes
    @prop
    def n_latitudes(self):
        return self.grid.n_latitudes
    @prop
    def Rp(self):
        """Planet radius."""
        if self.f:
            return self.f.read('Model/planet/radius')/self.h_unit
        else:
            return self.model.planet.radius/self.h_unit
    @prop
    def R(self):
        """Planet radius scaled using :attr:`r_factor`."""
        return self.Rp * self.r_factor

    @prop
    def z_idx(self):
        if not hasattr(self, "_z_idx") or self._z_idx is None:
            try:
                if isinstance(self.radiative_transfer, Emission):
                    self._z_idx = np.where(self.pressure_levels >= self.p_min)
                else:
                    self._z_idx = np.where(self.input_z < self.z_levels.max())
                self.grid.n_vertical = len(self._z_idx[0])
            except:
                self._z_idx = slice(0,self.n_layers)
        return self._z_idx
    @prop
    def input_z(self):
        return self.atmosphere.altitude/self.h_unit
    @prop
    def input_z_levels(self):
        try:
            return self.atmosphere.altitude_levels/self.h_unit
        except:
            return self.input_z
    @prop
    def z_levels(self):
        if not hasattr(self, "_z_levels") or self._z_levels is None:
            self._z_levels = self.input_z_levels[np.where(self.input_z_levels < self.zmax)]
        return self._z_levels
    @prop
    def z(self):
        if not hasattr(self, "_z") or self._z is None:
            self._z = self.input_z[self.z_idx]
        return self._z
    @prop
    def r(self):
        return self.R + self.z
    @prop
    def rays(self):
        if not hasattr(self, "_rays") or self._rays is None:
            try:
                if self.f:
                    self._rays = self.f.read('Model/radiative_transfer/rays')
                    output_rays = self.f.read('Output/radiative_transfer/rays')
                    self._rays.__dict__.update(output_rays)
                else:
                    raise Exception
            except:
                try:
                    self._rays = self.model.radiative_transfer.rays
                except:
                    return None
            try:
                self._rays.build(self.model)
            except Exception as e:
                self.error("Could not build rays: %s"%e)
        return self._rays
    @prop
    def pressure(self):
        if not hasattr(self, "_pressure") or self._pressure is None:
            self._pressure = self.atmosphere.pressure
        return self._pressure[self.z_idx]
    @prop
    def pressure_levels(self):
        if not hasattr(self, "_pressure_levels") or self._pressure_levels is None:
            if self.f:
                self._pressure_levels = self.f.read('Model/input_atmosphere/pressure')
            else:
                self._pressure_levels = self.model.input_atmosphere.pressure
            if self._pressure_levels.ndim > 1:
                self._pressure_levels = self._pressure_levels[:,0,0]
        return self._pressure_levels
    @prop
    def p_min(self):
        if not hasattr(self, "_p_min") or self._p_min is None:
            try:
                if self.f:
                    self._p_min = self.f.read('Model/input_atmosphere/min_pressure')
                else:
                    self._p_min = self.model.input_atmosphere.min_pressure
            except:
                self._p_min = 0
        return self._p_min
    @prop
    def temperature(self):
        if not hasattr(self, "_temperature") or self._temperature is None:
            self._temperature = self.atmosphere.temperature
        return self._temperature[self.z_idx]
    @prop
    def gas_mix_ratio(self):
        if not hasattr(self, "_gas_mix_ratio") or self._gas_mix_ratio is None:
            self._gas_mix_ratio = self.atmosphere.gas_mix_ratio
            for gas, value in self._gas_mix_ratio.items():
                if not isinstance(self._gas_mix_ratio[gas], (float, str)):
                    self._gas_mix_ratio[gas] = self._gas_mix_ratio[gas][self.z_idx]
        return self._gas_mix_ratio
    @prop
    def aerosols(self):
        if not hasattr(self, "_aerosols") or self._aerosols is None:
            self._aerosols = self.atmosphere.aerosols
            for a, a_dict in self._aerosols.items():
                for key, value in a_dict.items():
                    if hasattr(self._aerosols[a][key], "__len__") and not isinstance(self._aerosols[a][key], str):
                        self._aerosols[a][key] = self._aerosols[a][key][self.z_idx]
        return self._aerosols

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    @prop
    def shape(self):
        return self.grid.shape
    @prop
    def n_levels(self):
        return self.n_layers+1