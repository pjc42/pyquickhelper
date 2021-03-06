

.. _l-README:

README / Changes
================

.. image:: https://travis-ci.org/sdpython/pyquickhelper.svg?branch=master
    :target: https://travis-ci.org/sdpython/pyquickhelper
    :alt: Build status
    
.. image:: https://badge.fury.io/py/pyquickhelper.svg
    :target: http://badge.fury.io/py/pyquickhelper
        
.. image:: http://img.shields.io/pypi/dm/pyquickhelper.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/pyquickhelper
    
.. image:: http://img.shields.io/github/issues/sdpython/pyquickhelper.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pyquickhelper/issues
    
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT


**Links:**
    * `pypi/pyquickhelper <https://pypi.python.org/pypi/pyquickhelper/>`_
    * `GitHub/pyquickhelper <https://github.com/sdpython/pyquickhelper>`_
    * `documentation <http://www.xavierdupre.fr/app/pyquickhelper/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pyquickhelper>`_
    * `Travis <https://travis-ci.org/sdpython/pyquickhelper>`_
    * `Blog <http://www.xavierdupre.fr/app/pyquickhelper/helpsphinx/blog/main_0000.html#ap-main-0>`_

Functionalities
---------------

    * simple forms in notebooks
    * help generation including notebook conversion
    * folder synchronization
    * logging
    * help running unit tests
    * simple server to server sphinx documentation
    * file compression, zip, gzip, 7z
    * helpers for ipython notebooks (upgrade, offline run)
    * parser to quickly add a magic command in a notebook
    * Sphinx directives to integrate a blogpost in the documentation
    * mechanism to add forms in notebooks

Design
------

This project contains the following folders:
   * a source folder: ``src``
   * a unit test folder: ``_unittests``, go to this folder and run ``run_unittests.py``
   * a _doc folder: ``_doc``, it will contain the documentation
   * a file ``setup.py`` to build and to install the module, if the source were retrieve from GitHub,
     the script can also be called with the following extra options (``python setup.py <option>``):
     
        - clean_space: remove extra spaces in the code
        - clean_pyd: remove files *.pyd
        - build_sphinx: builds the documentation
        - unittests: run the unit tests, compute the code coverage
        
   * a script ``build_setup_help_on_windows.bat`` which run the unit tests, builds the setups and generate the documentaton on Windows
   * a script ``build_setup_help_on_linux.sh`` which does almost the same on Linux
   * a script ``publish_on_pipy.bat``

Versions / Changes
------------------

* **1.2 - 2015/??/??**
    * **change:** parameter prog was added to :class:`MagicCommandParser <pyquickhelper.ipythonhelper.magic_parser.MagicCommandParser>`
      *this might break classes taking dependency on it*
* **1.1 - 2015/05/24**
    * **fix:** shorten setup.py, move functionalities to the module, move utils_test.py to subfolder pycode
    * **change:** improve the generation of automated documentation
    * **change:** function :func:`create_visual_diff_through_html_files <pyquickhelper.filehelper.visual_sync.create_visual_diff_through_html_files>` 
      now returns appropriate objects to display the results into a notebook, it can also retrieve
      the content from a url or string
    * **add:** function :func:`read_url <pyquickhelper.filehelper.internet_helper.read_url>` and
      :func:`read_content_ufs <pyquickhelper.filehelper.anyfhelper.read_content_ufs>` 
      to read content from a string, a file, a url, a stream
    * **add:** add function :func:`set_notebook_name_theNotebook <pyquickhelper.ipythonhelper.notebook_helper.set_notebook_name_theNotebook>` 
      to set the notebook name into variable ``theNotebook`` within a notebook
    * **add:** add the possibility the run some code before executing a notebook
      (to populate a context for example)
    * **add:** revisit the automated scripts (*.bat), they are now generated by the module itself,
      see :func:`process_standard_options_for_setup <pyquickhelper.pycode.setup_helper.process_standard_options_for_setup>`
    * **add:** add format *slides* when converting a notebook
    * **add:** add function :func:`write_module_scripts <pyquickhelper.pycode.setup_helper.write_module_scripts>` which writes some helpful scripts
    * **add:** form interacting with Python functions in a notebook, 
      see notebook :ref:`havingaforminanotebookrst`.
    * **new:** the automated documentation now tries to split notebooks in slides by adding
      metadata, see method :meth:`add_tag_slide <pyquickhelper.ipythonhelper.notebook_runner.NotebookRunner.add_tag_slide>`
    * **add:** function :func:`add_notebook_menu <pyquickhelper.ipythonhelper.helper_in_notebook.add_notebook_menu>` 
      to automatically add a menu in a notebook 
      (which still shows up when the notebook is converted into another format)
    * **add:** the automated documentation now generates files .chm if it is done on Windows.
    * **new:** method :meth:`merge_notebook <pyquickhelper.ipythonhelper.notebook_runner.NotebookRunner.merge_notebook>` to merge notebooks into one
    * **new:** method :func:`nb2slides<pyquickhelper.helpgen.process_notebook_api.nb2slides>` to convert a notebook into slides
* **1.0 - 2015/04/21**
    * **new:** function to run a notebook end to end :func:`run_notebook <pyquickhelper.ipythonhelper.notebook_helper.run_notebook>`
    * **change:** function :func:`str_to_datetime <pyquickhelper.loghelper.convert_helper.str_to_datetime>` implicitely handles more formats
    * **change:** rename ``FileTreeStatus`` into :class:`FilesStatus <pyquickhelper.filehelper.files_status.FilesStatus>`
    * **new:** class :class:`FolderTransferFTP <pyquickhelper.filehelper.ftp_transfer_files.FolderTransferFTP>`
    * **new:** function :func:`remove_diacritics <pyquickhelper.texthelper.diacritic_helper.remove_diacritics>`
    * **new:** function :func:`docstring2html <pyquickhelper.helpgen.convert_doc_helper.docstring2html>` which converts RST documentation into HTML module IPython can display
    * **add:** run unit tests on `Travis-CI <https://travis-ci.org/sdpython/pyquickhelper>`_
    * **change:** renamed ``df_to_html`` into :func:`df2html <pyquickhelper.pandashelper.tblformat.df2html>`, ``df_to_rst`` into :func:`df2rst <pyquickhelper.pandashelper.tblformat.df2rst>`
    * **new:** function :func:`py3to2_convert_tree <pyquickhelper.pycode.py3to2.py3to2_convert_tree>` to convert files from python 3 to 2
    * **new:** class :class:`JenkinsExt <pyquickhelper.jenkinshelper.jenkins_server.JenkinsExt>` to help creating and deleting jobs on Jenkins
    * **new:** :class:`MagicCommandParser <pyquickhelper.ipythonhelper.magic_parser.MagicCommandParser>`, 
      :class:`MagicClassWithHelpers <pyquickhelper.ipythonhelper.magic_class.MagicClassWithHelpers>` to help creating magic commands on IPython notebooks,
      the parser tries to interpret values passed to the magic commands
    * **new:** function :func:`ipython_cython_extension <pyquickhelper.ipythonhelper.cython_helper.ipython_cython_extension>` which checks if cython can work on Windows (compiler issues)
    * **new:** the automated generation of the documentation now accepts blogs to be included (in folder ``_doc/sphinxdoc/source/blog``)
    * **change:** migration to IPython 3.1 (changes when running a notebook offline, converting a notebook)
    * **new:** some functionalities of pyquickhelper are now available in python 2.7, 
      not all the functionalities using string were migrated (too much of a pain)
