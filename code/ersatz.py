"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose
-------
* Make ersatz exoplanet data.

bugs
----
* Half the things that should be arguments are hard-set.
* Not tested at all.

"""
import numpy as np
import cPickle as pickle

def make_blank(N, M, timelim=[0., 1000.], sigmalim=[1., 4.]):
    """
    Choose times and uncertainties and make radial velocity curves
    with zero mean and heteroskedastic Gaussian noise with known
    variances.
    """
    result = []
    for nn in range(N):
        times = timelim[0] + (timelim[1] - timelim[0]) * np.sort(np.random.uniform(size=M))
        sigmas = sigmalim[0] + (sigmalim[1] - sigmalim[0]) * np.random.uniform(size=M)
        rvs = np.zeros_like(times)
        rvs += sigmas * np.random.normal(size=M)
        result.append((times, sigmas, rvs))
    return result

def add_stack(blanks, amp=0.5, period=180., phase=0.113):
    """
    Add the exact same exoplanet into every radial velocity curve.
    """
    result = []
    for blank in blanks:
        times, sigmas, brvs = blank
        rvs = 1. * brvs + amp * np.cos(2. * np.pi * times / period + phase)
        result.append((times, sigmas, rvs))
    return result

def ersatz_prior_draw():
    """
    Draw an exoplanet from a crazy, hard-set prior.
    """
    phase = 2. * np.pi * np.random.uniform()
    period = 180. + 40. * np.random.normal()
    amp = 0.5 + 0.1 * np.random.normal() 
    return amp, period, phase

def add_ersatz(blanks):
    """
    Add a different ersatz planet ito every radial velocity curve.
    Planets are drawn from `ersatz_prior_draw()`.
    """
    result = []
    for blank in blanks:
        times, sigmas, brvs = blank
        amp, period, phase = ersatz_prior_draw()
        rvs = 1. * brvs + amp * np.cos(2. * np.pi * times / period + phase)
        result.append((times, sigmas, rvs))
    return result

def make_all(N, M):
    """
    Make all three kinds of data: "Blank" data with no signal.
    "Stack" data all with the same signal in it; these data can be
    stacked to make a discovery.  "Ersatz" data with full
    heterogeneity, so no stack will work; hierarchical inference will
    be required!
    """
    blanks = make_blank(N, M)
    stacks = add_stack(blanks)
    ersatzes = add_ersatz(blanks)
    return blanks, stacks, ersatzes

if __name__ == "__main__":
    """
    Make and pickle.
    """
    np.random.seed(42)
    bs, ss, es = make_all(1000, 100)
    for data, prefix in [(bs, "blank"),
                         (ss, "stack"),
                         (es, "ersatz")]:
        picklefile = open(prefix + ".pickle", "wb")
        pickle.dump(data, picklefile)
        picklefile.close()
