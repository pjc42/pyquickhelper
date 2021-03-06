
.. _l-moreinstall:

Installation
============


* Using pip::

    pip install pyquickhelper

* Windows installation:
    * download ``pyquickhelper*.whl``
    * run ``pip install pyquickhelper*.whl``
* Windows installation with source:
    * download the file ``pyquickhelper*.tar.gz`` and unzip it
    * type the following commands::

        python setup.py install

* Linux installation:
    * download the file ``pyquickhelper*.tar.gz``
    * type the following commands::

        tar xf pyquickhelper*.tar.gz
        sudo su
        python3.4 setup.py install

If you install on `WinPython <https://winpython.github.io/>`_ distribution,
you might need to add ``--pre`` to force the installation::

    pip install pyquickhelper --pre
    
The version for Python 2.7 is not available through pypi
but it can be installed from `Python Extensions <http://www.xavierdupre.fr/site2013/index_code.html>`_
which indicates the latest available version for this platform::

    pip install http://www.xavierdupre.fr/app/pyquickhelper/pyquickhelper-1.1.611-py2-none-any.whl
    
