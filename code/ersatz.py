"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose: Make ersatz exoplanet data.
"""

import numpy as np


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

def add_stack(blanks, amp=0.25, period=187., phase=0.113):
    """
    Add the exact same exoplanet into every radial velocity curve.
    """
    result = []
    for blank in blanks:
        times, sigmas, brvs = blank
        rvs = 1. * brvs + amp * np.cos(2. * np.pi / period + phase)
        result.append((times, sigmas, rvs))
    return result

def ersatz_prior_draw():
    """
    Draw an exoplanet from a crazy, hard-set prior.
    """
    phase = 2. * np.pi * np.random.uniform()
    period = 180 + 40 * np.random.normal()
    amp = 0.25 + 0.05 * np.random.normal() 
    return amp, period, phase

def add_ersatz(blanks):
    result = []
    for blank in blanks:
        times, sigmas, brvs = blank
        amp, period, phase = ersatz_prior_draw()
        rvs = 1. * brvs + amp * np.cos(2. * np.pi / period + phase)
        result.append((times, sigmas, rvs))
    return result

def make_all(N, M):
    blanks = make_blank(N, M)
    stacks = add_stack(blanks)
    ersatzs = add_ersatz(blanks)
    return blanks, stacks, ersatzs

if __name__ == "__main__":
    np.random.seed(42)
    bs, ss, es = make_all(1000, 100)
