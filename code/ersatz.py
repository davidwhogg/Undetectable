"""
This file is part of the Undetectable project.
Copyright 2013 David W. Hogg.

purpose: Make ersatz exoplanet data.
"""

import numpy as np

def make_blank(N, M, timelim=[0., 1000.], sigmalim=[1., 4.]):
    result = []
    for nn in range(N):
        times = timelim[0] + (timelim[1] - timelim[0]) * np.random.uniform(size=M).sort()
        sigmas = sigmalim[0] + (sigmalim[1] - sigmalim[0]) * np.random.uniform(size=M)
        rvs = np.zeros_like(times)
        rvs += sigmas * np.random.normal(size=M)
        result += (times, sigmas, rvs)
    return result

def add_stack(blanks):
    return 1. * blanks

def add_ersatzs(blanks):
    return 1. * blanks

def make_all(N, M):
    blanks = make_blank(N, M)
    stacks = add_stack(blanks)
    ersatzs = add_ersatz(blanks)
    return blanks, stacks, ersatzs

if __name__ == "__main__":
    bs, ss, es = make_all(10, 100)
