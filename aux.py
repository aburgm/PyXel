import numpy as np

def rotate_point(x0, y0, x, y, angle):
    """Rotate point (x,y) counter-clockwise around (x0,y0)."""
    x_rot = x0 + x * np.cos(angle) - y * np.sin(angle)
    y_rot = y0 + x * np.sin(angle) + y * np.cos(angle)
    return (x_rot, y_rot)

def bin_pix2arcmin(bin_r, bin_width, src, err_src, bkg, err_bkg,
    net, err_net, npix, pix2arcmin):
    '''blah blah'''
    npix *= pix2arcmin**2 * 3600.
    bin_r = bin_r * pix2arcmin * 60.
    bin_width = bin_width * pix2arcmin * 60.
    src = src / pix2arcmin**2 / 3600.
    err_src = err_src / pix2arcmin**2 / 3600.
    bkg = bkg / pix2arcmin**2 / 3600.
    err_bkg = err_bkg / pix2arcmin**2 / 3600.
    net = net / pix2arcmin**2 / 3600.
    err_net = err_net / pix2arcmin**2 / 3600.
    return (bin_r, bin_width, src, err_src, bkg, err_bkg, net, err_net, npix)

def get_data_for_chi(profile, minrange, maxrange):
    nbins = len(profile)
    r = np.array([profile[i][0] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    w = np.array([profile[i][1] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    net = np.array([profile[i][6] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    net_err = np.array([profile[i][7] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    return nbins, r, w, net, net_err

def get_data_for_cash(profile, minrange, maxrange):
    nbins = len(profile)
    r = np.array([profile[i][0] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    src = np.array([profile[i][1] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    npix = np.array([profile[i][8] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    exp = np.array([profile[i][9] for i in range(nbins) if profile[i][0] >= minrange and profile[i][0] <= maxrange])
    return nbins, r, src, npix, exp

def call_model(func_name):
    model = getattr(model_defs, func_name)
    if not model:
        raise Exception("Model %s is not implemented." % func_name)
    else:
        return model
