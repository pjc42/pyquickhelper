"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
import re
import numpy


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.pyquickhelper import read_url, fLOG, isempty, isnan


class TestVersion (unittest.TestCase):

    def test_version(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        url = "http://www.xavierdupre.fr/enseignement/complements/marathon.txt"
        df = read_url(
            url,
            sep="\t",
            names=[
                "ville",
                "annee",
                "temps",
                "secondes"])
        assert len(df) > 0
        assert len(df.columns) == 4
        fLOG(df.head())

    def test_isnull(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        assert isempty("")
        assert not isempty("e")
        assert isempty(None)
        assert isempty(numpy.nan)

        assert isnan(numpy.nan)
        assert not isnan(0.0)

if __name__ == "__main__":
    unittest.main()
