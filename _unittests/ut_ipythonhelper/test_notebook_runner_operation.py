"""
@brief      test log(time=5s)
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

from src.pyquickhelper.ipythonhelper import read_nb
from src.pyquickhelper import get_temp_folder, fLOG


class TestNotebookRunnerOperation (unittest.TestCase):

    def test_notebook_runner_operation(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        temp = get_temp_folder(__file__, "temp_notebook_operation")

        nbfile = os.path.join(temp, "..", "data", "simple_example.ipynb")
        nbfile2 = os.path.join(
            temp, "..", "data", "td2a_cenonce_session_4B.ipynb")
        nb1 = read_nb(nbfile)
        n1 = len(nb1)
        nb2 = read_nb(nbfile2)
        n2 = len(nb2)
        add = nb1 + nb2
        nb1.merge_notebook([nb2])
        n3a = len(add)
        n3 = len(nb1)
        if n1 + n2 != n3:
            raise Exception("{0} + {1} != {2}".format(n1, n2, n3))
        if n3a != n3:
            raise Exception("{0} != {1}".format(n3a, n3))

        fLOG(n1, n2, n3, n3a)
        outfile = os.path.join(temp, "merge_nb.ipynb")
        nb1.to_json(outfile)
        assert os.path.exists(outfile)
        outfile = os.path.join(temp, "merge_nb_add.ipynb")
        add.to_json(outfile)
        assert os.path.exists(outfile)


if __name__ == "__main__":
    unittest.main()
