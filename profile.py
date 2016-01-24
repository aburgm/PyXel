import numpy as np
import matplotlib.pyplot as plt
from fitting import call_model
from aux import rotate_point

class Region(object):

    def profile(self, counts_img, bkg_img, exp_img,
        min_counts, only_counts):
        """Generate count profiles.

        The box is divided into bins based on a minimum number of counts or a
        minimum S/N. The box is divided into bins starting from the bottom up,
        where the bottom is defined as the bin starting at the lowest row in
        the nonrotated box. E.g., if the box is rotated by 135 deg and it
        can be divided into three bins, then the bins will be distributed as:

                                 x
                               x   x
                             x       x
                           x    1st    x
                         x   x           x
                       x       x    bin    x
                     x    2nd    x       x
                   x   x           x   x
                 x       x    bin    x
               x    3rd    x       x
                 x           x   x
                   x    bin    x
                     x       x
                       x   x
                         x

        If a background map is not read in, then the background is set to zero.
        If an exposure map is not read in, then the exposure is set to one
        everywhere. However, if point source exclusion is important, then an
        exposure map is necessary; regions with zero exposure will be ignored,
        so they need to be masked in the exposure map. Removing point sources
        from the exposure map with dmcopy can be very slow if the full field of
        view is not included in the region file. So to quicken things up, the
        region file should look something like:

                field()
                -ellipse(......)
                -circle(......)

        The function returns a list of tuples of the form:
        (bin radius, bin width, source counts, source counts uncertainty,
        background counts, background counts uncertainty, net counts,
        net counts uncertainty)
        """

        bins = self.bin_region(counts_img, bkg_img, exp_img, min_counts)
        profile = []
        for current_bin in bins:
            src, err_src, bkg, err_bkg, net, err_net = self.get_bin_vals(
                counts_img, bkg_img, exp_img, current_bin[2], only_counts)
            profile.append((current_bin[0], current_bin[1], src, err_src, bkg,
                err_bkg, net, err_net))
        return profile

    def counts_profile(self, counts_img, bkg_img, exp_img,
        min_counts=100, only_counts=True):
        """some docstring"""
        return self.profile(counts_img, bkg_img, exp_img,
            min_counts, only_counts=True)

    def sb_profile(self, counts_img, bkg_img, exp_img,
        min_counts=100, only_counts=False):
        """some docstring"""
        return self.profile(counts_img, bkg_img, exp_img,
            min_counts, only_counts=False)

    def plot_profile(self, profile, xlog=True, ylog=True,
        xlims=None, ylims=None, xlabel=None, ylabel=None,
        with_model=False, model_name=None, model_params=None):
        """Plot profile and (optional) fitted model.

        Plots the net count profile (with error bars) and the background
        profile (step function without error bars - the uncertainties are
        difficult to get from a renormalized background image without knowing
        the normalization). The plotting can easily be done without the use of
        this routine, by just calling count_profile to get the data. This would
        allow for more customization than this routine provides.
        """
        nbins = len(profile)

        r = np.array([profile[i][0] for i in range(nbins)])
        r_err = np.array([profile[i][1] for i in range(nbins)])

        bkg = np.array([profile[i][4] for i in range(nbins)])
        net_cts = np.array([profile[i][6] for i in range(nbins)])
        err_net_cts = np.array([profile[i][7] for i in range(nbins)])

        plt.scatter(r, net_cts, c="black", alpha=0.85, s=35, marker="s")
        plt.errorbar(r, net_cts, xerr=r_err, yerr=err_net_cts,
                     linestyle="None", color="black")
        plt.step(r, bkg, where="mid", linewidth=3)

        plt.rc('text', usetex=False)
        if xlabel is not None:
            plt.xlabel(xlabel)
        if ylabel is not None:
            plt.ylabel(ylabel)

        plt.grid(True)

        if xlims is not None:
            plt.xlim([xlims[0], xlims[1]])
        else:
            plt.xlim([0.01, np.max(r + r_err)])

        if ylims is not None:
            plt.ylim([ylims[0], ylims[1]])

        if xlog:
            plt.semilogx()

        if ylog:
            plt.semilogy()

        if with_model:
            if not model_name:
                raise Exception("No model is defined.")
            else:
                model = call_model(model_name)(r, *model_params)
                plt.plot(r, model, color="r", linewidth=3, alpha=0.75)

        plt.show()
