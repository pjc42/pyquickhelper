# -*- coding: utf-8 -*-
"""
@file
@brief Helpers to process blog post included in the documentation.
"""

import os
import sys
from docutils import io as docio
from docutils.core import publish_programmatically

if sys.version_info[0] == 2:
    from codecs import open


class BlogPostPareError(Exception):

    """
    exceptions when a error comes after a blogpost was parsed
    """
    pass


class BlogPost:

    """
    defines a blog post,
    """

    def __init__(self, filename, encoding="utf8"):
        """
        create an instance of a blog post from a file or a string

        @param      filename        filename or string
        @param      encoding        encoding

        The constructor creates the following members:

        * title
        * date
        * keywords
        * categories
        * _filename
        * _raw
        * rst_obj: the object generated by docutils (@see cl BlogPostDirective)
        * pub: Publisher

        """
        if os.path.exists(filename):
            with open(filename, "r", encoding=encoding) as f:
                try:
                    content = f.read()
                except UnicodeDecodeError as e:
                    raise Exception(
                        'unable to read filename (encoding issue):\n  File "{0}", line 1'.format(filename)) from e
            self._filename = filename
        else:
            content = filename
            self._filename = None

        self._raw = content

        overrides = {}
        overrides['input_encoding'] = encoding
        overrides["out_blogpostlist"] = []
        overrides["blog_background"] = False

        output, pub = publish_programmatically(
            source_class=docio.StringInput,
            source=content,
            source_path=None,
            destination_class=docio.StringOutput,
            destination=None,
            destination_path=None,
            reader=None,
            reader_name='standalone',
            parser=None,
            parser_name='restructuredtext',
            writer=None,
            writer_name='null',
            settings=None,
            settings_spec=None,
            settings_overrides=overrides,
            config_section=None,
            enable_exit_status=None)

        #document = pub.writer.document
        objects = pub.settings.out_blogpostlist

        if len(objects) != 1:
            raise BlogPostPareError(
                'no blog post (#={1}) in\n  File "{0}", line 1'.format(filename, len(objects)))

        post = objects[0]
        for k in post.options:
            setattr(self, k, post.options[k])
        self.rst_obj = post
        self.pub = pub
        self._content = post.content

    def __cmp__(self, other):
        """
        This method avoids to get the following error
        ``TypeError: unorderable types: BlogPost() < BlogPost()``

        @param      other       other @see cl BlogPost
        @return                 -1, 0, or 1
        """
        if self.Date < other.Date:
            return -1
        elif self.Date > other.Date:
            return 1
        else:
            if self.Tag < other.Tag:
                return -1
            elif self.Tag > other.Tag:
                return 1
            else:
                raise Exception(
                    "same tag for two BlogPost: {0}".format(self.Tag))

    def __lt__(self, other):
        """
        Tells if this blog should be placed before *other*.
        """
        if self.Date < other.Date:
            return True
        elif self.Date > other.Date:
            return False
        else:
            if self.Tag < other.Tag:
                return True
            else:
                return False

    @property
    def Fields(self):
        """
        return the fields as a dictionary
        """
        res = dict(title=self.title,
                   date=self.date,
                   keywords=self.Keywords,
                   categories=self.Categories)
        if self.BlogBackground is not None:
            res["blog_ground"] = self.BlogBackground
        if self.Author is not None:
            res["author"] = self.Author
        return res

    @property
    def Tag(self):
        """
        produces a tag for the blog post
        """
        return BlogPost.build_tag(self.Date, self.Title)

    @staticmethod
    def build_tag(date, title):
        """
        builds the tag for a post

        @param      date        date
        @param      title       title
        @return                 tag or label
        """
        return "post-" + date + "-" + \
               "".join([c for c in title.lower() if "a" <= c <= "z"])

    @property
    def FileName(self):
        """
        return the filename
        """
        return self._filename

    @property
    def Title(self):
        """
        return the title
        """
        return self.title

    @property
    def BlogBackground(self):
        """
        return the blog background or None if not defined
        """
        return self.blog_ground if hasattr(self, "blog_ground") else None

    @property
    def Author(self):
        """
        return the author or None if not defined
        """
        return self.author if hasattr(self, "author") else None

    @property
    def Date(self):
        """
        return the date
        """
        return self.date

    @property
    def Year(self):
        """
        return the year, we assume self.date is a string YYYY-MM-DD
        """
        return self.date[:4]

    @property
    def Keywords(self):
        """
        return the keywords
        """
        return [_.strip() for _ in self.keywords.split(",")]

    @property
    def Categories(self):
        """
        return the categories
        """
        return [_.strip() for _ in self.categories.split(",")]

    @property
    def Content(self):
        """
        return the content of the blogpost
        """
        return self._content

    def post_as_rst(self, language, directive="blogpostagg"):
        """
        reproduces the text of the blog post,
        updates the image links

        @param      language    language
        @param      directive   to specify a different behavior based on
        @return                 blog post as RST
        """
        rows = []
        rows.append(".. %s::" % directive)
        for f, v in self.Fields.items():
            if isinstance(v, str):
                rows.append("    :%s: %s" % (f, v))
            else:
                rows.append("    :%s: %s" % (f, ",".join(v)))
        if self._filename is not None:
            spl = self._filename.replace("\\", "/").split("/")
            name = "/".join(spl[-2:])
            rows.append("    :rawfile: %s" % name)
        rows.append("")

        if directive == "blogpostagg":
            for r in self.Content:
                rows.append("    " + self._update_link(r))
        else:
            for r in self.Content:
                rows.append("    " + r)

        rows.append("")
        rows.append("")

        # this is done in depart_blogpostagg_node
        # if directive=="blogpostagg":
        #    rows.append("    :ref:`{1} <{0}>`".format(self.Tag, TITLES[language]["more"]))
        #    rows.append("")
        #    rows.append("")

        return "\n".join(rows)

    image_tag = ".. image:: "

    def _update_link(self, row):
        """
        changes a link to an image if the page contains one into
        *year/img.png*

        @param      row     row
        @return             new row
        """
        r = row.strip("\r\t ")
        if r.startswith(BlogPost.image_tag):
            i = len(BlogPost.image_tag)
            r2 = row[i:]
            if "/" in r2:
                return row
            row = "{0}{1}/{2}".format(row[:i], self.Year, r2)
            return row
        else:
            return row
