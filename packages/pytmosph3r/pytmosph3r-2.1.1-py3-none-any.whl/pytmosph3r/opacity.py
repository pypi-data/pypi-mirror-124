import exo_k as xk
import numpy as np
from pytmosph3r.log import Logger

class Opacity(Logger):
    """This module is the (main) link between pytmosph3r and exo_k. It will load the gas databases, and compute the opacities of a list of cells of the atmosphere (using their physical properties: P, T, etc).
    """

    _remove_zeros = True # for exo_k

    def __init__(self, rayleigh=None, cia=None, wn_range=None):
        super().__init__(self.__class__.__name__)
        self.rayleigh = rayleigh
        """Activate Rayleigh (by default, it is deactivated)."""
        self.wn_range = wn_range
        if hasattr(wn_range, "__len__") and not len(wn_range):
            self.wn_range = None # empty range

        """Range (wn_min, wn_max) of wave numbers to select for the computations."""
        self.cia = cia
        """List of molecules to look for when computing CIA pairs."""

    def load_gas_database(self, model):
        """Loading :class:`exo_k` gas/CIA/aerosols databases,
        and potentially clip the spectral range.
        """
        self.model = model
        self.aerosols = self.model.atmosphere.aerosols

        # check if there is a background gas
        background = False
        for gas, value in self.model.atmosphere.gas_mix_ratio.items():
            if isinstance(value, str) and value == 'background':
                background = True
        if not background:
            self.warning("No background gas given.")

        self.visible_gases = list(self.model.atmosphere.gas_mix_ratio.keys())
        transparent_gases = self.model.input_atmosphere.transparent_gases
        if isinstance(transparent_gases, str):
            self.visible_gases.remove(transparent_gases) # only one gas
        else:
            if self.model.input_atmosphere.transparent_gases is not None:
                for gas in self.model.input_atmosphere.transparent_gases:
                    try:
                        self.visible_gases.remove(gas)
                    except:
                        pass
        self.info("Exo_k: Loading gas database for %s... (%s considered transparent)"%(self.visible_gases, transparent_gases))
        self.k_data = xk.Kdatabase(self.visible_gases, remove_zeros=self._remove_zeros)

        self.cia_data = None
        if len(self.visible_gases):
            self.k_data.clip_spectral_range(self.wn_range)
            if self.cia is not None and not False and hasattr(self.cia, "__len__") and len(self.cia):
                self.info("Exo_k: Loading CIA database for %s..."%(self.cia))
                self.cia_data = xk.CIAdatabase(molecules=self.cia)
                self.cia_data.sample(wngrid=self.k_data.wns)
        self.aerosol_data = None
        if self.aerosols:
            try:
                self.info("Exo_k: Loading aerosols database for %s..."%(list(self.aerosols.keys())))
                self.aerosol_data = xk.Adatabase(filenames=[self.aerosols[a]["optical_properties"] for a in self.aerosols.keys()])
            except KeyError as e:
                try:
                    self.aerosol_data = xk.Adatabase(filenames=[self.model.aerosol(a) for a in self.aerosols.keys()])
                except:
                    for aerosol in self.aerosols.keys():
                        if "optical_properties" not in self.aerosols[aerosol].keys():
                            raise KeyError("Please provide 'optical_properties' for aerosol '%s', i.e., the name of the file in 'aerosol_path' (%s) which contains the data associated with '%s'."%(aerosol, xk.Settings()._aerosol_search_path, aerosol))
                    raise e

            self.aerosol_data.sample(wngrid=self.k_data.wns)

        self.gas_mix = xk.Gas_mix(k_database=self.k_data, cia_database=self.cia_data)

        self.info("Exo_k: loading databases - DONE")

    def compute(self, log_p, temperature, gas_vmr, aer_reff_densities, wn_range):
        """Compute the opacities for a list of cells of the atmosphere.

        Args:
            log_p (ndarray): Log10(pressure) of each cell
            temperature (ndarray): Temperature of each cell
            gas_vmr (ndarray): gas dictionary (:code:`{gas_name: VMR}`) of each cell
            aer_reff_densities (ndarray): Aerosol data of each cell (see :class:`~pytmosph3r.aerosols.PrepareAerosols`)
            wn_range (ndarray): Wavenumber range to consider
        """
        self.cross_section = self.gas_mix.cross_section(composition=gas_vmr, logp_array=log_p, t_array=temperature, rayleigh=self.rayleigh, wn_range=wn_range)

        if self.aerosols:
            self.mie_abs_coeff = self.aerosol_data.absorption_coefficient(aer_reff_densities)
            if self.k_data.Ng:
                # homogenize the shapes of mie coeff and cross sections
                self.mie_abs_coeff = self.mie_abs_coeff[..., None] * np.ones(self.k_data.Ng)
        else:
            self.mie_abs_coeff = None

        return self.cross_section, self.mie_abs_coeff

    def inputs(self):
        return ["rayleigh", "cia", "wn_range"]
    def outputs(self):
        return [''] # Opacity is usually called multiple times so an output would be useless here
