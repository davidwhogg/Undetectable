"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose
-------
* Perform hierarchical inference on the samplings provided by `sample.py`

bugs
----
* Not yet written.

"""
import matplotlib
matplotlib.use('Agg')
from matplotlib import rc
rc('font',**{'family':'serif','size':12})
rc('text', usetex=True)
import pylab as plt
import numpy as np
import cPickle as pickle
import emcee

def ln_likelihood(samples, pars, info):
    """
    Natural log of probability of the data given the parameters.
    """
    return 0.

def ln_prior(pars, info):
    """
    Natural log of the (hard-set) prior on parameters.
    """
    return 0.

def ln_p(pars, data, info):
    """
    The input for emcee.
    """
    return 0.

def hogg_savefig(prefix):
    fn = prefix + ".png"
    print "writing " + fn
    plt.savefig(fn)
    return None

def read_pickle(prefix):
    """
    Read sets in from a pickle.
    """
    picklefile = open(prefix + ".pickle", "r")
    sets = pickle.load(picklefile)
    picklefile.close()
    return sets

if __name__ == "__main__":
    print "hello world"
