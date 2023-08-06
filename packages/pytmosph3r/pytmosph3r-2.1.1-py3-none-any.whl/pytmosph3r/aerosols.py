import numpy as np
from pytmosph3r.util.util import get, init_array
from exo_k.util.user_func import mmr_to_number_density
from pytmosph3r.constants import RGP

class PrepareAerosols():
    """Transform aerosols (from mmr, reff and condensate_density) to a format suitable to exo_k (reff and nb_density).
    """
    def __init__(self, model, size):
        """Initialize the aer_reff_densities to

        Args:
            model (:class:`~pytmosph3r.model.Model`): The model from which to extract some data.
            size (int): Size of the data (reff & nb_density) for each molecule.
        """
        self.model = model
        self.aer_reff_densities = {}
        """Dictionary that should be compatible with exo_k. Its keys should be the aerosol names and the values should be lists containing 2 floats (or arrays) as values. The values are the particle effective radii and number densities.  See `absorption_coefficient()`_ in the doc of exo_k:

        .. _absorption_coefficient():
        http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/adatabase/index.html?highlight=absorption_coefficient#exo_k.adatabase.Adatabase.absorption_coefficient
        """
        if model.aerosols:
            for aerosol in model.aerosols.keys():
                try:
                    key = model.aerosols[aerosol]["optical_properties"]
                except:
                    key = model.aerosol(aerosol)

                self.aer_reff_densities[key] = np.empty(2, dtype=object)
                self.aer_reff_densities[key][0] = init_array(model.aerosols[aerosol]["reff"], size)
                self.aer_reff_densities[key][1] = np.full((size), np.nan)

    def compute(self, i, coordinates):
        """Compute the value of aer_reff_densities at `coordinates`, which will be stored at index `i`.
        The input `aerosols` dictionary should contain a MMR `mmr` (in `kg/kg`), and effective radius `reff` (in `m`), and `condensate_density (in kg/m^3).

        Args:
            i (int):
            coordinates (tuple):

        Returns:
            dict: A dictionary with aerosol names as keys and lists containing 2 floats (or arrays) as values. The values are the particle effective radii and number densities.
        """
        gas_density = self.model.molar_mass[coordinates] * self.model.pressure[coordinates] / (RGP * self.model.temperature[coordinates])
        for aerosol in self.model.aerosols.keys():
            try:
                key = self.model.aerosols[aerosol]["optical_properties"]
            except:
                key = self.model.aerosol(aerosol)

            mmr = get(self.model.aerosols[aerosol]['mmr'], coordinates)
            reff = get(self.model.aerosols[aerosol]['reff'], coordinates)
            condensate_density = get(self.model.aerosols[aerosol]['condensate_density'], coordinates)
            nb_density = mmr_to_number_density(mmr, gas_density, reff, condensate_density)

            if isinstance(self.aer_reff_densities[key][0], np.ndarray):
                self.aer_reff_densities[key][0][i] = reff
            self.aer_reff_densities[key][1][i] = nb_density
        return self.aer_reff_densities