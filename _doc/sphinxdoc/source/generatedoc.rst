Generate this documentation
===========================


.. generatedoc:

The documentation can be written using `RST <http://sphinx-doc.org/rest.html>`_ format
or `javadoc <http://en.wikipedia.org/wiki/Javadoc>`_ format. The documentation
can generated by::

    python setup.py build_sphinx
    
It requires the full sources from GitHub and not only the installed package which does not 
contains the documentation.
It will go through the following steps:

    * it will copy all files found in ``src`` in folder ``_doc/sphinxdoc/source/[project_name]``
    * it will generates a file .rst for each python file in ``_doc/sphinxdoc/source/[project_name]``
    * it will run the generation of the documentation using Sphinx.
    * notebooks can be placed in ``_doc/notebooks``, they will be added to the documentation
    * it will generated aggregated pages for blog posts added to 
      ``_doc/sphinxdoc/source/blog/YYYY/<anything>.rst``.

The results are stored in folder ``_doc/sphinxdoc/build``.
On Windows, the batch file ``build_setup_help_on_windows.bat`` copies all files
into ``dist/html``.


Configuration:

.. literalinclude:: conf.py

Design
++++++

The module is organized as follows:

    * ``pyquickhelper/src/pyquickhelper``: contains the sources of the modules
    * ``pyquickhelper/_unittests/``: contains the unit tests, they can run with program ``run_unittests.py``
    * ``pyquickhelper/_unittests/_doc/notebooks``: contains the notebooks included in the documentation
    * ``pyquickhelper/_unittests/_doc/sphinxdoc/source``: contains the sphinx documentation
    * ``pyquickhelper/_unittests/_doc/sphinxdoc/blog/YYYY``: contains the blog posts

When the documentation is being generated,
the sources are copied into ``pyquickhelper/_unittests/_doc/sphinxdoc/source/pyquickhelper``.
The documentation can be in `javadoc <http://en.wikipedia.org/wiki/Javadoc>`_ 
format is replaced by the RST syntax. Various
files are automatically generated (indexes, examples, FAQ).
Then `sphinx <http://sphinx-doc.org/>`_ is run.
After the documentation is generated, everything is copied into folder ``pyquickhelper/dist``.

``python setup.py build_sphinx`` generates the documentation
(see :func:`process_standard_options_for_setup <pyquickhelper.pycode.setup_helper.process_standard_options_for_setup>`).


Extensions to install
+++++++++++++++++++++

* `Sphinx <http://sphinx-doc.org/>`_
* `coverage <http://nedbatchelder.com/code/coverage/>`_

Default extensions::

    extensions = ['sphinx.ext.autodoc',
                  'sphinx.ext.todo',
                  'sphinx.ext.coverage',
                  'sphinx.ext.pngmath',
                  'sphinx.ext.ifconfig',
                  'sphinx.ext.viewcode',
                  'sphinxcontrib.images',
                  'sphinx.ext.autosummary',
                  'sphinx.ext.graphviz',
                  'sphinx.ext.inheritance_diagram',
                  'matplotlib.sphinxext.plot_directive',
                  'matplotlib.sphinxext.mathmpl',
                  'matplotlib.sphinxext.only_directives',
                  'IPython.sphinxext.ipython_console_highlighting',
                  'sphinx.ext.napoleon',
                  'bokeh.sphinxext.bokeh_plot', ]

As the documentation creates graphs to represent the dependencies,
Graphviz needs to be installed. Here is the list of tools usually used:

* `Python 3.4 64 bit <https://www.python.org/downloads/>`_
* `7zip <http://www.7-zip.org/>`_
* `Miktex <http://miktex.org/>`_
* `Jenkins <https://jenkins-ci.org/>`_ (+ `GitHub <https://wiki.jenkins-ci.org/display/JENKINS/GitHub+Plugin>`_, 
  `git <https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin>`_, 
  `python <https://wiki.jenkins-ci.org/display/JENKINS/Python+Plugin>`_, 
  `pipeline <https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin>`_)
* `pandoc <http://pandoc.org/>`_
* `Git <http://git-scm.com/>`_ + `GitHub <https://github.com/>`_
* `GraphViz <http://www.graphviz.org/>`_

If you need to use `Antlr <http://www.antlr.org/>`_:

* `Java <http://www.java.com/fr/download/>`_



Notebooks
+++++++++

Notebooks in folder ``pyquickhelper/_doc/notebooks`` will be automatically
be convected into *html* and *pdf* formats but that requires
latex and `pandoc <http://pandoc.org/>`_.

Themes
++++++

Depending on the module, themes might be needed.

* `sphinxcontrib-images <http://pythonhosted.org//sphinxcontrib-images/>`_
* `sphinxjp.themes.sphinxjp <https://pypi.python.org/pypi/sphinxjp.themes.sphinxjp>`_ 
* `sphinx_rtd_theme <https://github.com/snide/sphinx_rtd_theme>`_ 
* `sphinx_bootstrap_theme <http://ryan-roemer.github.io/sphinx-bootstrap-theme/>`_ 
* `sphinxjp.themes.basicstrap <https://pythonhosted.org/sphinxjp.themes.basicstrap/>`_ 
* `sphinx_py3doc_enhanced_theme <https://pypi.python.org/pypi/sphinx_py3doc_enhanced_theme>`_