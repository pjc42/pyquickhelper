# -*- coding: utf-8 -*-
"""
@file
@brief Default values for the Sphinx configuration.
"""


import sys, os, datetime, re

#sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

def set_sphinx_variables(fileconf, module_name, author, year, theme, theme_path, ext_locals,
                add_extensions = None,
                bootswatch_theme = "spacelab",
                bootswatch_navbar_links = None
                ):
    """
    defines variables for Sphinx

    @param      fileconf                location of the configuration file
    @param      module_name             name of the module
    @param      author                  author
    @param      year                    year
    @param      theme                   theme to use
    @param      theme_path              themepath
    @param      ext_locals              context (see `locals <https://docs.python.org/2/library/functions.html#locals>`_)
    @param      add_extensions          additional extensions
    @param      bootswatch_theme        for example, ``spacelab``, look at ` <http://bootswatch.com/spacelab/>`_
    @param      bootswatch_navbar_links see `sphinx-bootstrap-theme <http://ryan-roemer.github.io/sphinx-bootstrap-theme/README.html>`_

    @example(Simple configuration file for Sphinx)

    We assume a module is configurated using the same
    structure as `pyquickhelper <https://github.com/sdpython/pyquickhelper/>`_.
    The file ``conf.py`` could just contain:

    @code
    # -*- coding: utf-8 -*-
    import sys, os, datetime, re
    import solar_theme
    from pyquickhelper.helpgen.default_conf import set_sphinx_variables

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
    set_sphinx_variables(   __file__,
                            "pyquickhelper",
                            "Xavier Dupré",
                            2014,
                            "solar_theme",
                            solar_theme.theme_path,
                            locals())
    @endcode
    @endexample
    """
    project_var_name            = module_name
    author                      = author
    year                        = str(year)
    version                     = extract_version_from_setup(fileconf)
    pygments_style              = 'sphinx'
    modindex_common_prefix      = [ project_var_name + ".", ]
    html_theme                  = theme
    shtml_theme_options         = { "bodyfont":"Calibri"}
    if theme_path is not None:
        html_theme_path         = [ theme_path ]
    html_logo                   = "project_ico.png"
    html_favicon                = "project_ico.ico"
    html_static_path            = ['phdoc_static']
    templates_path              = ['phdoc_templates']
    source_suffix               = '.rst'
    source_encoding             = 'utf-8'
    master_doc                  = 'index'
    project                     = project_var_name + ' documentation'
    copyright                   = str(year) + ", " + author
    version_file                = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", "..", "version.txt"))
    first_line                  = get_first_line(version_file)
    release                     = '%s.%s' % (version, first_line)
    exclude_patterns            = []
    html_title                  = "%s %s" % (project_var_name, release)
    html_show_sphinx            = False
    html_show_copyright         = False
    htmlhelp_basename           = '%s_doc' % project_var_name
    latex_use_parts             = True
    latex_show_pagerefs         = True
    __html_last_updated_fmt_dt  = datetime.datetime.now()
    html_last_updated_fmt       = '%04d-%02d-%02d' % (__html_last_updated_fmt_dt.year, __html_last_updated_fmt_dt.month, __html_last_updated_fmt_dt.day)
    autoclass_content           = 'both'
    autosummary_generate        = True
    graphviz_output_format      = "svg"
    graphviz_dot                = get_graphviz_dot()

    extensions = [  'sphinx.ext.autodoc',
                    'sphinx.ext.todo',
                    'sphinx.ext.coverage',
                    'sphinx.ext.pngmath',
                    'sphinx.ext.ifconfig',
                    'sphinx.ext.viewcode',
                    'sphinxcontrib.fancybox',
                    'sphinx.ext.autosummary',
                    'sphinx.ext.graphviz',
                    'sphinx.ext.inheritance_diagram',
                    'matplotlib.sphinxext.plot_directive',
                    ]

    if add_extensions is not None:
        extensions.extend(add_extensions)

    #add_function_parentheses = True
    #add_module_names = True
    #show_authors = False
    #html_sidebars = {}
    #html_additional_pages = {}
    #html_domain_indices = True
    #html_use_index = True
    #html_split_index = False
    #html_show_sourcelink = True
    #html_use_opensearch = ''
    #html_file_suffix = None
    #latex_logo = None
    #latex_show_urls = False
    #latex_appendices = []
    #latex_domain_indices = True
    #texinfo_appendices = []
    #texinfo_domain_indices = True
    #texinfo_show_urls = 'footnote'


    latex_elements      = { 'papersize': 'a4', 'pointsize': '10pt',
                        #'preamble': '',
                        }
    latex_documents     = [ ( 'index', '%s_doc.tex' % project_var_name, '%s Documentation' % project_var_name, author, 'manual'), ]
    man_pages           = [ ( 'index', '%s_doc' % project_var_name, '%s Documentation' % project_var_name, [author], 1) ]
    texinfo_documents   = [   ('index', '%s_documentation' % project_var_name, '%s Documentation' % project_var_name,
                            author, '%s documentation' % project_var_name,
                            'One line description of project.',
                            'Miscellaneous'),
                        ]


    if html_theme == "bootstrap":
        if bootswatch_navbar_links is None:
            bootswatch_navbar_links = []
        html_logo = "project_ico_small.png"
        html_theme_options = {
            'navbar_title'              : "home",
            'navbar_site_name'          : "Site",
            'navbar_links'              : navbar_links,
            'navbar_sidebarrel'         : True,
            'navbar_pagenav'            : True,
            'navbar_pagenav_name'       : "Page",
            'globaltoc_depth'           : 3,
            'globaltoc_includehidden'   : "true",
            'navbar_class'              : "navbar navbar-inverse",
            'navbar_fixed_top'          : "true",
            'source_link_position'      : "nav",
            'bootswatch_theme'          : bootswatch_theme,
            'bootstrap_version'         : "3",
        }

    loc = locals()
    for k,v in loc.items():
        if not k.startswith("_"):
            ext_locals[k] = v

    def this_setup(app):
        return custom_setup(app, author)
    ext_locals["setup"] = this_setup


#################
# custom functions
#################

def extract_version_from_setup(filename):
    """
    extract the version from setup.py assuming it is located in ../../..
    and the version is specified by the following line: ``sversion = "..."``
    """
    setup = os.path.abspath(os.path.split(filename)[0])
    setup = os.path.join(setup, "..", "..", "..", "setup.py")
    if os.path.exists(setup):
        with open(setup,"r") as f : content = f.read()
        exp = re.compile("sversion *= *['\\\"]([0-9.]+?)['\\\"]")
        all = exp.findall(content)
        if len(all) == 0:
            raise Exception("unable to locate the version from setup.py")
        if len(all) != 1 :
            raise Exception("more than one version was found: " + str(all))
        return all[0]
    else:
        raise FileNotFoundError("unable to find setup.py, tried: " + setup)

def get_first_line(filename):
    """
    expects to find a text file with a line, the function extracts and returns this line
    """
    try :
        with open(filename, "r") as ff : first_line = ff.readlines()[0].strip(" \n\r")
    except FileNotFoundError :
        first_line = "xxx"
    return first_line

def get_graphviz_dot():
    """
    finds Graphviz executable dot, does something specific for Windows
    """
    if sys.platform.startswith("win"):
        version = range(34,42)
        for v in version:
            graphviz_dot = r"C:\Program Files (x86)\Graphviz2.{0}\bin\dot.exe".format(v)
            if os.path.exists(graphviz_dot):
                break

    if sys.platform.startswith("win") :
        if not os.path.exists(graphviz_dot):
            raise FileNotFoundError(graphviz_dot)
    else:
        graphviz_dot = "dot"
    return graphviz_dot

#################
# sphinx functions
#################

def skip(app, what, name, obj, skip, options):
    """
    to skip some functions,

    see `Skipping members <http://sphinx-doc.org/ext/autodoc.html#event-autodoc-skip-member>`_
    """
    if name.startswith("_") and name not in \
            [   "__qualname__",
                "__module__",
                "__dict__",
                "__doc__",
                "__weakref__",
                ]:
        return False
    return skip

def custom_setup(app, author):
    """
    see `Sphinx core events <http://sphinx-doc.org/extdev/appapi.html?highlight=setup#sphinx-core-events>`_
    """
    app.connect("autodoc-skip-member", skip)
    app.add_config_value('author', author, True)