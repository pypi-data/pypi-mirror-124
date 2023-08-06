import numpy as np
from pytmosph3r.emission import Emission
import exo_k as xk

class LoadPlot:
    """Class to load HDF5 file or :attr:`model` attribute. Inherited by :class:`~pytmosph3r.plot.plot.Plot`.
    """
    @property
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
    @property
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
    @property
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
    @property
    def spectrum_value_angles(self):
        try:
            return self.radiative_transfer.spectrum_value_angles
        except:
            return None
    @property
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
    @property
    def noised_spectrum(self):
        if not hasattr(self, "_noised_spectrum") or self._noised_spectrum is None:
            try:
                if self.f:
                    self._noised_spectrum = self.spectrum.copy()
                    self._noised_spectrum.value = self.f.read('Output/spectrum_noised')
                else:
                    self._noised_spectrum = self.model.noised_spectrum
            except:
                return None
        return self._noised_spectrum
    @property
    def transmittance(self):
        if not hasattr(self, "_transmittance") or self._transmittance is None:
            try:
                self._transmittance = self.radiative_transfer.transmittance
            except:
                self._transmittance = None
        return self._transmittance
    @property
    def grid(self):
        if not hasattr(self, "_grid") or self._grid is None:
            self._grid = self.atmosphere.grid
        return self._grid
    @property
    def n_layers(self):
        return self.grid.n_vertical
    @property
    def n_levels(self):
        return self.n_layers+1
    @property
    def n_longitudes(self):
        return self.grid.n_longitudes
    @property
    def n_latitudes(self):
        return self.grid.n_latitudes
    @property
    def Rp(self):
        """Planet radius."""
        if self.f:
            return self.f.read('Model/planet/radius')/self.h_unit
        else:
            return self.model.planet.radius/self.h_unit
    @property
    def R(self):
        """Planet radius scaled using :attr:`r_factor`."""
        return self.Rp * self.r_factor

    @property
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
    @property
    def input_z(self):
        return self.atmosphere.altitude/self.h_unit
    @property
    def input_z_levels(self):
        try:
            return self.atmosphere.altitude_levels/self.h_unit
        except:
            return self.input_z
    @property
    def z_levels(self):
        if not hasattr(self, "_z_levels") or self._z_levels is None:
            self._z_levels = self.input_z_levels[np.where(self.input_z_levels < self.zmax)]
        return self._z_levels
    @property
    def z(self):
        if not hasattr(self, "_z") or self._z is None:
            self._z = self.input_z[self.z_idx]
        return self._z
    @property
    def r(self):
        return self.R + self.z
    @property
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
    @property
    def pressure(self):
        try:
            if not hasattr(self, "_pressure") or self._pressure is None:
                self._pressure = self.atmosphere.pressure
            return self._pressure[self.z_idx]
        except:
            return None
    @property
    def pressure_levels(self):
        if not hasattr(self, "_pressure_levels") or self._pressure_levels is None:
            if self.f:
                self._pressure_levels = self.f.read('Model/input_atmosphere/pressure')
            else:
                self._pressure_levels = self.model.input_atmosphere.pressure
            if self._pressure_levels.ndim > 1:
                self._pressure_levels = self._pressure_levels[:,0,0]
        return self._pressure_levels
    @property
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
    @property
    def temperature(self):
        if not hasattr(self, "_temperature") or self._temperature is None:
            self._temperature = self.atmosphere.temperature
        return self._temperature[self.z_idx]
    @property
    def gas_mix_ratio(self):
        if not hasattr(self, "_gas_mix_ratio") or self._gas_mix_ratio is None:
            self._gas_mix_ratio = self.atmosphere.gas_mix_ratio
            for gas, value in self._gas_mix_ratio.items():
                if not isinstance(self._gas_mix_ratio[gas], (float, str)):
                    self._gas_mix_ratio[gas] = self._gas_mix_ratio[gas][self.z_idx]
        return self._gas_mix_ratio
    @property
    def aerosols(self):
        if not hasattr(self, "_aerosols") or self._aerosols is None:
            self._aerosols = self.atmosphere.aerosols
            for a, a_dict in self._aerosols.items():
                for key, value in a_dict.items():
                    if not isinstance(self._aerosols[a][key], (float, str)):
                        self._aerosols[a][key] = self._aerosols[a][key][self.z_idx]
        return self._aerosols

    def close(self):
        if self.f:
            self.f.close()
            self.f = None

    @property
    def shape(self):
        return self.grid.shape
    @property
    def n_levels(self):
        return self.n_layers+1