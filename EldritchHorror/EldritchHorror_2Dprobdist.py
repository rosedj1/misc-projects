"""
PURPOSE: This script creates PDF tables of percent chance of success
    based on rolling a certain number of dice. 
SYNTAX:  python this_script.py
NOTES:   The x-axis will have strange ticks if max_successes or 
    max_dice >= 10. 
AUTHOR: Jake Rosenzweig
CREATED: 2020-08-08
UPDATED: 2020-08-09
"""
from ROOT import TH2F, TCanvas, gStyle, gROOT, kTRUE, kGray, kBird
# n trials and k successes, where p is the probability of a success.
# binom.pmf(k, n, p) = probability mass function 
from scipy.stats import binom
#--- User Parameters ---#
outfile_path = "/Users/Jake/Programming/Projects/EldritchHorror/eldritchhorror_2Dprobdists_twokindsoftables.pdf"
max_dice = 9
color_bar_lim = [0, 100]

class HistManager:
    def __init__(self, name, title, p_success, cumul=False):
        self.name = name
        self.title = title
        self.p_success = p_success
        self.cumul = cumul

    def make_2d_hist(self, max_dice):
        self.max_dice = max_dice
        self.max_successes = max_dice
        x_label = "Number of Successes"
        y_label = "Number of Dice Thrown"
        title = r"Percent Chance of Exactly N Successes while #bf{%s}" % self.title
        if (self.cumul):
            title = title.replace("Exactly", "#geq")
        self.h2d = TH2F(self.name, 
                        "%s;%s;%s" % (title, x_label, y_label),
                        self.max_successes+1, 0, self.max_successes+1,  # x-binning.
                        self.max_dice, 1, self.max_dice+1)  # y-binning.
        
        self.pretty_up_hist()

    def pretty_up_hist(self):
        """Set other hist configurations for nice format. """
        # self.h2d.SetMarkerColor(kGray+1)
        self.h2d.SetContour(200)   # Number of color divisions.
        self.h2d.GetXaxis().SetTickSize(0)
        self.h2d.GetYaxis().SetTickSize(0)
        self.h2d.GetXaxis().CenterLabels(kTRUE)
        self.h2d.GetYaxis().CenterLabels(kTRUE)

        self.h2d.GetZaxis().SetRangeUser(*color_bar_lim)  # Change color bar limits.
        # gStyle.SetPalette(55)  # The color map. Apparently Rainbow is frowned upon. kBird is default.
        gROOT.SetBatch(kTRUE)  # Do not show plots to screen.
        gStyle.SetPaintTextFormat(r"6.4g%%")  # Pad 6 spaces, use 4 sig figs.
        gStyle.SetOptStat(0)  # Do not show hist stats.

    def fill_hist(self):
        """Fill a 2D hist with binomial probabilities with these bins:
        x-axis = successes: [0, max_successes]
        y-axis = dice thrown: [1, max_dice]
        """
        for n_dice in range(1, self.max_dice + 1):
            total_prob = 0
            for k_suc in reversed(range(self.max_successes + 1)):
                prob = binom.pmf(k_suc, n_dice, self.p_success)
                if (self.cumul):
                    # Calculate probabilities based on >= N successes.
                    total_prob += prob
                    self.h2d.Fill(k_suc, n_dice, total_prob * 100.0)
                else:
                    # Calculate probabilities based on exactly N successes.
                    self.h2d.Fill(k_suc, n_dice, prob * 100.0)

    def draw_hist(self, canv, outfile_path):
        """Draw the h2d to the active canvas and complete this page of PDF."""
        self.h2d.Draw("colz text")
        canv.Print(outfile_path)
# End class def. 

def create_histmans():
    """Create the histogram managers, one for each table to be made."""
    hist_manag_ls = [
        HistManager("HashtagBlessed", "#Blessed", p_success=3/6.0),
        HistManager("Normal", "Normal", p_success=2/6.0),
        HistManager("Cursed", "Cursed", p_success=1/6.0),
        HistManager("HashtagBlessed_cumul", "#Blessed", p_success=3/6.0, cumul=True),
        HistManager("Normal_cumul", "Normal", p_success=2/6.0, cumul=True),
        HistManager("Cursed_cumul", "Cursed", p_success=1/6.0, cumul=True),
    ]
    return hist_manag_ls

if __name__ == "__main__":
    print("Making histogram managers...")
    hist_manag_ls = create_histmans()
    print("Filling histograms...")
    for hm in hist_manag_ls:
        hm.make_2d_hist(max_dice)
        hm.fill_hist()
    print("Drawing histograms...")
    c1 = TCanvas()
    c1.Print(outfile_path + "[")
    for hm in hist_manag_ls:
        hm.draw_hist(c1, outfile_path)
    c1.Print(outfile_path + "]")