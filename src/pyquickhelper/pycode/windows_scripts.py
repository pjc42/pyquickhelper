"""
@brief
@file Batch file use to automate some of the tasks (setup, unit tests, help, pypi).

.. versionadded:: 1.1
"""

#################
#: stop if error
#################
windows_error = "if %errorlevel% neq 0 exit /b %errorlevel%"

#################
#: prefix
#################
windows_prefix = """
echo off

if "%1"=="" goto default_value_python:
set pythonexe=%1
goto start_script:

:default_value_python:
set pythonexe=__PY34_X64__\\python
:start_script:
"""

#################
#: prefix 27
#################
windows_prefix_27 = """
echo off

if "%1"=="" goto default_value_python:
set pythonexe27=%1
goto start_script:

:default_value_python:
set pythonexe27=__PY27_X64__\\python
:start_script:
"""

#################
#: run unit test 27
#################
windows_unittest27 = """
set PYTHONPATH=
cd dist_module27\\_unittests

for /d %%d in (ut_*) do %pythonexe27%\\..\\Scripts\\nosetests.exe -w %%d
"""

#################
#: call the setup
#################
windows_setup = "%pythonexe% setup.py"
jenkins_windows_setup = "%jenkinspythonexe% setup.py"

#################
#: build script for Windows
#################
windows_build = """
echo off
IF EXIST dist del /Q dist\\*.*

if "%1"=="" goto default_value:
set pythonexe=%1
%pythonexe% setup.py write_version
goto custom_python:

:default_value:
IF NOT EXIST __PY34__ GOTO checkinstall64:

:checkinstall:
IF EXIST __PY34__vir GOTO nexta:
mkdir __PY34__vir

:nexta:
IF EXIST __PY34__vir\\install GOTO fullsetupa:
__PY34__\\Scripts\\virtualenv __PY34__vir\\install --system-site-packages
if %errorlevel% neq 0 exit /b %errorlevel%

:fullsetupa:
echo #######################################################0
__PY34__vir\\install\\Scripts\\python -u setup.py install
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################1

:checkinstall64:
IF EXIST __PY34_X64__vir GOTO nextb:
mkdir __PY34_X64__vir

:nextb:
IF EXIST __PY34_X64__vir\\install GOTO fullsetupb:
__PY34_X64__\\Scripts\\virtualenv __PY34_X64__vir\\install --system-site-packages
if %errorlevel% neq 0 exit /b %errorlevel%

:fullsetupb:
echo #######################################################2
__PY34_X64__vir\\install\\Scripts\\python -u setup.py install
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################3

:setup34:
IF NOT EXIST __PY34__ GOTO utpy34_64:
set pythonexe=__PY34__\\python
%pythonexe% setup.py write_version
%pythonexe% setup.py clean_pyd
%pythonexe% setup.py build bdist_wininst --plat-name=win-amd64
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################4

:utpy34_64:
set pythonexe=__PY34_X64__\\python
:custom_python:
echo ###----################################################5
if not exist ..\\virtual mkdir ..\\virtual
set virtual_env_py=..\\virtual\\__MODULE__
if exist %virtual_env_py% rmdir /Q /S %virtual_env_py%
mkdir %virtual_env_py%
echo %pythonexe%\\..\\Scripts\\virtualenv --system-site-packages %virtual_env_py%
if exist %virtual_env_py%\\python goto with_virtual:
%pythonexe%\\..\\Scripts\\virtualenv --system-site-packages %virtual_env_py%_vir
if %errorlevel% neq 0 exit /b %errorlevel%

:with_virtual:
set pythonexe=%virtual_env_py%_vir\\Scripts\\python
set pythonpip=%virtual_env_py%_vir\\Scripts\\pip

:requirements:
echo %pythonexe% auto_setup_dep.py install
%pythonexe% auto_setup_dep.py install

__REQUIREMENTS__

%pythonexe% setup.py write_version
echo #######################################################_clean
%pythonexe% -u setup.py clean_space
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################_unit
%pythonexe% -u setup.py unittests
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################6

%pythonexe% setup.py clean_pyd
%pythonexe% setup.py sdist --formats=gztar,zip --verbose
if %errorlevel% neq 0 exit /b %errorlevel%
%pythonexe% setup.py bdist_wininst --plat-name=win-amd64
if %errorlevel% neq 0 exit /b %errorlevel%
%pythonexe% setup.py bdist_msi
if %errorlevel% neq 0 exit /b %errorlevel%
%pythonexe% setup.py bdist_wheel
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################7

:documentation:
%pythonexe% -u setup.py build_sphinx
if %errorlevel% neq 0 exit /b %errorlevel%
echo #######################################################8

:copyfiles:
if not exist dist\\html mkdir dist\\html
xcopy /E /C /I /Y _doc\\sphinxdoc\\build\\html dist\\html
if exist _doc\\sphinxdoc\\build\\latex xcopy /E /C /I /Y _doc\\sphinxdoc\\build\\latex\\*.pdf dist\\html
if %errorlevel% neq 0 exit /b %errorlevel%

:end:
rem we copy the wheel on a local folder to let a pypiserver take it
if not exist ..\\local_pypi_server mkdir ..\\local_pypi_server
copy dist\\*.whl ..\\local_pypi_server
"""

#################
#: notebooks
#################
windows_notebook = """
if "%1"=="" goto default_value:
set pythonexe=%1
goto nextn:

:default_value:
set pythonexe=__PY34_X64__

:nextn:
set path=%path%;%pythonexe%;%pythonexe%\\Scripts
ipython3 notebook --notebook-dir=_doc\\notebooks --matplotlib=inline
"""

#################
#: publish a module
#################
windows_publish = """
%pythonexe% setup.py rotate --match=.zip --keep=1
%pythonexe% setup.py rotate --match=.tar.gz --keep=3
rem %pythonexe% setup.py sdist register
%pythonexe% setup.py sdist --formats=gztar upload
"""

#################
#: publish the documentation
#################
windows_publish_doc = """
%pythonexe% setup.py upload_docs --upload-dir=dist/html
"""

#################
#: run a pypi server
#################
windows_pypi = """
set pythonexe=__PY34_X64__

:custom_python:
if "%2"=="" goto default_port:
set portpy=%2
goto run:

:default_port:
set portpy=__PORT__

:run:
echo on
%pythonexe%\Scripts\pypi-server.exe -u -p %portpy% --disable-fallback .
"""

#################
#: script for Jenkins
#################
windows_jenkins = "set jenkinspythonexe=__PYTHON__\n" + jenkins_windows_setup + " build_script\n" + \
    windows_error + "\nauto_unittest_setup_help.bat %jenkinspythonexe%\n" + \
    windows_error

#################
#: script for Jenkins
#################
windows_jenkins_27 = "set jenkinspythonexe=__PYTHON__\n" + jenkins_windows_setup + " build_script\n" + \
    windows_error + "\nauto_setup_copy27.bat %jenkinspythonexe%\n" + windows_error + \
    "\nauto_cmd_run27.bat %jenkinspythonexe%\n" + windows_error + \
    "\nauto_cmd_build27.bat %jenkinspythonexe%\n" + windows_error

##################
#: auto setup
##################
setup_script_dependency_py = """
import sys
from distutils.core import setup, Extension
import distutils.sysconfig as SH
from setuptools import find_packages

project_var_name = "dependencies___MODULE__"
versionPython = "%s.%s" % (sys.version_info.major, sys.version_info.minor)
path = "Lib/site-packages/" + project_var_name

setup(
    name=project_var_name,
    version=versionPython,
    install_requires=[
        "numpy",
        "dateutils",
        "IPython",
        "matplotlib",
        "sphinx",
        "pandas",
        "docutils", ],
)
"""
