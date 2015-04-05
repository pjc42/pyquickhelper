# -*- coding: utf-8 -*-
"""
@file
@brief Helpers to process blog post included in the documentation.
"""

import os
from docutils import io as docio
from docutils.core import publish_programmatically


class BlogPostPareError(Exception):

    """
    exceptions when a error comes after a blogpost was parsed
    """
    pass


class BlogPost:

    """
    defines a blog post,
    """

    def __init__(self, filename, encoding="utf-8-sig"):
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
                content = f.read()
            self._filename = filename
        else:
            content = filename
            self._filename = None

        self._raw = content

        overrides = {}
        overrides['input_encoding'] = encoding
        overrides["out_blogpostlist"] = []
        
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
            raise BlogPostPareError('no blog post (#={1}) in\n  File "{0}", line 1'.format(filename, len(objects)))

        post = objects[0]
        for k in post.options:
            setattr(self, k, post.options[k])
        self.rst_obj = post
        self.pub = pub
        self._content = post.content

    @property
    def Fields(self):
        """
        return the fields as a dictionary
        """
        return dict(title=self.title,
                    date=self.date,
                    keywords=self.Keywords,
                    categories=self.Categories)

    @property
    def Tag(self):
        """
        produces a tag for the blog post
        """
        return "post-" + self.Date + "-" + \
               "".join([c for c in self.Title.lower() if "a" <= c <= "z"])

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
    def Date(self):
        """
        return the date
        """
        return self.date

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

    def post_as_rst(self, directive="blogpostagg"):
        """
        reproduces the text of the blog post

        @return         blog post as RST
        """
        rows = []
        rows.append(".. %s::" % directive)
        for f, v in self.Fields.items():
            if isinstance(v, str):
                rows.append("    :%s: %s" % (f, v))
            else:
                rows.append("    :%s: %s" % (f, ",".join(v)))
        rows.append("")
        for r in self.Content:
            rows.append("    " + r)
        return "\n".join(rows)
