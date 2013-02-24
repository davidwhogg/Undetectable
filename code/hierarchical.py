"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose
-------
* Perform hierarchical inference on the samplings provided by `sample.py`.

bugs
----
* Must be massively synchronized with `sample.py`.

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
Hard-set some hyperprior defaults.  Synchronize to `sample.py`
"""
lnamp1 = -4.6
lnamp2 = 2.3
lnperiod1 = 2.3
lnperiod2 = 9.2
pars0 = np.array([lnamp1, lnamp2, lnperiod1, lnperiod2])
pars1 = 1. * pars0

def ln_likelihood(samples, pars, info):
    """
    Natural log of probability of the data given the parameters.

    This function makes **strong** assumptions about what happened in
    `sample.py`, both in terms of the format of the sampling output,
    and the prior used there (it assumes flatness in space of `pars`).

    This function does a **very dangerous** log-sum operation.
    """
    N, K, D = info
    lnampmin, lnampmax, lnperiodmin, lnperiodmax = pars
    foo= (ln_uniform(0.5 * (lnamp1 + lnamp2), lnamp1, lnamp2) +
          ln_uniform(0.5 * (lnperiod1 + lnperiod2), lnperiod1, lnperiod2))
    lnpratios = np.zeros((N, K))
    for n, sampling in enumerate(samples):
        for k, sample in enumerate(sampling):
            ln_amp, ln_period, phase = sample
            lnpratios[n, k] = (ln_uniform(ln_amp, lnampmin, lnampmax) +
                               ln_uniform(ln_period, lnperiodmin, lnperiodmax) -
                               foo)
    lnpratios = np.log(np.mean(np.exp(lnpratios), axis=1))
    print "woo hoo", pars
    return np.sum(lnpratios)

def ln_hyperprior(pars, info):
    """
    Natural log of the (hard-set) prior on parameters.
    """
    lnampmin, lnampmax, lnperiodmin, lnperiodmax = pars
    if lnampmin >= lnampmax:
        return -np.Inf
    if lnperiodmin >= lnperiodmax:
        return -np.Inf
    return (ln_uniform(lnampmin, lnamp1, lnamp2) +
            ln_uniform(lnampmax, lnamp1, lnamp2) +
            ln_uniform(lnperiodmin, lnperiod1, lnperiod2) +
            ln_uniform(lnperiodmax, lnperiod1, lnperiod2))

def ln_p(pars, samples, info):
    """
    The input for emcee.
    """
    assert pars.shape == pars0.shape
    lnp = ln_hyperprior(pars, info)
    if lnp == -np.Inf:
        return lnp
    return lnp + ln_likelihood(samples, pars, info)

def ln_uniform(x, a, b):
    """
    Natural log of uniform PDF.
    """
    if x <= a:
        return -np.Inf
    if x >= b:
        return -np.Inf
    assert a < b
    return -np.log(b - a)

def hogg_savefig(prefix):
    fn = prefix + ".png"
    print "writing " + fn
    plt.savefig(fn)
    return None

def read_pickles(prefix):
    """
    Read sets in from a pickle.
    """
    N = 512
    for n in range(N):
        picklefile = open(prefix + "%03d_sampling.pickle" % n, "r")
        sampling = pickle.load(picklefile)
        picklefile.close()
        shape = sampling.shape
        sampling = sampling.reshape((shape[0] * shape[1], shape[2]))
        if n == 0:
            sshape = (N,) + sampling.shape
            samples = np.zeros(sshape)
        samples[n] = sampling
    return samples

if __name__ == "__main__":
    # get data
    samples = read_pickles("stack")
    info = samples.shape
    # initialize MCMC
    pars = 1. * pars0
    pars[0] += 1.
    pars[1] -= 1.
    pars[2] += 1.
    pars[3] -= 1.
    nwalkers = 16
    p0 = [pars + 0.01 * np.random.normal(size = pars.size) for i in range(nwalkers)]
    sampler = emcee.EnsembleSampler(nwalkers, pars.size, ln_p, args=[samples, info], threads=nwalkers+1)
    # burn in and run
    nsteps = 512
    pos, lnp, state = sampler.run_mcmc(p0, nsteps)
    # save chain
    thinchain = sampler.chain[:,nsteps/2::1,:] # subsample by factor 1!!
    fn = "hierarchical.pickle"
    print "writing " + fn
    picklefile = open(fn, "wb")
    pickle.dump(thinchain, picklefile)
    picklefile.close()
    for d in range(pars.size):
        plt.clf()
        for w in range(nwalkers):
            plt.plot(sampler.chain[w,:,d], '-', alpha=0.5)
        hogg_savefig("hierarchical%03d" % d)
