"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose
-------
* Sample with default priors in prep for hierarchical importance sampling.

bugs
----
* Lots is hard coded that shouldn't be.

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

"""
Hard-set some prior defaults.
"""
lnamp1 = -4.6
lnamp2 = 2.3
lnperiod1 = 2.3
lnperiod2 = 9.2

def ln_likelihood(data, pars, info):
    """
    Natural log of probability of the data given the parameters.  Sort-of.
    """
    times, invvars = info
    ln_amp, ln_period, phase = pars
    models = np.exp(ln_amp) * np.cos(2. * np.pi * times / np.exp(ln_period) + phase)
    chi_squared = (data - models)**2 * invvars
    return -0.5 * np.sum(chi_squared)

def ln_prior(pars, info):
    """
    Natural log of the (hard-set) prior on parameters.  Sort-of.
    """
    ln_amp, ln_period, phase = pars
    if phase < 0.:
        return -np.Inf
    if phase > 2. * np.pi:
        return -np.Inf
    if ln_amp < lnamp1:
        return -np.Inf
    if ln_amp > lnamp2:
        return -np.Inf
    if ln_period < lnperiod1:
        return -np.Inf
    if ln_period > lnperiod2:
        return -np.Inf
    return 0.

def ln_p(pars, data, info):
    """
    The input for emcee.
    """
    lnp = ln_prior(pars, info)
    if lnp == -np.Inf:
        return lnp
    return lnp + ln_likelihood(data, pars, info)

def sample_one_set(set, prefix, plot=False):
    """
    Run MCMC on one exoplanet system.
    """
    times, sigmas, rvs = set
    info = times, 1. / (sigmas * sigmas)
    # initialize MCMC
    nwalkers = 16
    foo = np.array([np.log(1.), np.log(180.), np.pi])
    p0 = [foo + 0.001 * np.random.normal(size = foo.size) for i in range(nwalkers)]
    sampler = emcee.EnsembleSampler(nwalkers, foo.size, ln_p, args=[rvs, info])
    # burn in and run
    nsteps = 2048
    pos, lnp, state = sampler.run_mcmc(p0, nsteps)
    # save thinned chain
    thinchain = sampler.chain[:,nsteps/2::16,:] # thin by factor of 16
    fn = prefix + ".pickle"
    print "writing " + fn
    picklefile = open(fn, "wb")
    pickle.dump(thinchain, picklefile)
    picklefile.close()
    # plot
    if plot:
        plt.clf()
        for w in range(nwalkers):
            plt.plot(sampler.chain[w,:,2], '-', alpha=0.5)
            # plt.plot(sampler.lnprobability[w,:], '-', alpha=0.5)
        hogg_savefig(prefix)
    return None

def hogg_savefig(prefix):
    fn = prefix + ".png"
    print "writing " + fn
    plt.savefig(fn)
    return None

def sample_all_sets(sets, prefix):
    """
    Run MCMC on every exoplanet in the sets, and make plots and
    pickles.
    """
    pbit = True
    for i, set in enumerate(sets):
        if i > 7:
            pbit = False
        sprefix = "%s%03d_sampling" % (prefix, i)
        sample_one_set(set, sprefix, plot=pbit)
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
    np.random.seed(42)
    for prefix in ["stack", "ersatz", "blank"]:
        sets = read_pickle(prefix)
        sample_all_sets(sets, prefix)
