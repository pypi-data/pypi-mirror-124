import os
import warnings
import numpy as np
from copy import deepcopy

import matplotlib
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker

from pytmosph3r.plot.plotutils import *
from pytmosph3r.emission import Emission
from pytmosph3r.constants import *
from pytmosph3r.util.geometry import *
from pytmosph3r.interface.hdf5 import HDF5Input
from pytmosph3r.util.util import get_column, get_2D, get_index, get_latitude_index, get_longitude_index, get_methods, prop
import exo_k as xk

# some global matplotlib vars
mpl.rcParams['axes.labelsize'] = 11  #set the value globally
mpl.rcParams['axes.linewidth'] = 1  #set the value globally
mpl.rcParams['text.antialiased'] = True
mpl.rcParams['errorbar.capsize'] = 2
prop_cycle = plt.rcParams['axes.prop_cycle']
prop_colors = prop_cycle.by_key()['color']

class Plot(BasePlot, LoadPlot):
    """Plot one model, either read from a HDF5 file or directly after its computation.

    Args:
        pytmosph3r_h5 (string) : HDF5 filename from which to read the model. Overrides  :py:attr:`model` if this parameter was not None.
        model (:class:`~pytmosph3r.model.model.Model`) : Model after its computation.
    """
    phi = 1.618 # Au

    def __init__(self,pytmosph3r_h5=None,title=None,label=None,
    suffix=None, out_folder='.', cmap='Paired',
    r_factor=1., h_unit=1e6, zmax=np.inf, pmin=None, substellar_longitude=None,
    interactive=False, model=None, *args, **kwargs):
        super().__init__(self, self.__class__.__name__, *args, **kwargs)
        self.h_unit = h_unit
        """Height unit scaling. By default 1e6, i.e., Mm."""
        self.zmax = zmax
        """Max altitude (in Mm) to plot."""
        self.r_factor = r_factor
        """Radius factor (for visual purposes). By default 1."""
        self._p_min = pmin
        """Min (top) pressure to plot."""
        self.substellar_longitude  = substellar_longitude
        if substellar_longitude is not None:
            self.substellar_longitude  = float(substellar_longitude)
        """Longitude of the substellar point (in degrees)."""
        self.f = None


        if pytmosph3r_h5:
            if os.path.splitext(pytmosph3r_h5)[-1] != ".h5":
                try:
                    new_path = os.path.join(pytmosph3r_h5, "output_pytmosph3r.h5")
                    if os.path.isfile(new_path):
                        pytmosph3r_h5 = new_path
                    else:
                        raise NameError
                except:
                    self.warning("Input file (%s) extension unrecognized. Not .h5?" % pytmosph3r_h5)
            # self.f = h5py.File(pytmosph3r_h5,'r')
            self.f = HDF5Input(pytmosph3r_h5)

        self._model = model
        self.interactive = interactive

        self.title = title
        self.cmap = mpl.cm.get_cmap(cmap)
        self.suffix=suffix
        if self.suffix is None:
            self.suffix = "pytmosph3r"
        self.out_folder=out_folder

        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)

        if label is None:
            if pytmosph3r_h5:
                label = path_leaf(pytmosph3r_h5)
            elif model is not None and 'filename' in model.__dict__ and model.filename:
                label = path_leaf(model.filename)
            else:
                label = "Pytmosph3R"
        self.label=label
        self.p_id = label

    def inputs(self):
        return ["pytmosph3r_h5","title","label", "suffix", "out_folder" "cmap", "r_factor", "h_unit", "zmax", "pmin", "substellar_longitude", "interactive", "model"]

    def __repr__(self) -> str:
        msg = "The inputs of "+ self.__class__.__name__ + "() are:\n %s\n"%(self.inputs())
        msg += "An exhaustive list of methods: \n "
        msg += "%s"%(get_methods(self))
        return msg

    def get_value_dim(self, index, dim):
        """Returns the value at :attr:`index` in the dimension :attr:`dim`.

        Args:
            index (int): Index of the value we're looking for.
            dim (str): Dimension of the value we're looking for. Among "altitude", "latitude" or "longitude".
        """
        if isinstance(index, (str,)):
            return index # return text as is
        unit = "°"
        if dim == "altitude":
            if isinstance(self.radiative_transfer, Emission):
                unit = 'Pa'
                array = self.pressure_levels
            else:
                unit = 'm'
                if self.h_unit == 1e6:
                    unit = 'Mm'
                elif self.h_unit == 1e3:
                    unit = 'Km'
                array = self.z
        elif dim == "latitude":
            array = np.degrees(self.grid.mid_latitudes)
        elif dim == "longitude":
            array = np.degrees(self.grid.mid_longitudes)
        else:
            self.error("I don't know dimension %s"%dim)
            return -1
        return "%.1f %s"%(array[index], unit)

    @prop
    def idx_latitude(self):
        return get_latitude_index(self.latitude, self.n_latitudes)

    @prop
    def idx_longitude(self):
        return get_longitude_index(self.longitude, self.n_longitudes)

    def legend2D(self, axes):
        if not hasattr(axes, "__len__") or len(axes.flatten()) == 1:
            return
        for ax, lat in zip(axes[:,0], self.latitudes):
            ax.annotate("Latitude:\n %s"% get_latitude_index(lat, self.n_latitudes),
                xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 10, 0), xycoords=ax.yaxis.label,
                textcoords='offset points', size='large', ha='right', va='center')
        for ax, lon in zip(axes[0], self.longitudes):
            ax.annotate("Longitude:\n %s"% get_longitude_index(lon, self.n_longitudes),
                xy=(0.5, 1), xytext=(0, 5), xycoords='axes fraction',
                textcoords='offset points', size='large', ha='center', va='baseline')

    def bin_down(self, resolution=200, spectrum=None, copy=True):
        if spectrum is None:
            spectrum = self.spectrum
        bingrid = xk.wavenumber_grid_R(spectrum.wns.min(),
                                       spectrum.wns.max(), resolution)
        if copy:
            return spectrum.bin_down_cp(bingrid)
        self.old_spectrum = deepcopy(spectrum) # save just in case
        spectrum.bin_down(bingrid)

    def savecolumn(self, label):
        return label + "_" + self.latitude + "_" + self.longitude

    @warning
    def plot_rays(self, points=True, mid_points=False, rays=False, rays_bottom=False, rays_top=True, rays_terminator=True):
        """Plot rays with matplotlib.

        Args:
            rays_bottom (bool, optional): Display the bottom layer (surface) of the planet. Defaults to False.
            rays_top (bool, optional): Display the top layer of the planet. Defaults to False.
            rays_terminator (bool, optional): Display the terminator plane. Defaults to False.
        """
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        lat, lon = np.meshgrid(self.grid.mid_latitudes, self.grid.all_longitudes)
        if rays_bottom:
            points_b = cs.sp2cart(self.R, lat, lon)
            s = ax.plot_surface(points_b[0], points_b[1], points_b[2], label="surface", alpha=.3)
            s._facecolors2d=s._facecolors3d
            s._edgecolors2d=s._edgecolors3d

        if rays_top:
            points_t = cs.sp2cart(self.r.max(), lat, lon)
            s = ax.plot_wireframe(points_t[0], points_t[1], points_t[2], label="top", alpha=.4)

        if rays_terminator:
            # terminator plane
            scale = 1
            num = 2
            A=self.rays.cartesian_system.direction.x
            B=self.rays.cartesian_system.direction.y
            C=self.rays.cartesian_system.direction.z
            if C != 0:
                x = np.linspace(-self.R*scale,self.R*scale, num)
                y = np.linspace(-self.R*scale,self.R*scale, num)
                X,Y = np.meshgrid(x,y)
                Z = -(A * X + B * Y) / C
            elif B != 0:
                x = np.linspace(-self.R*scale,self.R*scale, num)
                z = np.linspace(-self.R*scale,self.R*scale, num)
                X,Z = np.meshgrid(x,z)
                Y = -(A * X + C * Z) / B
            else:
                y = np.linspace(-self.R*scale,self.R*scale, num)
                z = np.linspace(-self.R*scale,self.R*scale, num)
                Y,Z = np.meshgrid(y,z)
                X = -(C * Z + B * Y) / A
            s = ax.plot_surface(X, Y, Z, label="terminator", alpha=.5)
            s._facecolors2d=s._facecolors3d
            s._edgecolors2d=s._edgecolors3d

        try:
            if points:
                self.plot_points(ax, self.rays.points)
            if mid_points:
                self.plot_points(ax, self.rays.mid_points)
        except:
            print("No points in output file. Try running pytmosph3r with -v")
        if rays:
            raise NotImplementedError

        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        self.save_plot("rays")

    @warning
    def plot_points(self, ax, points):
        if isinstance(points, (dict,)):
            iterator = points.items()
        elif isinstance(points, (list,)):
            iterator = enumerate(points)
            if isinstance(points[0], (list,)):
                for p_angle in points:
                    for p_radius in p_angle:
                        self.plot_points_ray(ax, p_radius)
                return
        elif isinstance(points, (np.ndarray,)):
            iterator = enumerate([points[radius,angle] for radius,angle in self.rays.walk()])

        for i, ray in iterator:
            self.plot_points_ray(ax, ray)

    @warning
    def plot_points_ray(self, ax, ray):
        if len(ray) < 1: # no points
            return

        if isinstance(ray, dict):
            points = cs.sp2cart(ray["radius"]/self.h_unit+self.R, ray["latitude"], ray["longitude"])
        else:
            points = cs.sp2cart(ray[:, 1]/self.h_unit, ray[:, 2], ray[:, 3])
        ax.plot(points[0], points[1], points[2])

    def plot_2Dmap(self, ax, location, dim, x, y, z, p_levels=[1e-4, 1, 100, 10**4], cmap="YlOrRd", log=False, vmin=None, imshow=False, *args, **kwargs):
        """Plot a 2D map at a specific location and dimension (core function). Called by :func:`map_2D`.

        Args:
            location (str, int): Name ("equator", ...) or index of location to plot
            dim (str, int): Dimension of location (altitude/latitude/longitude)
            x (ndarray): Meshgrid
            y (ndarray): Meshgrid
            z (ndarray): Values to plot
            p_levels (list, optional): Pressure levels to plot over the map. Defaults to [1e-4, 1, 100, 10**4].
            cmap (str, optional): Colormap to be used. Defaults to "YlOrRd".
            log (bool): Log scale for colors. Defaults to False.
            vmin (float): Minimum value for colorbar.
            vmax (float): Maximum value for colorbar.
            imshow (bool): If True, the map will use plt.imshow() instead of plt.contourf(). imshow() shows exactly the temperature map used, while contourf() makes it smoother. Defaults to False (i.e., contourf).
        """
        hz = get_2D(z, location, dim)
        if isinstance(hz, (float, str)):
            hz = np.full((len(x), len(y)), hz)
        if hz.ndim < 2 or hz.shape[1] == 1:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot(111)
            cs = ax.imshow(hz, aspect=".1")
            plt.colorbar(cs)
            ax.set_yticklabels(['%.2f' % i for i in y[0].tolist()])
            if dim == "latitude":
                ax.set_xlabel('East Longitude')
                ax.set_ylabel('Altitude (Mm)')
            elif dim == "longitude":
                ax.set_xlabel('Latitude')
                ax.set_ylabel('Altitude (Mm)')
            return ax
        if dim != "longitude":
            hz = np.concatenate((hz, hz[:, 0:1]), axis=1)

        if dim != "altitude":
            if p_levels is not None:
                zp = get_2D(self.pressure, location, dim)
                if dim == "latitude":
                    zp = np.concatenate((zp, zp[:, 0:1]), axis=1)
                ax.contour(x,y,zp, colors="black", linewidths=.2,
                locator=ticker.FixedLocator(p_levels),
                )

        locator = ticker.LinearLocator(100)
        formatter = None
        extend = 'neither'
        if log:
            locator = ticker.LogLocator(base=1.01,subs=(1.0,),numticks=100)
            formatter = ticker.LogFormatter(1.01, labelOnlyBase=False)
        if vmin:
            hz[np.where(hz<vmin)] = vmin
            extend = 'min'
        if imshow:
            cs = ax.imshow(hz, extent=[x.min(), x.max(), y.min(), y.max()], cmap=cmap, vmin=vmin, *args, **kwargs)
        else:
            cs = ax.contourf(x, y, hz, cmap=cmap, vmin=vmin, locator=locator, extend=extend, *args, **kwargs)
        plt.colorbar(cs, format=formatter, pad = 0.08)
        return None

    def plot_2D(self, func, dim=None, altitudes=None, latitudes=None, longitudes=None, *args, **kwargs):
        """Calls :attr:`func` on all `locations` of :attr:`dim` for a 2D plot."""
        if altitudes is not None:
            loop = altitudes
            dim = "altitude"
        elif latitudes is not None:
            loop = latitudes
            dim = "latitude"
        elif longitudes is not None:
            loop = longitudes
            dim = "longitude"
        elif dim == "altitude":
            loop = self.altitudes
        elif dim == "latitude":
            loop = self.latitudes
        elif dim == "longitude":
            loop = self.longitudes
        else:
            warnings.warn("Dimension '%s' not recognized. Should be among 'altitude', 'latitude' or 'longitude'. Not plotting 2D."% dim)
            loop = []

        for location in loop:
            func(location=location, dim=dim, *args, **kwargs)

    def map_2D(self, array, location="equator", dim="latitude", ax=None, *args, **kwargs):
        """Generic 2D map plot for a specific dimension & location. Selects the data to send to :fun:`plot_2Dmap`."""
        fig = plt.figure(figsize=(5,3.5))
        if dim == "altitude":
            ax = fig.add_subplot(111)
            longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1]+2*np.pi))
            x, y = np.degrees(np.meshgrid(longitudes, self.grid.mid_latitudes))
            ax.set_xlabel('East Longitude')
            ax.set_ylabel('Latitude')
        elif dim == "latitude":
            ax = fig.add_subplot(111, projection='polar')
            longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1]+2*np.pi))
            x, y = np.meshgrid(longitudes, self.r)
            if self.r.ndim > 1:
                x, y = np.meshgrid(longitudes, self.pressure[:, 0,0])
        elif dim == "longitude":
            ax = fig.add_subplot(111, projection='polar')
            x, y = np.meshgrid(self.grid.mid_latitudes, self.r)
            if self.r.ndim > 1:
                x, y = np.meshgrid(self.grid.mid_latitudes, self.pressure[:, 0,0])

        newax = self.plot_2Dmap(ax, location, dim, x, y, array, *args, **kwargs)
        if newax:
            ax = newax

        if dim == "longitude":
            if self.grid.mid_latitudes[0] != self.grid.mid_latitudes[-1]:
                ax.set_xlim(self.grid.mid_latitudes[0],self.grid.mid_latitudes[-1])
        elif dim == "latitude":
            try:
                ax.set_theta_zero_location("W")
                ax.set_xticklabels(["0°","45°","90°","135","180°","225°","270°","315°"], fontsize=8)
            except: # in case of 1x1 maps
                plt.tight_layout(pad=2)
        else:
            plt.tight_layout(pad=2)

        if dim != "altitude" and not newax:
            ax.set_rmin(0)
            ax.grid(linewidth=.1)
            ax.set_yticklabels(["{:,.1f}".format(x) + ' Mm' for x in [self.z_levels[0], self.z_levels[-1]]], fontsize=6)
            ax.set_rgrids([self.r.min(), self.r.max()])
            ax.set_rlabel_position(80)
            ax.tick_params(pad=0)

        return ax

    def t_map(self, location="equator", dim="latitude", ax=None, *args, **kwargs):
        """Temperature 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""
        ax = self.map_2D(self.temperature, location, dim, ax, *args, **kwargs)
        index = get_index(self.grid,location,dim)
        dim_display = dim
        if isinstance(self.radiative_transfer, Emission) and dim == "altitude":
            dim_display = "pressure"
        ax.set_title("Temperature (K) at %s %s"%(dim_display, self.get_value_dim(index, dim)))
        self.save_plot("t_map_%s_%s" % (dim, index))

    @warning
    def t_maps(self, dim="latitude", *args, **kwargs):
        """Temperature 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You should set beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"`,
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"` (default),
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """
        self.plot_2D(self.t_map, dim, *args, **kwargs)

    def x_map(self, gas=None, location="equator", dim="latitude", cmap="PuBuGn", ax=None, *args, **kwargs):
        """VMR 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""
        if isinstance(self.gas_mix_ratio[gas], str):
            total_vmr = sum([x for x in self.gas_mix_ratio.values() if not isinstance(x , str)])
            vmr = 1-total_vmr * np.ones(self.shape)
        else:
            vmr = self.gas_mix_ratio[gas] * np.ones(self.shape)
        vmin=max(np.min(vmr), 1e-16)
        if vmin > 1e-16:
            vmin = None
        ax = self.map_2D(vmr, location=location, dim=dim, ax=ax, cmap=cmap, log=True, vmin=vmin, *args, **kwargs)

        index = get_index(self.grid,location,dim)
        dim_display = dim
        if isinstance(self.radiative_transfer, Emission) and dim == "altitude":
            dim_display = "pressure"
        ax.set_title("log([%s]) at %s %s"%(gas, dim_display, self.get_value_dim(index, dim)))
        # self.zp_legend(ax, fig)
        os.makedirs(os.path.join(self.out_folder, gas), exist_ok=True)
        self.save_plot(os.path.join(gas, "x_map"), "%s_%s" % (dim, index))

    @warning
    def x_maps(self, gases=None, dim="latitude", *args, **kwargs):
        """Gas Volume Mixing ratio 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You should set beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"` (default),
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"`,
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """
        if gases is None:
            gases = self.gas_mix_ratio
        if isinstance(gases, str):
            gases = [gases]
        for gas in gases:
            self.plot_2D(self.x_map, gas=gas, dim=dim, *args, **kwargs)

    def a_map(self, aerosol=None, location="equator", dim="latitude", cmap="BuPu", ax=None, *args, **kwargs):
        """Aerosols MMRs 2D map for a specific dimension & location (calls :func:`map_2D` with identical parameters)."""
        mmr = self.aerosols[aerosol]["mmr"] * np.ones(self.shape)
        vmin=max(np.min(mmr), 1e-16)
        if vmin > 1e-16:
            vmin = None
        ax = self.map_2D(mmr, location=location, dim=dim, ax=ax, cmap=cmap, log=True, vmin=vmin, *args, **kwargs)

        index = get_index(self.grid,location,dim)
        dim_display = dim
        if isinstance(self.radiative_transfer, Emission) and dim == "altitude":
            dim_display = "pressure"
        ax.set_title("Aerosol MMR: log(%s) at %s %s"%(aerosol, dim_display, self.get_value_dim(index, dim)))
        # self.zp_legend(ax, fig)
        os.makedirs(os.path.join(self.out_folder, aerosol), exist_ok=True)
        self.save_plot(os.path.join(aerosol, "a_map"), "%s_%s" % (dim, index))

    @warning
    def a_maps(self, aerosols=None, dim="latitude", *args, **kwargs):
        """Aerosols Mass Mixing ratio 2D maps over multiple locations. See :func:`plot_2Dmap` for further parameters. You should set beforehand:

        - :attr:`self.altitudes <altitudes>` when :attr:`dim = "altitude"` (default),
        - :attr:`self.latitudes <latitudes>` when :attr:`dim = "latitude"`,
        - :attr:`self.longitudes <longitudes>` when :attr:`dim = "longitude"`
        """
        if aerosols is None:
            aerosols = self.aerosols
        if isinstance(aerosols, str):
            aerosols = [aerosols]
        for aerosol in aerosols:
            self.plot_2D(self.a_map, aerosol=aerosol, dim=dim, *args, **kwargs)

    def plot_xprofile(self, ax=None, *args, **kwargs):
        """Plot VMRs (gas mix profiles) of one vertical column."""
        save = False
        if ax is None:
            fig = plt.figure(figsize=(7,7/self.phi))
            ax = fig.add_subplot(111)
            save = True

        pressure = get_column(self.pressure, self.latitude, self.longitude)

        gas_legends = {}
        mol_idx = 0
        min_mix = 1
        max_mix = 0
        for mol_name, mix in self.gas_mix_ratio.items():
            if mix == 'background':
                others=list(self.gas_mix_ratio.values())
                others.remove('background')
                mix = 1-np.sum(others)
            if isinstance(mix, (np.ndarray)):
                max_mix = max(max_mix, mix.max())
                min_mix = min(min_mix, mix.min())
            elif not isinstance(mix, (str)):
                max_mix = max(max_mix, mix)
                min_mix = min(min_mix, mix)
            color = self.x_colors[mol_name]

            self.plot_column(ax, mix, pressure, color=color, label=mol_name, *args, **kwargs)

            gas_legends[mol_name] = mpl.lines.Line2D([0], [0], color=color, label=mol_name)
            mol_idx += 1

        plt.yscale('log')
        plt.xscale('log')
        min_mix = max(min_mix, 1e-12)
        plt.xlim(min_mix, 1)
        if self.title:
            plt.title(self.title, fontsize=14)
        if save:
            self.x_legend(ax, fig)
            self.save_plot(self.savecolumn('mixratio'))
        return gas_legends, min_mix, max_mix

    def x_legend(self, axes, fig, *args, **kwargs):
        if isinstance(axes, (np.ndarray)):
            self.legend2D(axes)
            ax = axes.flatten()[0]
            ax1 = axes.flatten()[-1]
        else:
            ax = axes
            ax1 = axes
        ax.invert_yaxis()
        plt.xlabel('Mixing ratio')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()

        h, labels = ax1.get_legend_handles_labels()
        fig.subplots_adjust(left=0.2, right=0.82, wspace=0.25, hspace=0.35)
        fig.legend(h, labels, loc='center right', bbox_to_anchor=(1, 0.5), ncol=1, prop={'size':11}, frameon=False)

    @warning
    def plot_xprofiles(self, *args, **kwargs):
        """Plot VMRs (gas mix profiles) of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""
        return self.plot_columns(self.plot_xprofile, title="mixratio", legend=self.x_legend, *args, **kwargs)

    @warning
    def plot_tp(self, ax=None, title=None):
        """Plot TP profile of one vertical column."""
        save = False
        if ax is None:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot(111)
            save = True

        ax.set_title(title)

        self.plot_column(ax, self.temperature, self.pressure)

        plt.yscale('log')
        if self.title:
            plt.title(self.title, fontsize=14)
        if save:
            self.tp_legend(ax)
            self.save_plot(self.savecolumn("tp"))

    def tp_legend(self, ax, *args, **kwargs):
        if isinstance(ax, (np.ndarray)):
            self.legend2D(ax)
            ax = ax.flatten()[0]
        ax.invert_yaxis()
        plt.xlabel('Temperature (K)')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()
        self.legend()

    @warning
    def plot_tps(self, *args, **kwargs):
        """Plot TP profiles of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""
        self.plot_columns(self.plot_tp, title="tp", legend=self.tp_legend, *args, **kwargs)

    def plot_zp(self, ax=None, title=None):
        """Plot ZP profile of one vertical column."""
        save = False
        if ax is None:
            fig = plt.figure(figsize=(5,3.5))
            ax = fig.add_subplot(111)
            save = True
        ax.set_title(title)

        self.plot_column(ax, self.pressure, self.z)

        ax.set_xscale('log')
        if save:
            self.zp_legend(ax)
            self.save_plot(self.savecolumn("zp"))

    def zp_legend(self, ax, *args, **kwargs):
        if isinstance(ax, (np.ndarray)):
            self.legend2D(ax)
            ax = ax.flatten()[0]
        ax.invert_xaxis()
        plt.ylabel('Altitude ($10^6$m)')
        plt.xlabel('Pressure (Pa)')
        plt.tight_layout()
        self.legend()

    @warning
    def plot_zps(self, *args, **kwargs):
        """Plot ZP profiles of multiple columns. Set :attr:`self.latitudes <latitudes>` and :attr:`self.longitudes <longitudes>` for this beforehand."""
        self.plot_columns(self.plot_zp, title="zp", legend=self.zp_legend, *args, **kwargs)

    @warning
    def plot_spectrum(self, ax=None, save=False, phase=None, resolution=None, ylabel=None, dashes=[], linewidth=.5, legend=True, log=False, color=None, *args, **kwargs):
        """Plot a spectrum.

        Args:
            phase (ndarray, optional): List of phases to plot (in emission mode only). BEWARE: if :attr:`substellar_longitude` has not been set, this should be the observer longitude! Defaults to None.
            resolution (int, optional): Number of points to bin to. Defaults to None.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=(5.3, 3.5))
            save = True
            ax.set_xlabel(r"$\lambda(\mu m)$")

        if self.noised_spectrum is not None:
            noise = xk.Spectrum(np.full_like(self.noised_spectrum.wns, self.noise), self.noised_spectrum.wns, self.noised_spectrum.wnedges)
            if resolution:
                spectrum = self.bin_down(resolution, self.noised_spectrum)
            else:
                spectrum = self.noised_spectrum
                below = spectrum.value-noise.value
                above = spectrum.value+noise.value
                ax.fill_between(spectrum.wls, below, above, alpha=0.4, zorder=-2, edgecolor='none', color=color)
        else:
            spectrum = self.spectrum
            if resolution:
                spectrum = self.bin_down(resolution, copy=True)

        if isinstance(phase, bool) or phase is None:
            ax.plot(spectrum.wls, spectrum.value, dashes=dashes, label=self.label, linewidth=linewidth, color=color, *args, **kwargs)
        else:
            try:
                flux = self.radiative_transfer.phase_curve
            except:
                self.warning("No phase curve to plot. If you want it, set 'phase_curve' to True.")
                return
            longitudes = np.degrees(self.radiative_transfer.observer_longitudes)
            label = "$\lambda_{obs}$"
            if self.substellar_longitude is not None:
                flux = flux[::-1]
                longitudes = np.degrees(np.pi+np.radians(self.substellar_longitude)-self.radiative_transfer.observer_longitudes)[::-1] # reversed for searching
                label = "$\phi$"
            if isinstance(phase, (float,int)):
                phase = [phase]
            for ph in phase:
                ph_index = longitudes.searchsorted(float(ph), 'left')
                ax.plot(spectrum.wls, flux[ph_index], label=r"%s = %.1f°"%(label, longitudes[ph_index]), *args, **kwargs)

        ax.set_xscale('log')
        if log:
            ax.set_yscale("log")
        # ax.set_title("Spectrum")
        if ylabel is None:
            ylabel = "$(R_p/R_s)^2$"
            if isinstance(self.radiative_transfer, Emission):
                # ylabel = "Flux $(W/m^2/%s)$"%spectrum.wn_unit
                ylabel = "Flux $(W/m^2/cm^{-1})$"
                if self.radiative_transfer.planet_to_star_flux_ratio:
                    ylabel = "$F_P/F_S$"
        ax.set_ylabel(ylabel)
        if 'title' in self.__dict__ and self.title:
            ax.set_title(self.title, fontsize=14)
        if save:
            if legend:
                ax.legend()
            plt.tight_layout()
            self.save_plot("spectrum")

    @warning
    def transmittance_map(self, wl=.6, ax=None, title="Transmittance at ", cmap="gnuplot", overlay=True, *args, **kwargs):
        """Plot transmittance at a specific wavelength :attr:`wl` (or closest inferior wavelength).
        """
        if hasattr(wl, '__len__'):
            if len(wl) > 1:
                fig = plt.figure()#figsize=(5,3.5))
                # iterate over wavelengths
                ncols = int((len(wl)+1)/2)
                nrows = int((len(wl)+1)/ncols)
                axes = []
                for i, wavelength in enumerate(wl):
                    ax = fig.add_subplot(nrows, ncols, i+1, polar=True)
                    axes.append(ax)
                    cs = self.transmittance_map(wl=float(wavelength), ax=ax, title="", cmap=cmap, *args, **kwargs)
                fig.subplots_adjust(right=1)
                clippedcolorbar(cs, format='%.3f', ax=axes)
                self.save_plot("transmittance")
                return
            wl = wl[0]

        save = False
        if ax is None:
            save = True

        wls = self.spectrum.wls[::-1]
        wl_index = len(wls) - wls.searchsorted(float(wl), 'right')
        wl_index = min(len(wls)-1, wl_index) # outside of bounds
        try:
            tr = self.transmittance[::-1, :, wl_index]
        except:
            self.warning("No transmittance to plot.")
            return

        r = self.rays.r[::-1]/self.h_unit
        z = r  - self.Rp
        r = z + self.R # divide planet radius by 2
        z_idx = np.where(z < self.zmax)
        z = z[z_idx]
        r = r[z_idx]
        tr = tr[z_idx]
        if len(self.rays.angles) != tr.shape[1]: # in case rays were not in h5 for example
            self.rays.n_radial = tr.shape[0]
            self.rays.n_angular = tr.shape[1]
            self.rays.compute_radii()
            self.rays.compute_angles()
        th = self.rays.angles

        if len(th)>1: # can actually plot a polar map
            if ax is None:
                fig = plt.figure(figsize=(5,3.5))
                ax = fig.add_subplot(111, projection='polar')
            th = np.concatenate((th, th[0:1]+2*np.pi))
            x, y = np.meshgrid(th, r)
            tr = np.concatenate((tr, tr[:, 0:1]), axis=1)
            cs = ax.contourf(x, y, tr, cmap=cmap, locator=ticker.LinearLocator(100), vmin=0, vmax=1, *args, **kwargs)
            ax.set_theta_zero_location("N")
            ax.set_rmin(0)
            ticks = [0, -1]
            if self.r_factor <1 and overlay:
                ticks = [0, int(len(z)/2),-1]
            ax.set_rgrids(r[ticks])
            ax.set_yticklabels(["{:,.1f}".format(x) + ' Mm' for x in z[ticks[:-1]]]+["0"], fontsize=8)
            ax.grid(linewidth=1)
            if overlay:
                ax.set_xticklabels(["0°","45°","90°","135","180°","225°","270°","315°"], fontsize=9)
            else:
                ax.set_xticklabels([])
            ax.set_rlabel_position(0)
        else: # Only one angle to plot, use 1D heatmap
            if ax is None:
                #
                fig = plt.figure(figsize=(5,3.5))
                ax = fig.add_subplot(111)
            x, y = np.meshgrid(th, r)
            cs = ax.imshow(tr, aspect=".2")

            ax.set_yticklabels(['%.2f' % i for i in z.tolist()])
            ax.set_ylabel("Altitude (Mm)")
            ax.set_xlabel("Azimuthal angle")

        if overlay:
            ax.set_title(r"%s%.3f $\mu m$" % (title, self.spectrum.wls[wl_index]), pad=15)
        plt.tight_layout(pad=1)
        if save:
            fig.colorbar(cs, ticks=ticker.LinearLocator(11), format='%.1f', pad=.1)
            self.save_plot("transmittance")
        return cs

    @warning
    def emission_map(self, wl=15., ax=None, title="Emission at ", cmap="gnuplot", overlay=True, figsize=(5,3.5), *args, **kwargs):
        """Plot emission at a specific wavelength :attr:`wl` (or closest inferior wavelength, in micrometer).
        """
        if hasattr(wl, '__len__'):
            if len(wl) > 1:
                fig = plt.figure()#figsize=(5,3.5))
                # iterate over wavelengths
                nrows = int((len(wl)+1)/2)
                ncols = int((len(wl)+1)/nrows)
                axes = []
                try:
                    i = self.spectrum.wls[::-1].searchsorted([float(w) for w in wl])
                    vmin = self.radiative_transfer.raw_flux[..., -i].min()
                    vmax = self.radiative_transfer.raw_flux[..., -i].max()
                except:
                    self.warning("No raw emission flux to plot. If you need it, set 'store_raw_flux' to True.")
                    return
                for i, wavelength in enumerate(wl):
                    ax = fig.add_subplot(nrows, ncols, i+1)
                    axes.append(ax)
                    cs = self.emission_map(wl=float(wavelength), ax=ax, title="", cmap=cmap, vmax=vmax, vmin=vmin, *args, **kwargs)
                fig.subplots_adjust(right=1)
                cbar = clippedcolorbar(cs, format='%.3f', ax=axes)
                self.save_plot("emission")
                return
            wl = wl[0]

        save = False
        if ax is None:
            save = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        ax.set_xlabel('East Longitude')
        ax.set_ylabel('Latitude')

        wls = self.spectrum.wls[::-1]
        wl_index = len(wls) - wls.searchsorted(float(wl), 'right')
        wl_index = min(len(wls)-1, wl_index) # outside of bounds
        try:
            flux = self.radiative_transfer.raw_flux[..., wl_index]
            flux = np.concatenate([flux, flux[:, 0:1]], axis=1)
        except:
            self.warning("No raw emission flux to plot. If you need it, set 'store_raw_flux' to True.")
            return

        longitudes = np.concatenate((self.grid.mid_longitudes, self.grid.mid_longitudes[0:1]+2*np.pi))
        x, y = np.degrees(np.meshgrid(longitudes, self.grid.mid_latitudes))
        locator=ticker.LogLocator(base=1.01,subs=(1.0,),numticks=100)
        locator=ticker.LinearLocator(100)
        cs = ax.contourf(x, y, flux, locator=locator, *args, **kwargs)

        if overlay:
            ax.set_title(r"%s%.3f $\mu m$" % (title, self.spectrum.wls[wl_index]), pad=15)
        plt.tight_layout(pad=1)
        if save:
            fig.colorbar(cs, format=ticker.LogFormatter(1.01, labelOnlyBase=False), pad=.1)
            self.save_plot("emission")
        return cs

    @warning
    def plot_phase_curve(self, wl=15, ax=None, legend=True, figsize=(5,3.5), *args, **kwargs):
        save = False
        if ax is None:
            save = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        wls = self.spectrum.wls[::-1]
        if isinstance(wl, (float,int)):
            wl = [wl]

        try:
            x = np.degrees(self.radiative_transfer.observer_longitudes)
        except:
            self.warning("No phase curve to plot. If you want it, set 'phase_curve' to True.")
            return
        if self.substellar_longitude is not None:
            x = np.degrees(np.pi+np.radians(self.substellar_longitude)-self.radiative_transfer.observer_longitudes)

        for w in wl:
            wl_index = len(wls) - wls.searchsorted(float(w), 'right')
            wl_index = min(len(wls)-1, wl_index) # outside of bounds
            flux = self.radiative_transfer.phase_curve[..., wl_index]
            if self.substellar_longitude is not None:
                flux = flux[::-1]
            ax.plot(x, flux, label=r"%.3f $\mu m$"%self.spectrum.wls[wl_index], *args, **kwargs)

        ax.set_xlabel('Observer longitude (degrees)')
        if self.substellar_longitude is not None:
            ax.set_xlabel('Phase angle (degrees)')
        ylabel = "Flux $(W/m^2/cm^{-1})$"
        if self.radiative_transfer.planet_to_star_flux_ratio:
            ylabel = "$F_P/F_S$"
        ax.set_ylabel(ylabel)

        if legend:
            ax.legend()
        plt.tight_layout(pad=1)
        if save:
            self.save_plot("phase_curve")

    @warning
    def plot_phase_curves(self, ax=None, title=None, figsize=(5,3.5), cmap="gnuplot", *args, **kwargs):
        """2D phase curves (imshow). If you want the X-axis to be in phases, you have to specify the longitude of the substellar point.

        Args:
            substellar_longitude (float, optional): Longitude (in degrees) of the substellar point. If set, the X-axis of the plot will be in phases. Defaults to None.
            figsize (tuple, optional): Size of the figure. Defaults to (5,3.5).
            cmap (str, optional): Colormap to use in the imshow(). Defaults to "gnuplot".
        """
        save = False
        if ax is None:
            save = True
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)

        try:
            flux = self.radiative_transfer.phase_curve
        except:
            self.warning("No phase curve to plot. If you want it, set 'phase_curve' to True.")
            return
        x = self.spectrum.wls
        y = np.degrees(self.radiative_transfer.observer_longitudes)
        if self.substellar_longitude is not None:
            y = np.degrees(np.pi+np.radians(self.substellar_longitude)-self.radiative_transfer.observer_longitudes)
            flux = flux[::-1]
        if x[0] > x[-1]:
            flux = flux[..., ::-1] # get increasing spectral axis for imshow
        cs = ax.imshow(flux, extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto', cmap=cmap, *args, **kwargs)

        ax.set_xlabel(r"$\lambda(\mu m)$")
        ax.set_ylabel('Observer longitude (degrees)')
        if self.substellar_longitude is not None:
            ax.set_ylabel('Phase angle (degrees)')
        if title is None:
            title = "Flux $(W/m^2/cm^{-1})$"
            if self.radiative_transfer.planet_to_star_flux_ratio:
                title = "$F_P/F_S$"
        ax.set_title(title)

        plt.tight_layout(pad=1)
        if save:
            fig.colorbar(cs)
            self.save_plot("phase_curves")

class Comparison(Plot):
    """Compare (and plot) multiple models."""
    def __init__(self, models=None,title=None,suffix=None,cmap='Paired',out_folder='.', interactive=False):
        BasePlot.__init__(self, self.__class__.__name__)
        self.models = np.array([x for x in models if x is not None])
        if len(self.models) <= 1:
            warnings.warn("No models to compare ("+str(len(models))+")")
        self.title = title
        self.interactive = interactive
        self.cmap = mpl.cm.get_cmap(cmap)
        self.suffix=suffix
        if self.suffix is None:
            self.suffix = "comp_output"
        self.out_folder=out_folder

        if not os.path.exists(self.out_folder):
            os.makedirs(self.out_folder)

    @warning
    def transmittance_map(self, ids=None, *args, **kwargs):
        if ids is None:
            ids=np.array([m.p_id for m in self.models])
        for model in filter(lambda x: x.p_id in ids, self.models):
            model.transmittance_map(*args, **kwargs)

    @warning
    def plot_spectra(self, title="Spectra", ids=None, ax=None, figsize=(4,4), legend=True, ref=None, *args, **kwargs):
        save = False
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            save = True
        if ids is None:
            ids=np.array([m.p_id for m in self.models])
        dashes=[]
        for i, model in enumerate(list(filter(lambda x: x.p_id in ids, self.models))):
            if i == ref: # plot reference curve as dashed
                dashes=[5,2]
            model.plot_spectrum(ax=ax, dashes=dashes, color=None, *args, **kwargs)
        if legend: # in case you don't need it
            ax.legend()
            ax.set_title(title)
        plt.tight_layout()
        if save:
            self.save_plot("spectra")

    def diff_spectra(self, title="Difference", ids=None, colors=None, ax=None, log=False, abs=True, resolution=None, figsize=(4,4), legend=True, ylabel=r"$\Delta (R_p/R_s)^2$", *args, **kwargs):
        """
        Compare models using ids. Example of use: comparison.diff_spectra(ids=[["3D", "1D"],["3D", "1D"]])
        """
        save = False
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
            save = True
        if ids == None:
            ids = [[m.p_id, self.models[0].p_id] for m in self.models[1:]]
        for comp in ids:
            model0 = list(filter(lambda x: comp[0] == x.p_id, self.models))
            model1 = list(filter(lambda x: comp[1] == x.p_id, self.models))
            if len(model0) and len(model1):
                model0 = model0[0]
                model1 = model1[0]
            spectrum0 = model0.spectrum
            spectrum1 = model1.spectrum
            if resolution:
                spectrum0 = model0.bin_down(resolution, copy=True)
                spectrum1 = model1.bin_down(resolution, copy=True)

            x, i0, i1 = np.intersect1d(spectrum0.wls, spectrum1.wls, return_indices=True)
            diff = 1e6 * (spectrum0.value[i0] - spectrum1.value[i1])
            if abs:
                diff = np.abs(diff)
            ax.plot(x, diff, label=model0.label+" - "+model1.label+" (%.2f ppm)"%np.mean(diff), *args, **kwargs)
        if log:
            ax.set_yscale('log')
        ax.set_xscale('log')
        # ax.set_title(title)
        ax.set_xlabel(r"$\lambda(\mu m)$")
        ax.set_ylabel(ylabel)
        #ax.grid()
        ax.legend()
        plt.tight_layout()
        if save:
            self.save_plot("diff_spectra")

    def plot_tp(self, ax=None, title="PT profile", logx=False, logy=True):
        """TP profile of one column."""
        save = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(9,3))
            save = True
        for model in self.models:
            self.plot_column(ax, model.temperature, model.pressure, label=model.label)
        if logy:
            ax.set_yscale('log')
        if logx:
            ax.set_xscale('log')
        if save:
            ax.set_title(title)
            self.tp_legend(ax)
            self.save_plot("tp")

    def plot_zp(self, ax=None, title="ZP profile", logx=True, logy=False):
        """ZP profile of one column."""
        save = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(9,3))
            save = True
        for model in self.models:
            self.plot_column(ax, model.pressure, model.z, label=model.label)
        if logy:
            ax.set_yscale('log')
        if logx:
            ax.set_xscale('log')
        # ax.legend()
        if save:
            ax.set_title(title)
            self.zp_legend(ax, fig)
            self.save_plot("zp")

    def plot_xprofile(self, ax=None, *args, **kwargs):
        """Mixing ratio. longitude = 1 plots the terminator. Outdated?"""
        save = False
        if ax is None:
            fig, ax = plt.subplots(figsize=(9,3))
            save = True
        num_models = len(self.models)
        xmin=1
        gas_legends = {}
        models = []
        for model_idx, model in enumerate(self.models):
            dashes = [(num_models-model_idx)+2, (model_idx*3)+3]

            model_gas_legend, model_min, model_max = model.plot_xprofile(ax, dashes=dashes, *args, **kwargs)

            try:
                xmin = min(model_min, xmin)
            except:
                pass
            models.append(mpl.lines.Line2D([0], [0], dashes=dashes, label=model.label))
            gas_legends.update(model_gas_legend)

        ax.set_xlim(max(1e-12,xmin))
        if save:
            self.save_plot("vmr")
        return models, gas_legends

    def x_legend(self, axes, fig, legends):
        """Place legend with model + gas labels."""
        if isinstance(axes, (np.ndarray)):
            self.legend2D(axes)
            ax = axes.flatten()[0]
        else:
            ax = axes
        ax.invert_yaxis()
        plt.xlabel('Mixing ratio')
        plt.ylabel('Pressure (Pa)')
        plt.tight_layout()

        fig.subplots_adjust(right=0.9, wspace=0.25, hspace=0.35)
        legends
        plt.gca().add_artist(fig.legend(handles=legends[0], loc=1))
        plt.gca().add_artist(fig.legend(handles=legends[1].values(), loc=4))

    def tp_legend(self, axes, fig, *args, **kwargs):
        Plot.tp_legend(self, axes, *args, **kwargs)
        self.comp_legend(axes, fig, *args, **kwargs)

    def zp_legend(self, axes, fig, *args, **kwargs):
        Plot.zp_legend(self, axes, *args, **kwargs)
        self.comp_legend(axes, fig, *args, **kwargs)

    def comp_legend(self, axes, fig, *args, **kwargs):
        """Place legend with model labels."""
        if isinstance(axes, (np.ndarray)):
            self.legend2D(axes)
            ax1 = axes.flatten()[-1]
        else:
            ax1 = axes
        plt.tight_layout()

        h, labels = ax1.get_legend_handles_labels()
        fig.legend(h, labels, loc=4)

    def legend2D(self, axes):
        """Legend for rows and columns (latitudes and longitudes) when using :func:`Plot.plot_columns`."""
        if not hasattr(axes, "__len__") or len(axes.flatten()) == 1:
            return
        for ax, lat in zip(axes[:,0], self.latitudes):
            ax.annotate("Latitude:\n %s"% lat,
                xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 10, 0), xycoords=ax.yaxis.label,
                textcoords='offset points', size='large', ha='right', va='center')
        for ax, lon in zip(axes[0], self.longitudes):
            ax.annotate("Longitude:\n %s"% lon,
                xy=(0.5, 1), xytext=(0, 5), xycoords='axes fraction',
                textcoords='offset points', size='large', ha='center', va='baseline')

    @warning
    def plot_diff_spectra(self, plots=None, compares=None, suffix="", ylabel="$(R_p/R_s)^2$", *args, **kwargs):
        """All comparison plots. longitude = 1 plots the terminator"""
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(4,5.5), gridspec_kw={'height_ratios': [3, 1]})
        self.plot_spectra(ids=plots, ax=ax[0], ylabel=ylabel, *args, **kwargs)
        self.diff_spectra(ids=compares, ax=ax[1], ylabel=r'$\Delta $'+ylabel, legend=False, *args, **kwargs)
        self.save_plot("spectra_diff"+suffix)

    @warning
    def plot_all(self, plots=None, compares=None, longitude=1):
        """All comparison plots. longitude = 1 plots the terminator"""
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(9,4))
        self.plot_spectra(ids=plots, ax=ax[0])
        self.diff_spectra(ids=compares, ax=ax[1])
        self.plot_tp(ax=ax[2])
        self.plot_x(longitude=longitude)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Pytmosph3R-Plotter')
    parser.add_argument("-i", "--input",dest='input_files',nargs='+',type=str,required=True,help="Input hdf5 file from pytmosph3r")
    parser.add_argument("-o","--output-dir",dest="output_dir",type=str,required=True,help="output directory to store plots")
    parser.add_argument("-a","--all",dest="all",default=False,action='store_true', help="Generate all (relevant) plots")
    parser.add_argument("-aa","--absolutely-all",dest="all",const=2, action='store_const', help="Plot absolutely everything (probably too much information!)")
    parser.add_argument("-x","--plot-xprofile",dest="xprofile",default=False,help="Plot molecular profiles",action='store_true')
    parser.add_argument("-aer","--aerosols",dest="aprofile",default=False,help="Plot aerosol profiles",action='store_true')
    parser.add_argument("-t","--plot-tpprofile",dest="tpprofile",default=False,help="Plot Temperature profiles",action='store_true')
    parser.add_argument("-z","--plot-zpprofile",dest="zpprofile",default=False,help="Plot Altitude-Pressure profiles",action='store_true')
    parser.add_argument("-d","--plot-tau",dest="tau",default=False,help="Plot optical depth contribution",action="store_true")
    parser.add_argument("-s","--plot-spectrum",dest="spectrum",nargs='*',default=False, help="Plot spectrum")
    parser.add_argument("-tr","--transmittance",dest="transmittance",nargs='*',default=False, help="Plot transmittance")
    parser.add_argument("-e","--emission",dest="emission",nargs='*',default=False, help="Plot emission")
    parser.add_argument("-sl","--substellar-longitude",dest="substellar_longitude", default=None, type=float, help="Define longitude of the substellar point.")
    parser.add_argument("-2D","--plot-2D",dest="plot_2D",default=False,help="Plot all 2D profiles (T, P, gases, aerosols)",action="store_true")
    parser.add_argument("-g", "--debug", dest='debug',default=False,action="store_true", help="Force to stop on fail.")
    parser.add_argument("-int","--interactive",dest="interactive",default=False,help="Interactive plot",action='store_true')
    parser.add_argument("-c","--compare",dest="compare",default=None,nargs='+',help="Override the list of models to compare in spectra difference. By default, compares every model to the first.",action='append')
    parser.add_argument("-neg","--negative",dest="negative",default=True,help="Turn off absolute value of spectra difference (to differentiate negative from positive differences).",action='store_false')

    parser.add_argument("-T","--title",dest="title",type=str,help="Title of plots")
    parser.add_argument("-sx","--suffix",dest="suffix",type=str,help="File suffix for outputs")

    parser.add_argument("-alt", "--altitudes",dest='altitudes',nargs='+',type=str,default=["surface", "top", "middle"],help="Altitudes to print")
    parser.add_argument("-lat", "--latitudes",dest='latitudes',nargs='+',type=str,default=["equator"],help="Latitudes to print")
    parser.add_argument("-lon", "--longitudes",dest='longitudes',nargs='+',type=str,default=["day", "terminator",  "night"],help="Longitudes to print")
    parser.add_argument("-m","--color-map",dest="cmap",type=str,default="Paired",help="Matplotlib colormap to use")
    parser.add_argument("-l","--labels",dest="labels",nargs='+',type=str,default=None,help="Set model name for labels")
    parser.add_argument("-R","--resolution",dest="resolution",type=float,default=None,help="Resolution to bin spectra to")
    parser.add_argument("-rad","--radius-factor",dest="r_factor",default=1., type=float ,help="Radius factor. Should be between 0 and 1 (to make atmosphere bigger).")
    parser.add_argument("-zmax","--max-altitude",dest="zmax",default=np.inf, type=float ,help="Max altitude to plot. By default, max altitude of the model.")

    parser.add_argument("-r","--rays",dest="plot_rays",default=False,help="Plot Rays",action="store_true")
    parser.add_argument("-rr","--rays-coords",dest="rays",default=False,help="Plot rays coordinates",action='store_true')
    parser.add_argument("-nrp","--no-rays-points",dest="points",default=True,help="Plot intersection points",action='store_false')
    parser.add_argument("-rm","--rays-midpoints",dest="mid_points",default=False,help="Plot mid-subray points",action='store_true')

    args=parser.parse_args()

    BasePlot.debug = args.debug
    plot_xprofile = args.xprofile or args.all
    plot_aprofile = args.aprofile or args.all
    plot_tp_profile = args.tpprofile or args.all
    plot_zp_profile = args.zpprofile or args.all
    plot_spectrum = args.spectrum or (not isinstance(args.spectrum, bool) and not len(args.spectrum)) or args.all
    transmittance = args.transmittance or (not isinstance(args.transmittance, bool) and not len(args.transmittance)) or args.all
    emission = args.emission or (not isinstance(args.emission, bool) and not len(args.emission)) or args.all
    plot_rays = args.plot_rays or (args.all == 2) or args.mid_points
    if not (plot_xprofile or plot_tp_profile or plot_zp_profile or plot_spectrum or transmittance or args.plot_2D or plot_rays):
        plot_spectrum = True # if no plot, then plot spectrum

    print("Plotting %s"%args.input_files)
    if len(args.input_files) > 1:
        # Superimpose multiple plots
        plots = []
        labels = args.labels
        if args.labels is None:
            labels = args.input_files
        for idx, file in enumerate(args.input_files):
            if args.labels is None:
                labels[idx] = os.path.splitext(file)[0]
            plot=Plot(file,cmap=args.cmap, interactive=args.interactive,
                        title=args.title,suffix=args.suffix,
                        out_folder=args.output_dir,
                        zmax=args.zmax,
                        r_factor=args.r_factor,
                        substellar_longitude=args.substellar_longitude,
                        label=labels[idx])
            plot.altitudes = args.altitudes
            plot.longitudes = args.longitudes
            plot.latitudes = args.latitudes
            plots.append(plot)

        comparison = Comparison(plots,cmap=args.cmap,
                        title=args.title,suffix=args.suffix,out_folder=args.output_dir)
        comparison.altitudes = args.altitudes
        comparison.longitudes = args.longitudes
        comparison.latitudes = args.latitudes

        if plot_spectrum:
            comparison.plot_diff_spectra(resolution=args.resolution, compares=args.compare, abs=(not args.negative))
            comparison.plot_spectra(resolution=args.resolution)
            comparison.diff_spectra(resolution=args.resolution, ids=args.compare, abs=(not args.negative))
        if plot_xprofile:
            comparison.plot_xprofiles()
        if plot_tp_profile:
            comparison.plot_tps()
        if plot_zp_profile:
            comparison.plot_zps()

        return

    if not args.interactive:
        matplotlib.use('Agg')

    file = args.input_files[0] # only one plot
    plot=Plot(file,cmap=args.cmap, interactive=args.interactive,
                    title=args.title,suffix=args.suffix,
                    out_folder=args.output_dir,
                    zmax=args.zmax,
                    r_factor=args.r_factor,
                    substellar_longitude=args.substellar_longitude,
                    )

    plot.altitudes = args.altitudes
    plot.longitudes = args.longitudes
    plot.latitudes = args.latitudes

    if plot_spectrum:
        plot.plot_spectrum(resolution=args.resolution, phase=plot_spectrum)
    if transmittance:
        if isinstance(transmittance, (bool,)) or len(transmittance) == 0:
            transmittance = 1
        plot.transmittance_map(wl=transmittance)
    if emission:
        if isinstance(emission, (bool,)) or len(emission) == 0:
            emission = 1
        plot.emission_map(wl=emission)
        plot.plot_phase_curve(wl=emission)
        plot.plot_phase_curves()
    if plot_xprofile:
        plot.plot_xprofiles()
    if plot_tp_profile:
        plot.plot_tps()
    if plot_zp_profile:
        plot.plot_zps()
    if args.plot_2D or plot_tp_profile or args.all:
        plot.t_maps()
    if args.plot_2D or plot_tp_profile or (args.all>1):
        plot.t_maps(dim="longitude")
        plot.t_maps(dim="altitude")
    if args.plot_2D or plot_xprofile or args.all:
        plot.x_maps()
    if args.plot_2D or plot_xprofile or (args.all>1):
        plot.x_maps(dim="longitude")
        plot.x_maps(dim="altitude")
    if args.plot_2D or plot_aprofile or args.all:
        plot.a_maps()
    if args.plot_2D or plot_aprofile or (args.all>1):
        plot.a_maps(dim="longitude")
        plot.a_maps(dim="altitude")
    if plot_rays:
        plot.plot_rays(points=args.points, mid_points=args.mid_points, rays=args.rays)
if __name__ == "__main__":
    main()
