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
        plt.plot([xx, xx], [yy - yerr, yy + yerr], '-', **kwargs)
    return None

def hogg_savefig(prefix):
    """
    Do what savefig *should* do
    """
    for fn in [prefix + ".png", prefix + ".pdf"]:
        print "saving " + fn
        plt.savefig(fn)
    return None

def plot_pickle(fn):
    """
    Make all the plots for an ersatz data set.
    """
    picklefile = open(fn, "r")
    sets = pickle.load(picklefile)
    picklefile.close()
    for i, (times, sigmas, rvs) in enumerate(sets):
        prefix = "data%03d" % i
        plt.clf()
        hogg_errorbar(times, rvs, sigmas, alpha=0.5)
        plt.plot(times, rvs, 'ko', alpha=0.5)
        hogg_savefig(prefix)
        assert False
    return None

if __name__ == "__main__":
    for prefix in ["blank", "stack", "ersatz"]:
        plot_pickle(prefix + ".pickle")
