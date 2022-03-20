"""Determine what barbell plates are needed to achieve a certain total weight.

Date: 2022-03-19
Author: Jake Rosenzweig

NOTE:
    Didn't finish this code because, at a lovely brunch at Northwest Grille,
    Derek made the excellent point that all total weights can be achieved
    simply by making the most efficient combination of plates just shy of 
    45 lbs on one side of the barbell. Once you reach 45 lbs, you take off all
    the previous plates and put a 45-lb plate on. Thus, you have all the
    initial plates available and can begin the stacking process again.

    In this way, plate math becomes modular arithmetic (mod 45).
    
    The fewest set of plates needed to get to 42.5 lbs that I found is:
        2.5-lb plate
        5-lb plate
        5-lb plate
        10-lb plate
        25-lb plate
    
    With this set, you can make all weight combinations from 2.5 lbs to 42.5
    lbs, in intervals of 2.5 lbs.
"""
import numpy as np
from pprint import pprint
from itertools import combinations

barbell_mass = 45
desired_mass = 60

ls_tup_plates = [
    # (quantity, weight)
    (2, 2.5),
    (4, 5),
    (4, 10),
    (2, 25),
    (2, 35),
    (4, 45),
]

class WeightInventory:
    def __init__(self, barbell_mass, ls_tup_plates):
        """
        Args:
            barbell (float):
            ls_tup_plates (list):
                List of 2-tuples where each tuple is: (quantity, weight)
                Example showing two 5-lb plates and four 45-lbs plates:
                    [
                        (2, 5),
                        (4, 45),
                    ]
        """
        self.bb_mass = barbell_mass
        self.ls_tup_plates = ls_tup_plates

    def get_ls_plate_masses(self, oneside=False):
        """Return a list of masses of plates.
        
        Args:
            oneside (bool, optional):
                If True, then return the plates available to one side such
                that there will be the same number of plates on both sides.
                Example:
                    If there are four 5-lb plates total, then two plates can
                    be put on each side. Return [5, 5]
                    If there are three 5-lb plates total, then only one plate
                    can be put on each side. Return [5]
                Default is False.
        """
        ls_plate_masses = []
        for quant, mass in self.ls_tup_plates:
            if oneside:
                quant = np.floor(quant / 2)
            ls = int(quant) * [mass]
            ls_plate_masses += ls
        return ls_plate_masses
        
    def get_total_mass_plates(self):
        """Return sum of plate masses."""
        return sum(self.get_ls_plate_masses())

    def get_mass_total(self):
        """Return mass of barbell + all plates."""
        return self.bb_mass + self.get_total_mass_plates()

    def get_smallest_increment(self):
        """Return twice the smallest plate available."""
        return 2 * min(self.get_ls_plate_masses())

    def get_all_desired_masses(self, max_wgt, increm):
        """Return mass list from barbell to max_wgt in steps of increm."""
        max_wgt_include = max_wgt * 1.01
        return np.arange(self.bb_mass, max_wgt_include, increm)

    def get_n_plates_oneside(self):
        """Return the number of symmetric plates available on oneside."""
        return len(self.get_ls_plate_masses(oneside=True))

    def get_all_plate_combos_oneside(self):
        """Return set of all tuple combos of plates on one side of barbell."""
        all_combos_oneside = set()
        ls_mass_oneside = self.get_ls_plate_masses(oneside=True)
        n_plates_oneside = self.get_n_plates_oneside()
        for r in range(1, n_plates_oneside + 1):
            combos = combinations(ls_mass_oneside, r=r)
            for tup in combos:
                all_combos_oneside.add(tup)
        return all_combos_oneside

    def show_inventory(self):
        """Print info about plates, smallest increment, barbell, etc."""
        print(
            f"Barbell mass: {self.bb_mass}\n"
            f"Weight inventory:"
            )
        for quant, mass in self.ls_tup_plates:
            msg = f"  {quant} plates, each {mass} lbs"
            if quant == 1:
                msg = msg.replace("plates", "plate")
            print(msg)
        f"Smallest increment available: {self.get_smallest_increment()}"
        f" (2 * {min(self.get_ls_plate_masses())} lbs)"

    def show_missing_plates(self, desired_mass):
        """Print quantity and mass of plates to achieve desired mass."""
        self.show_inventory()
        print(
            f"Desired total mass: {desired_mass}\n"
            f"Trying to make the following weight combinations:"
            )
        increm = self.get_smallest_increment()
        all_desired_masses = self.get_all_desired_masses(desired_mass, increm)
        pprint(all_desired_masses)

        all_combos_oneside = self.get_all_plate_combos_oneside()
        print("all weight combos oneside:")
        print(all_combos_oneside)
        

if __name__ == '__main__':
    wgtinv = WeightInventory(
        barbell_mass=barbell_mass,
        ls_tup_plates=ls_tup_plates,
        )
    wgtinv.show_missing_plates(desired_mass=desired_mass)
