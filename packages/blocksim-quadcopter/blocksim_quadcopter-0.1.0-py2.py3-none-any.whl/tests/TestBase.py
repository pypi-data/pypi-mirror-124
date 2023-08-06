import os
import unittest
from typing import Iterable
import pathlib
from inspect import currentframe, getframeinfo

import numpy as np
from numpy import sqrt, cos, sin, exp, pi
from matplotlib import pyplot as plt

from blocksim.graphics import plotVerif
from blocksim.graphics.FigureSpec import FigureSpec
from blocksim.graphics.AxeSpec import AxeSpec


class TestBase(unittest.TestCase):
    def setUp(self):
        np.random.seed(1883647)

    def plotVerif(self, fig_title, *axes):
        fig = plotVerif(self.log, fig_title, *axes)

        if "SHOW_PLOT" in os.environ.keys():
            plt.show()

        return fig
