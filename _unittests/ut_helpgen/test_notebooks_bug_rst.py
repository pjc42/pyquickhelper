"""
@brief      test log(time=5s)
@author     Xavier Dupre
"""

import sys
import os
import unittest
import re


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

from src.pyquickhelper import fLOG, process_notebooks

if sys.version_info[0] == 2:
    from codecs import open


class TestNoteBooksBugRst(unittest.TestCase):

    def test_notebook_rst(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        fold = os.path.normpath(os.path.join(path, "notebooks_rst"))
        nbs = [os.path.join(fold, _)
               for _ in os.listdir(fold) if ".ipynb" in _]
        formats = ["rst", ]

        temp = os.path.join(path, "temp_nb_bug_rst")
        if not os.path.exists(temp):
            os.mkdir(temp)
        for file in os.listdir(temp):
            os.remove(os.path.join(temp, file))

        if "travis" in sys.executable:
            return

        res = process_notebooks(nbs, temp, temp, formats=formats)
        fLOG("*****", len(res))
        for _ in res:
            fLOG(_)
            assert os.path.exists(_[0])

        with open(os.path.join(temp, "having_a_form_in_a_notebook.rst"), "r", encoding="utf8") as f:
            content = f.read()
        exp = "<#Animated-output>`"
        if exp in content or exp.lower() not in content:
            raise Exception(content)


if __name__ == "__main__":
    unittest.main()
