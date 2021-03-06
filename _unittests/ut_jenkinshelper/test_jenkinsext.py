"""
@brief      test log(time=2s)
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

from src.pyquickhelper import fLOG
from src.pyquickhelper.jenkinshelper.jenkins_server import JenkinsExt, JenkinsExtException


class TestJenkinsExt(unittest.TestCase):

    def test_jenkins_ext(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        srv = JenkinsExt(
            "http://localhost:8080/", "user", "password", mock=True)
        github = "https://github.com/sdpython/"

        if not sys.platform.startswith("win"):
            # not yet implemented
            return

        conf = srv.create_job_template("pyquickhelper",
                                       git_repo=github +
                                       "%s/" % "pyquickhelper",
                                       upstreams=None,
                                       location=r"/home/username/jenkins/",
                                       dependencies={
                                           "myversion": "/home/username/mymodule/src/", },
                                       platform="win32")
        assert "MYVERSION=/home/username/mymodule/src/" in conf
        assert "auto_unittest_setup_help.bat" in conf

        conf = srv.create_job_template("pyquickhelper",
                                       git_repo=github +
                                       "%s/" % "pyquickhelper",
                                       upstreams=None,
                                       location=r"/home/username/jenkins/",
                                       dependencies={
                                           "myversion": "/home/username/mymodule/src/", },
                                       scheduler="H H(13-14) * * *",
                                       platform="win32")
        assert "H H(13-14) * * *" in conf

        try:
            conf = srv.create_job_template("pyquickhelper",
                                           git_repo=github +
                                           "%s/" % "pyquickhelper",
                                           upstreams=["pyquickhelper"],
                                           location=r"/home/username/jenkins/",
                                           dependencies={
                                               "myversion": "/home/username/mymodule/src/", },
                                           scheduler="H H(13-14) * * *",
                                           platform="win32")
            raise Exception("should not happen")
        except JenkinsExtException:
            pass

        conf = srv.create_job_template("pyquickhelper",
                                       git_repo=github +
                                       "%s/" % "pyquickhelper",
                                       upstreams=["pyquickhelper"],
                                       location=r"/home/username/jenkins/",
                                       dependencies={
                                           "myversion": "/home/username/mymodule/src/", },
                                       scheduler=None,
                                       platform="win32")
        assert "pyquickhelper" in conf

    def test_jenkins_ext_setup_server(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        srv = JenkinsExt(
            "http://localhost:8080/", "user", "password", mock=True)

        github = "https://github.com/sdpython/"

        if sys.platform.startswith("win"):
            modules = [  # update anaconda
                ("standalone [conda_update]", "H H(8-9) * * 0"),
                "standalone [conda_update27]",
                "standalone [local_pypi]",
                # pyquickhelper,
                ("pyquickhelper", "H H(10-11) * * 0"),
                ("pymyinstall", None, dict(success_only=True)),
                ["pyquickhelper [anaconda]", "pyquickhelper [winpython]",
                 "pyquickhelper [27] [anaconda2]"],
                ["pyensae", ],
                ["pymmails", "pysqllike", "pyrsslocal", "pymyinstall [27] [anaconda2]",
                 "python3_module_template", "pyensae [anaconda]", "pyensae [winpython]"],
                ["pymmails [anaconda]", "pysqllike [anaconda]", "pyrsslocal [anaconda]",
                 "python3_module_template [anaconda]",
                 "python3_module_template [27] [anaconda2]",
                 "pymyinstall [LONG]"],
                # actuariat
                [("actuariat_python", "H H(12-13) * * 0")],
                ["actuariat_python [winpython]",
                 "actuariat_python [anaconda]"],
                # code_beatrix
                ("code_beatrix", "H H(14-15) * * 0"),
                "code_beatrix [winpython]",
                "code_beatrix [anaconda]",
                # teachings
                ("ensae_teaching_cs", "H H(15-16) * * 0"),
                ["ensae_teaching_cs [winpython]",
                 "ensae_teaching_cs [anaconda]"],
                "ensae_teaching_cs [custom_left]",
                "ensae_teaching_cs [winpython] [custom_left]",
                "ensae_teaching_cs [anaconda] [custom_left]",
                # documentation
                ("pyquickhelper [doc]", "H H(3-4) * * 1"),
                ["pymyinstall [doc]", "pysqllike [doc]", "pymmails [doc]",
                 "pyrsslocal [doc]", "pyensae [doc]"],
                ["actuariat_python [doc]", "code_beatrix [doc]"],
                ("ensae_teachings_cs [doc]", None,
                 dict(pre="rem pre", post="rem post")),
                ("custom [any_name]", "H H(3-4) * * 1",
                 dict(script="any_script.bat")),
            ]
        else:
            modules = [  # update anaconda
                ("standalone [conda_update]", "H H(8-9) * * 0"),
                "standalone [conda_update27]",
                "standalone [local_pypi]",
                # pyquickhelper,
                ("pyquickhelper", "H H(10-11) * * 0"),
                ("pymyinstall", None, dict(success_only=True)),
                ["pyquickhelper [anaconda]", "pyquickhelper [winpython]",
                 "pyquickhelper [27] [anaconda2]"],
                ["pyensae", ],
                ["pymmails", "pysqllike", "pyrsslocal", "pymyinstall [27] [anaconda2]",
                 "python3_module_template", "pyensae [anaconda]"],
                ["pymmails [anaconda]", "pysqllike [anaconda]", "pyrsslocal [anaconda]",
                 "python3_module_template [anaconda]",
                 "python3_module_template [27] [anaconda2]",
                 "pymyinstall [LONG]"],
                # actuariat
                [("actuariat_python", "H H(12-13) * * 0")],
                ["actuariat_python [anaconda]"],
                # code_beatrix
                ("code_beatrix", "H H(14-15) * * 0"),
                ["code_beatrix [anaconda]"],
                # teachings
                ("ensae_teaching_cs", "H H(15-16) * * 0"),
                ["ensae_teaching_cs [anaconda]"],
                "ensae_teaching_cs [custom_left]",
                ["ensae_teaching_cs [anaconda] [custom_left]", ],
                # documentation
                ("pyquickhelper [doc]", "H H(3-4) * * 1"),
                ["pymyinstall [doc]", "pysqllike [doc]", "pymmails [doc]",
                 "pyrsslocal [doc]", "pyensae [doc]"],
                ["actuariat_python [doc]", "code_beatrix [doc]"],
                "ensae_teachings_cs [doc]",
            ]

        pythonexe = os.path.dirname(sys.executable)
        location = None
        dependencies = {'pymyinstall': ['pyquickhelper'],
                        'pyensae': ['pyquickhelper'],
                        'python3_module_template': ['pyquickhelper'],
                        'ensae_teaching_cs': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                        'actuariat_python': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                        'code_beatrix': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                        }

        if not sys.platform.startswith("win"):
            # not yet implemented
            return

        res = srv.setup_jenkins_server(github=github, modules=modules, pythonexe=pythonexe,
                                       overwrite=True,
                                       fLOG=fLOG, dependencies=dependencies,
                                       location="anything/")
        df_ = 0
        reg = re.compile("<description>(.*)</description>")
        for i, r in enumerate(res):
            conf = r[-1]

            if "DF_" in conf:
                df_ += 1

            if not conf.startswith("<?xml version='1.0' encoding='UTF-8'?>"):
                raise Exception(conf)

            search = reg.search(conf)
            if not search:
                raise Exception(conf)

            fLOG(search.groups()[0], r[0], r[1])

            if "__" in conf and "pyquickhelper_vir" not in conf:
                raise Exception(conf)
            if "notebook" in conf:
                raise Exception(conf)

            if "pymyinstall" in r[0] and "[" not in r[0]:
                if "FAILURE" in conf:
                    raise Exception(conf)
                if "SUCCESS" not in conf:
                    raise Exception(conf)

            if i == 0:
                if "conda update" not in conf:
                    raise Exception(conf)
                if "H H(8-9) * * 0" not in conf:
                    raise Exception(conf)
                if "A0101" not in conf:
                    raise Exception(conf)
                if "github" in conf:
                    raise Exception(conf)

            if i == 3:
                if "pyquickhelper" not in conf:
                    raise Exception(conf)
                if "H H(10-11) * * 0" not in conf:
                    raise Exception(conf)
                if "B0101" not in conf:
                    raise Exception(conf)
                if "github" not in conf:
                    raise Exception(conf)

            if "python3_module_template [27]" in r[0]:
                if "PYQUICKHELPER27=" not in conf:
                    raise Exception(conf)
                if "PYQUICKHELPER=" not in conf:
                    raise Exception(conf)
                if "PYQUICKHELPER27=a" not in conf:
                    raise Exception(conf)
                if "dist_module27" not in conf:
                    raise Exception(conf)
                if "Anaconda3" in conf:
                    raise Exception(conf)

            if "[27]" not in r[0] and "update" not in conf:
                if "PYQUICKHELPER27=a" in conf:
                    raise Exception(conf)
                if "dist_module27" in conf:
                    raise Exception(conf)

            if "_LONG" in conf and "build_script" not in conf:
                raise Exception(conf)

            if "custom_left" in conf:
                if "auto_cmd_any_setup_command.bat custom_left" not in conf:
                    raise Exception(conf)

            if ">F0" in conf:
                if "auto_cmd_any_setup_command.bat build_sphinx" not in conf:
                    raise Exception(conf)

            if "ensae_teachings_cs [doc]" in conf:
                if "rem pre" not in conf or "rem post" not in conf:
                    raise Exception(conf)

        assert i > 0
        assert df_ > 0


if __name__ == "__main__":
    unittest.main()
