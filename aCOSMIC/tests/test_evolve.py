"""Unit test for aCOSMIC
"""

__author__ = 'Katie Breivik <katie.breivik@gmail.com>'

import os
import unittest2
import numpy as np
import pandas as pd

from aCOSMIC.evolve import Evolve
from aCOSMIC.sample import Sample

bpp_columns = ['tphys', 'mass_1', 'mass_2', 'kstar_1', 'kstar_2' , 'sep', 'ecc', 'RROL_1', 'RROL_2', 'evol_type']

TEST_DATA_DIR = os.path.join(os.path.split(__file__)[0], 'data')
BPP_ARRAY = np.load(os.path.join(TEST_DATA_DIR, 'bpp_array_ind_sampling.npy'))
INIT_CONDITIONS = np.load(os.path.join(TEST_DATA_DIR, 'init_conditions_ind_sampling.npy'))

bppDF = pd.DataFrame(BPP_ARRAY, columns=bpp_columns, index=[int(INIT_CONDITIONS[35])] * len(BPP_ARRAY))

SAMPLECLASS = Sample(0.02, size=1)
SAMPLECLASS.kstar1 = INIT_CONDITIONS[0]
SAMPLECLASS.kstar2 = INIT_CONDITIONS[1]
SAMPLECLASS.mass1_binary = INIT_CONDITIONS[2]
SAMPLECLASS.mass2_binary = INIT_CONDITIONS[3]
SAMPLECLASS.porb = INIT_CONDITIONS[4]
SAMPLECLASS.ecc = INIT_CONDITIONS[5]
SAMPLECLASS.tphysf = INIT_CONDITIONS[7]

BSEDict = {'xi': 0.5, 'bhflag': 1, 'neta': 0.5, 'windflag': 3, 'wdflag': 0, 'alpha1': 1.0, 'pts1': 0.05, 'pts3': 0.02, 'pts2': 0.01, 'epsnov': 0.001, 'hewind': 1.0, 'CK': -1000, 'bwind': 0.0, 'lambdaf': -1.0, 'mxns': 3.0, 'beta': -1.0, 'tflag': 1, 'acc2': 1.5, 'nsflag': 2, 'ceflag': 0, 'eddfac': 1.0, 'merger': 0, 'ifflag': 0, 'bconst': -3000, 'sigma': 265.0, 'gamma': -2.0}

class TestEvolve(unittest2.TestCase):
    """`TestCase` for the aCOSMIC
    """
    def test_single_evolve(self):
        # Check that the sample_primary function samples mass correctly
        evolve = Evolve(SAMPLECLASS)
        bpp, bcm = evolve.evolve(idx=INIT_CONDITIONS[35], BSEDict=BSEDict)
        pd.testing.assert_frame_equal(bpp, bppDF)
