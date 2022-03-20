"""Determine what barbell plates are required to achieve a certain total mass.

"""

barbell_mass = 45
desired_mass = 45

class WeightInventory:
    def __init__(self, barbell_mass, dct_plates):
        """
        Args:
            barbell (float):
            dct_plates (dict):
                Example showing two 5-lb plates and four 45-lbs plates:
                {
                    '5_lbs' : 2,
                    '45_lbs' : 4,
                }
        """
        self.bb_mass = barbell
        self.dct_plates = dct_plates

    def get_ls_plate_masses(self):
        """Return a list of each plate's mass."""
        ls_plate_masses = []
        for str_mass, quant in self.dct_plates.items():
            mass = float(str_mass.rstrip('_lbs'))
            ls = [mass] * quant
            ls_plate_masses += ls
        return ls_plate_masses
        
    def get_total_mass_plates(self):
        """Return sum of plate masses."""
        return sum(self.get_ls_plate_masses())

    def get_mass_total(self):
        """Return mass of barbell + all plates."""
        return self.bb_mass + self.get_total_mass_plates()

    def show_missing_plates(self, desired_mass):
        """Print quantity and mass of plates to achieve desired mass."""
        print

def show_plates(barbell_mass, dct_plates, desired_mass):
    """Return the plates missing from dct_plates 

    Args:
        barbell_mass (float)
        desired_mass (float)

    Returns:
        list of ints: Plate values on one side of barbell.
    """
    wgtinv = WeightInventory(
        barbell_mass=barbell_mass,
        dct_plates=dct_plates,
        )
    mass_tot = wgtinv.get_mass_total()
    while current_mass != total_mass:

    return ls_wgt

if __name__ == '__main__':
    show_plates(
        barbell_mass=barbell_mass,
        dct_plates=dct_plates,
        desired_mass=desired_mass
    )
