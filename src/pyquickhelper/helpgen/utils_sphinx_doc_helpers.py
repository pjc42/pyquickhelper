"""
@file
@brief various variables and classes used to produce a Sphinx documentation

"""

import inspect
import os
import copy
import re
import sys
import importlib
from ..pandashelper.tblformat import df2rst
from ..loghelper.flog import noLOG
from .helpgen_exceptions import HelpGenException, ImportErrorHelpGen

if sys.version_info[0] == 2:
    from codecs import open


#: max length for short summaries
_length_truncated_doc = 120


#: template for a module, substring ``__...__`` ought to be replaced
add_file_rst_template = """
__FULLNAME_UNDERLINED__




.. inheritance-diagram:: __FULLNAMENOEXT__


Short summary
+++++++++++++

__DOCUMENTATION__


__CLASSES__

__FUNCTIONS__

__PROPERTIES__

__STATICMETHODS__

__METHODS__

Documentation
+++++++++++++

.. automodule:: __FULLNAMENOEXT__
    :members:
    :show-inheritance:

__ADDEDMEMBERS__

"""

#: fields to be replaced
add_file_rst_template_cor = {"class": "__CLASSES__",
                             "method": "__METHODS__",
                             "function": "__FUNCTIONS__",
                             "staticmethod": "__STATICMETHODS__",
                             "property": "__PROPERTIES__",
                             }

#: names for python objects
add_file_rst_template_title = {"class": "Classes",
                               "method": "Methods",
                               "function": "Functions",
                               "staticmethod": "Static Methods",
                               "property": "Properties",
                               }

#
# :platform: Unix, Windows
#   :synopsis: Analyze and reanimate dead parrots.
# .. moduleauthor:: xx <x@x>
# .. moduleauthor:: xx <x@x>
#  for autosummary
#   :toctree: __FILENAMENOEXT__/
#


def compute_truncated_documentation(doc,
                                    length=_length_truncated_doc,
                                    raise_exception=False):
    """
    produces a truncated version of a docstring
    @param      doc                 doc string
    @param      length              approximated length of the truncated docstring
    @param      raise_exception     raises an exception when the result is empty and the input is not
    @return                         truncated doc string
    """
    if len(doc) == 0:
        return doc
    else:
        doc_ = doc

        if "@brief " in doc:
            doc = doc.split("@brief ")
            doc = doc[-1]

        doc = doc.strip("\n\r\t ")
        doc = doc.replace("\n", " ").replace("\r", "").strip("\n\r\t ")

        for subs in ["@" + "param", "@" + "return", ":param", ":return"]:
            if subs in doc:
                doc = doc[:doc.find(subs)].strip("\r\t ")

        if len(doc) >= _length_truncated_doc:
            spl = doc.split(" ")
            doc = ""
            cq = 0
            i = 0
            while len(doc) < _length_truncated_doc or cq % 2 != 0:
                cq += spl[i].count("`")
                doc += spl[i] + " "
                i += 1
            doc += "..."

        if raise_exception and len(doc) == 0:
            raise ValueError("bad format for docstring: " + doc_)
        return doc


class ModuleMemberDoc:

    """
    represents a member in a module

    See `inspect <https://docs.python.org/3.4/library/inspect.html>`_

    @var    obj         object
    @var    type        (str) type
    @var    cl          (class) class it belongs to
    @var    name        (str) name
    @var    module      (str) module name
    @var    doc         (str) documentation
    @var    truncdoc    (str) truncated documentation
    @var    owner       (module)
    """

    def __init__(self, obj, ty=None, cl=None, name=None, module=None):
        """
        constructor
        @param      obj     any kind of object
        @param      ty      type (if you want to overwrite what the class will choose),
                            this type is a string (class, method, function)
        @param      cl      if is a method, class it belongs to
        """
        if module is None:
            raise ValueError("module cannot be null")

        self.owner = module
        self.obj = obj
        self.cl = cl
        if ty is not None:
            self.type = ty
        self.name = name
        self.populate()

        typstr = str  # unicode#

        if self.cl is None and self.type in [
                "method", "staticmethod", "property"]:
            self.cl = self.obj.__class__
        if self.cl is None and self.type in [
                "method", "staticmethod", "property"]:
            raise TypeError(
                "N/a method must have a class (not None): %s" % typstr(self.obj))

    def add_prefix(self, prefix):
        """
        adds a prefix (for the documentation)
        @param      prefix      string
        """
        self.prefix = prefix

    @property
    def key(self):
        """
        returns a key to identify it
        """
        return "%s;%s" % (self.type, self.name)

    def populate(self):
        """
        extract some information about an object
        """
        obj = self.obj
        ty = self.type if "type" in self.__dict__ else None
        typstr = str  # unicode#
        if ty is None:
            if inspect.isclass(obj):
                self.type = "class"
            elif inspect.ismethod(obj):
                self.type = "method"
            elif inspect.isfunction(obj):
                self.type = "function"
            elif inspect.isgenerated(obj):
                self.type = "generator"
            else:
                raise TypeError(
                    "E/unable to deal with this type: " + typstr(type(obj)))

        if ty == "method":
            if isinstance(obj, staticmethod):
                self.type = "staticmethod"
            elif isinstance(obj, property):
                self.type = "property"
            elif sys.version_info >= (3, 4):
                # should be replaced by something more robust
                if len(obj.__code__.co_varnames) == 0:
                    self.type = "staticmethod"
                elif obj.__code__.co_varnames[0] != 'self':
                    self.type = "staticmethod"

        # module
        try:
            self.module = obj.__module__
            self.name = obj.__name__
        except Exception:
            if self.type in ["property", "staticmethod"]:
                self.module = self.cl.__module__
            else:
                self.module = None
            if self.name is None:
                raise IndexError("unable to find a name for this object")

        # full path for the module
        if self.module is not None:
            self.fullpath = self.module
        else:
            self.fullpath = ""

        # documentation
        if self.type == "staticmethod":
            try:
                self.doc = obj.__func__.__doc__
            except Exception as ie:
                try:
                    self.doc = obj.__doc__
                except Exception as ie2:
                    self.doc = typstr(
                        ie) + " - " + typstr(ie2) + " \n----------\n " + typstr(dir(obj))
        else:
            try:
                self.doc = obj.__doc__
            except Exception as ie:
                self.doc = typstr(ie) + " \n----------\n " + typstr(dir(obj))

        try:
            self.file = self.module.__file__
        except:
            self.file = ""

        # truncated documentation
        if self.doc is not None:
            self.truncdoc = compute_truncated_documentation(self.doc)
        else:
            self.doc = ""
            self.truncdoc = ""

        if self.name is None:
            raise TypeError("S/name is None for object: %s" % typstr(self.obj))

    def __str__(self):
        """
        usual
        """
        return "[key={0},clname={1},type={2},module_name={3},file={4}".format(
            self.key, self.classname, self.type, self.module, self.owner.__file__)

    def rst_link(self, prefix=None, class_in_bracket=True):
        """
        returns a sphinx link on the object
        @param      prefix              to correct the path with a prefix
        @param      class_in_bracket    if True, adds the class in bracket for methods and properties
        @return                         a string style::

                                            :%s:`%s <%s>`               or
                                            :%s:`%s <%s>` (class)
        """
        cor = {"function": "func", "method": "meth",
               "staticmethod": "meth", "property": "meth"}

        if self.type in ["method", "staticmethod", "property"]:
            path = "%s.%s.%s" % (self.module, self.cl.__name__, self.name)
        else:
            path = "%s.%s" % (self.module, self.name)

        if prefix is not None:
            path = "%s.%s" % (prefix, path)

        if self.type in ["method", "staticmethod",
                         "property"] and class_in_bracket:
            link = ":%s:`%s <%s>` (%s)" % (
                cor.get(self.type, self.type), self.name, path, self.cl.__name__)
        else:
            link = ":%s:`%s <%s>`" % (
                cor.get(self.type, self.type), self.name, path)
        return link

    @property
    def classname(self):
        """
        returns the class name if the object is a method
        @return     class object
        """
        if self.type in ["method", "staticmethod", "property"]:
            return self.cl
        else:
            return None

    def __cmp__(self, oth):
        """
        comparison operators, compares first the first, second the name (lower case)
        @param      oth         other object
        @return                 -1, 0 or 1
        """
        if self.type == oth.type:
            ln = self.fullpath + "@@@" + self.name.lower()
            lo = oth.fullpath + "@@@" + oth.name.lower()
            c = -1 if ln < lo else (1 if ln > lo else 0)
            if c == 0 and self.type == "method":
                ln = self.cl.__name__
                lo = self.cl.__name__
                c = -1 if ln < lo else (1 if ln > lo else 0)
            return c
        else:
            return - \
                1 if self.type < oth.type else (
                    1 if self.type > oth.type else 0)

    def __lt__(self, oth):
        """
        operator ``<``
        """
        return self.__cmp__(oth) == -1

    def __eq__(self, oth):
        """
        operator ``==``
        """
        return self.__cmp__(oth) == 0

    def __gt__(self, oth):
        """
        operator ``>``
        """
        return self.__cmp__(oth) == 1


class IndexInformation:

    """
    keeps some information to index
    """

    def __init__(self, type, label, name, text, rstfile, fullname):
        """
        @param      type        each type gets an index
        @param      label       label used to index
        @param      name        name to display
        @param      text        text to show as a short description
        @param      rstfile     tells which file the index refers to (rst file)
        @param      fullname    fullname of a file the rst file describes
        """
        self.type = type
        self.label = label
        self.name = name
        self.text = text
        self.fullname = fullname
        self.set_rst_file(rstfile)

    def __str__(self):
        """
        usual
        """
        return "%s -- %s" % (self.label, self.rst_link())

    def set_rst_file(self, rstfile):
        """
        sets the rst file and checks the label is present in it
        @param      rst_file        rst_file
        """
        self.rstfile = rstfile
        if rstfile is not None:
            self.add_label_if_not_present()

    @property
    def truncdoc(self):
        """
        returns self.text
        """
        return self.text.replace("\n", "  ").replace(
            "\t", "").replace("\r", "")

    def add_label_if_not_present(self):
        """
        The function checks the label is present in the original file.
        """
        if self.rstfile is not None:
            with open(self.rstfile, "r", encoding="utf8") as f:
                content = f.read()
            label = ".. _%s:" % self.label
            if label not in content:
                content = "\n%s\n%s" % (label, content)
                with open(self.rstfile, "w", encoding="utf8") as f:
                    f.write(content)

    def get_label(existing, suggestion):
        """
        returns a new label given the existing ones
        @param  existing    existing labels stored in a dictionary
        @param  suggestion  the suggestion will be chosen if it does not exists, ``suggestion + zzz`` otherwise
        @return             string
        """
        suggestion = suggestion.replace("_", "").replace(".", "")
        while suggestion in existing:
            suggestion += "z"
        return suggestion
    get_label = staticmethod(get_label)

    def rst_link(self):
        """
        return a link rst
        @return     rst link
        """
        if self.label.startswith("_"):
            return ":ref:`%s`" % self.label[1:]
        else:
            return ":ref:`%s`" % self.label


class RstFileHelp:

    """
    defines what a rst file and what it describes
    """

    def __init__(self, file, rst, doc):
        """
        @param      file        original filename
        @param      rst         produced rst file
        @param      doc         documentation if any
        """
        self.file = file
        self.rst = rst
        self.doc = doc


def import_module(
        rootm, filename, log_function, additional_sys_path=[], fLOG=noLOG):
    """
    import a module using its filename
    @param      rootm                   root of the module (for relative import)
    @param      filename                file name of the module
    @param      log_function            logging function
    @param      additional_sys_path     additional path to include to sys.path before importing a module (will be removed afterwards)
    @param      fLOG                    logging function
    @return                             module object, prefix

    @warning It adds the file path at the first position in sys.path and then deletes it.

    .. versionadded:: 1.0
        Parameter *fLOG* was added.
    """
    memo = copy.deepcopy(sys.path)
    l = filename.replace("\\", "/")
    sdir = os.path.abspath(os.path.split(l)[0])
    relpath = os.path.relpath(l, rootm).replace("\\", "/")
    spl = relpath.split("/")
    fmod = spl[0]  # this is the prefix
    relpath = "/".join(spl[1:])

    # has init
    init_ = os.path.join(sdir, "__init__.py")
    if init_ != filename and not os.path.exists(init_):
        # no init
        return "No __init__.py, unable to import %s" % (filename), fmod

    # we remove every path ending by "src"
    rem = []
    for i, p in enumerate(sys.path):
        if p.endswith("src") or ".zip" in p:
            rem.append(i)
    rem.reverse()
    for r in rem:
        del sys.path[r]

    # remove fmod from sys.modules
    addback = []
    rem = []
    for n, m in sys.modules.items():
        if n.startswith(fmod):
            rem.append(n)
            addback.append((n, m))

    # we remove the modules
    # this line is important to remove all modules
    # from the sources in folder src and not the modified ones
    # in the documentation folder
    for r in rem:
        del sys.modules[r]

    # full path
    if rootm is not None:
        root = rootm
        tl = relpath
        fi = tl.replace(".py", "").replace("/", ".")
        fi = fmod + "." + fi
        context = None
        if fi.endswith(".__init__"):
            fi = fi[:-len(".__init__")]
    else:
        root = sdir
        tl = os.path.split(l)[1]
        fi = tl.replace(".py", "")
        context = None

    if additional_sys_path is not None and len(additional_sys_path) > 0:
        # there is an issue here due to the confusion in the paths
        # the paths should be removed just after the import
        sys.path.extend(additional_sys_path)

    sys.path.insert(0, root)
    try:
        try:
            mo = importlib.import_module(fi, context)
        except ImportError:
            fLOG("unable to import module ", fi, "fullname", filename)
            mo_spec = importlib.util.find_spec(fi, context)
            fLOG("imported spec", mo_spec)
            mo = mo_spec.loader.load_module()
            fLOG("successful try", mo_spec)

        if not mo.__file__.replace(
                "\\", "/").endswith(filename.replace("\\", "/").strip("./")):
            namem = os.path.splitext(os.path.split(filename)[-1])[0]

            if "src" in sys.path:
                sys.path = [_ for _ in sys.path if _ != "src"]

            if namem in sys.modules:
                del sys.modules[namem]
                # add the context here for relative import
                # use importlib.import_module with the package argument filled
                # mo = __import__ (fi)
                try:
                    mo = importlib.import_module(fi, context)
                except ImportError:
                    mo = importlib.util.find_spec(fi, context)

                if not mo.__file__.replace(
                        "\\", "/").endswith(filename.replace("\\", "/").strip("./")):
                    raise ImportError("the wrong file was imported (2):\nEXP: {0}\nIMP: {1}\nPATHS:\n   - {2}"
                                      .format(filename, mo.__file__, "\n   - ".join(sys.path)))
            else:
                raise ImportError("the wrong file was imported (1):\nEXP: {0}\nIMP: {1}\nPATHS:\n   - {2}"
                                  .format(filename, mo.__file__, "\n   - ".join(sys.path)))

        sys.path = memo
        log_function("importing ", filename, " successfully", mo.__file__)
        for n, m in addback:
            if n not in sys.modules:
                sys.modules[n] = m
        return mo, fmod

    except ImportError as e:
        exp = re.compile("No module named '(.*)'")
        find = exp.search(str(e))
        if find:
            module = find.groups()[0]
            log_function(
                "unable to import module " + module + " --- " + str(e).replace("\n", " "))

        log_function("  File \"%s\", line %d" % (__file__, 501))
        log_function("-- unable to import module (1) ", filename,
                     ",", fi, " in path ", sdir, " Error: ", str(e))
        log_function("    cwd ", os.getcwd())
        log_function("    path", sdir)
        import traceback
        stack = traceback.format_exc()
        log_function("      executable", sys.executable)
        log_function("      version", sys.version_info)
        log_function("      stack:\n", stack)

        message = [stack]
        message.append("      executable: " + sys.executable)
        message.append("      version: " + str(sys.version_info))
        for p in sys.path:
            message.append("      path: " + p)
        for p in sorted(sys.modules):
            try:
                m = sys.modules[p].__path__
            except AttributeError:
                m = str(sys.modules[p])
            message.append("      module: {0}={1}".format(p, m))

        sys.path = memo
        for n, m in addback:
            if n not in sys.modules:
                sys.modules[n] = m

        if 'File "<frozen importlib._bootstrap>"' in stack:
            raise ImportErrorHelpGen(
                "frozen importlib._bootstrap is an issue:\n" + "\n".join(message)) from e

        return "unable to import %s\nError:\n%s" % (filename, str(e)), fmod

    except SystemError as e:
        log_function("-- unable to import module (2) ", filename,
                     ",", fi, " in path ", sdir, " Error: ", str(e))
        import traceback
        stack = traceback.format_exc()
        log_function("      executable", sys.executable)
        log_function("      version", sys.version_info)
        log_function("      stack:\n", stack)
        sys.path = memo
        for n, m in addback:
            if n not in sys.modules:
                sys.modules[n] = m
        return "unable to import %s\nError:\n%s" % (filename, str(e)), fmod

    except Exception as e:
        log_function("-- unable to import module (3) ", filename,
                     ",", fi, " in path ", sdir, " Error: ", str(e))
        import traceback
        stack = traceback.format_exc()
        log_function("      executable", sys.executable)
        log_function("      version", sys.version_info)
        log_function("      stack:\n", stack)
        sys.path = memo
        for n, m in addback:
            if n not in sys.modules:
                sys.modules[n] = m
        return "unable to import %s\nError:\n%s" % (filename, str(e)), fmod


def get_module_objects(mod):
    """
    gets all the classes from a module
    @param      mod     module objects
    @return             list of ModuleMemberDoc
    """

    # exp = { "__class__":"",
    #        "__dict__":"",
    #        "__doc__":"",
    #        "__format__":"",
    #        "__reduce__":"",
    #        "__reduce_ex__":"",
    #        "__subclasshook__":"",
    #        "__dict__":"",
    #        "__weakref__":""
    #         }

    cl = []
    for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj) or \
           inspect.isfunction(obj) or \
           inspect.isgenerator(obj) or \
           inspect.ismethod(obj):
            cl.append(ModuleMemberDoc(obj, module=mod))
            if inspect.isclass(obj):
                for n, o in inspect.getmembers(obj):
                    try:
                        ok = ModuleMemberDoc(
                            o, "method", cl=obj, name=n, module=mod)
                        if ok.module is not None:
                            cl.append(ok)
                    except Exception as e:
                        if str(e).startswith("S/"):
                            raise e

    res = []
    for _ in cl:
        try:
            # if _.module != None :
            if _.module == mod.__name__:
                res.append(_)
        except:
            pass

    res.sort()
    return res


def process_var_tag(
        docstring, rst_replace=False, header=["attribute", "meaning"]):
    """
    Process a docstring using tag ``@ var``, and return a list of 2-tuple

    @code
        @ var    filename        file name
        @ var    utf8            decode in utf8?
        @ var    errors          decoding in utf8 can raise some errors
    @endcode

    @param      docstring       string
    @param      rst_replace     if True, replace the var bloc var a rst bloc
    @param      header          header for the table
    @return                     a matrix with two columns or a string if rst_replace is True

    """
    from pandas import DataFrame

    reg = re.compile("[@]var +([_a-zA-Z][a-zA-Z0-9_]*?) +((?:(?!@var).)+)")

    docstring = docstring.split("\n")
    docstring = [_.strip("\r \t") for _ in docstring]
    docstring = [_ if len(_) > 0 else "\n\n" for _ in docstring]
    docstring = "\n".join(docstring)
    docstring = docstring.split("\n\n")

    values = []
    if rst_replace:
        for line in docstring:
            line2 = line.replace("\n", " ")
            if "@var" in line2:
                all = reg.findall(line2)
                val = []
                for a in all:
                    val.append(list(a))
                if len(val) > 0:
                    tbl = DataFrame(columns=header, data=val)
                    align = ["1x"] * len(header)
                    align[-1] = "3x"
                    rst = df2rst(tbl, align=align)
                    values.append(rst)
            else:
                values.append(line)
        return "\n".join(values)
    else:
        for line in docstring:
            line = line.replace("\n", " ")
            if "@var" in line:
                alls = reg.findall(line)
                for a in alls:
                    values.append(a)
        return values


def make_label_index(title, comment):
    """
    build a sphinx label from a string by
    removing any odd characters

    @param      title       title
    @param      comment     add this string in the exception when it raises one
    @return                 label
    """
    def accept(c):
        if "a" <= c <= "z":
            return c
        if "A" <= c <= "Z":
            return c
        if "0" <= c <= "9":
            return c
        if c in "-_":
            return c
        return ""

    try:
        r = "".join(map(accept, title))
        if len(r) == 0:
            typstr = str  # unicode#
            raise HelpGenException("unable to interpret this title (empty?): {0} (type: {2})\nCOMMENT:\n{1}".format(
                typstr(title), comment, typstr(type(title))))
        return r
    except TypeError as e:
        typstr = str  # unicode#
        raise HelpGenException("unable to interpret this title: {0} (type: {2})\nCOMMENT:\n{1}".format(
            typstr(title), comment, typstr(type(title)))) from e


def process_look_for_tag(tag, title, files):
    """
    looks for specific information in all files, collect them
    into one single page

    @param      tag     tag
    @param      title   title of the page
    @param      files   list of files to look for
    @return             a list of tuple (page, content of the page)

    The function is looking for regular expression::

        .. tag(...).
        ...
        .. endtag.

    They can be split into several pages::

        .. tag(page::...).
        ...
        .. endtag.

    If the extracted example contains an image (..image:: ../../), the path
    is fixed too.

    The function parses the files instead of loading the files as a module.
    The function needs to replace ``\\\\`` by ``\\``, it does not takes into
    acount doc string starting with ``r'''``.

    .. versionchanged:: 0.9
        Calls function @see fn remove_some_indent with ``backslash=True`` to replace double backslash by simple backslash.
    """
    def noneempty(a):
        if "___" in a:
            page, a = a.split("___")
            return "_" + page, a.lower(), a
        else:
            return "", a.lower(), a
    repl = "__!LI!NE!__"
    exp = re.compile(
        "[.][.] %s[(](.*?);;(.*?)[)][.](.*?)[.][.] end%s[.]" % (tag, tag))
    exp2 = re.compile(
        "[.][.] %s[(](.*?)[)][.](.*?)[.][.] end%s[.]" % (tag, tag))
    coll = []
    for file in files:
        if file.file is None:
            continue
        if "utils_sphinx_doc.py" in file.file:
            continue
        try:
            with open(file.file, "r", encoding="utf8") as f:
                content = f.read()
        except:
            with open(file.file, "r") as f:
                content = f.read()
        content = content.replace("\n", repl)

        all = exp.findall(content)
        all2 = exp2.findall(content)
        if len(all2) > len(all):
            raise HelpGenException(
                "an issue was detected in file: " + file.file)

        coll += [noneempty(a) +
                 (fix_image_page_for_root(c.replace(repl, "\n"), file), b) for a, b, c in all]

    coll.sort()
    coll = [(_[0],) + _[2:] for _ in coll]

    pages = set(_[0] for _ in coll)

    pagerows = []

    for page in pages:
        if page == "":
            tit = title
            suf = ""
        else:
            tit = title + ": " + page.strip("_")
            suf = page.replace(" ", "").replace("_", "")
            suf = re.sub(r'([^a-zA-Z0-9_])', "", suf)
            page = re.sub(r'([^a-zA-Z0-9_])', "", page)

        rows = ["""
            .. _l-{0}{3}:

            {1}
            {2}

            .. contents::

            """.replace("            ", "").format(tag, tit, "=" * len(tit), suf)]

        if os.environ.get("USERNAME", "````````````") in rows[0]:
            raise HelpGenException(
                "the title is probably wrong: {0}\ntag={1}\ntit={1}".format(rows[0], tag, tit))

        for pa, a, b, c in coll:
            pan = re.sub(r'([^a-zA-Z0-9_])', "", pa)
            if page != pan:
                continue
            lindex = make_label_index(a, pan)
            rows.append("")
            rows.append(".. _lm-{0}:".format(lindex))
            rows.append("")
            rows.append(a)
            rows.append("+" * len(a))
            rows.append("")
            rows.append(remove_some_indent(b, backslash=True))
            rows.append("")
            spl = c.split("-")
            d = "file {0}.py".format(spl[1])  # line, spl[2].lstrip("l"))
            rows.append("see :ref:`%s <%s>`" % (d, c))
            rows.append("")

        pagerows.append((page, "\n".join(rows)))
    return pagerows


def fix_image_page_for_root(content, file):
    """
    look for images and fix their path as if the extract were copied to the root

    @param      content     extracted content
    @param      file        file where is comes from (unused)
    @return                 content
    """
    rows = content.split("\n")
    for i in range(len(rows)):
        row = rows[i]
        if ".. image::" in row:
            spl = row.split(".. image::")
            img = spl[-1]
            if "../images" in img:
                img = img.lstrip("./ ")
            if len(spl) == 1:
                row = ".. image:: " + img
            else:
                row = spl[0] + ".. image:: " + img
            rows[i] = row
    return "\n".join(rows)


def remove_some_indent(s, backslash=False):
    """
    bring text to the left

    @param      s               text
    @param      backslash       if True, replace double backslash by simple backslash
    @return                     text

    .. versionchanged:: 0.9
        Add parameter *backslash* to remove replace double backslash by simple backslah.
    """
    rows = s.split("\n")
    mi = len(s)
    for l in rows:
        ll = l.lstrip()
        if len(ll) > 0:
            d = len(l) - len(ll)
            mi = min(d, mi)

    if mi > 0:
        keep = []
        for _ in rows:
            keep.append(_[mi:] if len(_.strip()) > 0 and len(_) > mi else _)
        res = "\n".join(keep)
    else:
        res = s

    if backslash:
        res = res.replace("\\\\", "\\")
    return res


def find_in_PATH(prog):
    """
    look into every path mentioned in ``%PATH%`` a specific file,
    it raises an exception if not Found

    @param      prog        program to look for
    @return                 path

    .. versionadded:: 0.9
    """
    path = os.environ["PATH"]
    for p in path.split(";"):
        f = os.path.join(p, prog)
        if os.path.exists(f):
            return p
    return None


def find_graphviz_dot():
    """
    determines the path to graphviz (on Windows),
    the function tests the existence of versions 34 to 45
    assuming it was installed in a standard folder: ``C:\Program Files\MiKTeX 2.9\miktex\bin\x64``

    @return         path to dot

    :raises FileNotFoundError: if graphviz not found

    .. versionadded:: 0.9
    """
    if sys.platform.startswith("win"):
        version = range(34, 45)
        for v in version:
            graphviz_dot = r"C:\Program Files (x86)\Graphviz2.{0}\bin\dot.exe".format(
                v)
            if os.path.exists(graphviz_dot):
                return graphviz_dot
        p = find_in_PATH("dot.exe")
        if p is None:
            typstr = str  # unicode#
            raise FileNotFoundError(
                "unable to find graphviz, look into paths such as: " + typstr(graphviz_dot))
        else:
            return os.path.join(p, "dot.exe")
    else:
        # linux
        return "dot"


def find_latex_path():
    """
    @return ``C:\Program Files\MiKTeX 2.9\miktex\bin\x64``

    :raises FileNotFoundError: if latex not found

    .. versionadded:: 0.9
    """
    if sys.platform.startswith("win"):
        latex = latex0 = r"C:\Program Files\MiKTeX 2.9\miktex\bin\x64"
        if not os.path.exists(latex):
            latex = find_in_PATH("latex.exe")
            if latex is None or not os.path.exists(latex):
                typstr = str  # unicode#
                raise FileNotFoundError(
                    "unable to find latex (miktex), look into paths such as: " + typstr(latex0))
        return latex
    else:
        # linux
        return ""


def find_pandoc_path():
    """
    determines pandoc location

    @return         path to pandoc

    .. versionadded:: 0.9
    """
    if sys.platform.startswith("win"):
        path = os.environ["USERPROFILE"]
        pandoc = os.path.join(path, "AppData", "Local", "Pandoc")
        tries = [pandoc]
        if not os.path.exists(pandoc):
            # we try others users because pandoc goes into a user folder by
            # default
            root = os.path.normpath(os.path.join(path, ".."))
            users = os.listdir(root)
            for u in users:
                p = os.path.join(root, u)
                if os.path.isdir(p):
                    pandoc = os.path.join(p, "AppData", "Local", "Pandoc")
                    if os.path.exists(pandoc):
                        return pandoc
                    tries.append(pandoc)
            pandoc = find_in_PATH("pandoc.exe")
            if pandoc is None:
                raise FileNotFoundError(
                    "unable to find pandoc, look into paths such as:\n" + "\n".join(tries))
            else:
                return pandoc
        else:
            return pandoc
    else:
        # linux
        return ""


def example_function_latex():
    """
    This function only contains an example with latex to check it is working fine.

    @example(How to display a formula)

    We want to check this formula to successfully converted.

    :math:`\\left \\{ \\begin{array}{l} \\min_{x,y} \\left \\{ x^2 + y^2 - xy + y \\right \\}  \\\\ \\text{sous contrainte} \\; x + 2y = 1 \\end{array}\\right .`

    Brackets and baskslash might be an issue.

    @endexample
    """
    pass
