"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose
-------
* Plot ersatz radial-velocity data.

"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import rc
rc('font',**{'family':'serif','size':12})
rc('text', usetex=True)
import pylab as plt
import numpy as np
import cPickle as pickle

def hogg_errorbar(x, y, yerr, **kwargs):
    """
    Plot simple error bars.
    """
    for xx, yy, yyerr in zip(x, y, yerr):
        plt.plot([xx, xx], [yy - yyerr, yy + yyerr], 'k-', **kwargs)
    return None

def hogg_lim_and_label():
    """
    Enforce identical ranges and labels.
    """
    plt.xlim(-20., 1020.)
    plt.xlabel("time (d)")
    plt.ylim(-20., 20.)
    plt.ylabel("radial velocity (km\,s$^{-1}$)")
    return None

def hogg_savefig(prefix):
    """
    Do what savefig *should* do
    """
    for fn in [prefix + ".png"]: # , prefix + ".pdf"]:
        print "saving " + fn
        plt.savefig(fn)
    return None

def read_pickle(prefix):
    picklefile = open(prefix + ".pickle", "r")
    sets = pickle.load(picklefile)
    picklefile.close()
    return sets

def plot_pickle(prefix):
    """
    Make all the plots for an ersatz data set.
    """
    sets = read_pickle(prefix)
    for i, (times, sigmas, rvs) in enumerate(sets):
        pprefix = "%s%03d" % (prefix, i)
        plt.clf()
        hogg_errorbar(times, rvs, sigmas, alpha=1.)
        plt.plot(times, rvs, 'ko', alpha=1.)
        hogg_lim_and_label()
        hogg_savefig(pprefix)
        if i == 7:
            break
    return None

def plot_stack_pickle(prefix):
    sets = read_pickle(prefix)
    pprefix = "%s_stack" % (prefix)
    plt.clf()
    for i, (times, sigmas, rvs) in enumerate(sets):
        plt.plot(times, rvs, 'ko', alpha=0.1)
    hogg_lim_and_label()
    hogg_savefig(pprefix)
    return None

def bin_stack(sets, binwidth = 10., timelim = [0., 1000.]):
    binwidth = 10.
    bincenters = np.arange(timelim[0] + 0.5 * binwidth, timelim[1], binwidth)
    binedges = np.append(bincenters - 0.5 * binwidth, bincenters[-1] + 0.5 * binwidth)
    numerator = 0.
    denominator = 0.
    for i, (times, sigmas, rvs) in enumerate(sets):
        invvars = 1. / (sigmas * sigmas)
        foo, bar = np.histogram(times, weights=invvars, bins=binedges)
        denominator += foo
        foo, bar = np.histogram(times, weights=invvars * rvs, bins=binedges)
        numerator += foo
    return bincenters, numerator / denominator, 1. / np.sqrt(denominator)

def plot_bin_stack_pickle(prefix):
    sets = read_pickle(prefix)
    xp, yp, yperr = bin_stack(sets)
    pprefix = "%s_bin_stack" % (prefix)
    plt.clf()
    hogg_errorbar(xp, yp, yperr, alpha=1.)
    plt.plot(xp, yp, 'ko', alpha=1.0)
    hogg_lim_and_label()
    hogg_savefig(pprefix)
    return None

if __name__ == "__main__":
    for prefix in ["blank", "stack", "ersatz"]:
        plot_pickle(prefix)
        plot_stack_pickle(prefix)
        plot_bin_stack_pickle(prefix)
