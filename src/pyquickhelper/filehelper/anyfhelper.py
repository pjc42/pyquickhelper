"""
@file
@brief      Various helpers about files

.. versionadded:: 1.1
"""

import os
import io
import stat
import sys
import warnings
from .synchelper import explore_folder_iterfile
from .internet_helper import read_url

if sys.version_info[0] == 2:
    from codecs import open


def change_file_status(folder, status=stat.S_IWRITE, strict=False,
                       include_folder=True):
    """
    change the status of all files inside a folder

    @param      folder          folder or file
    @param      status          new status
    @param      strict          False, use ``|=``, True, use ``=``
    @param      include_folder  change the status of the folders as well
    @return                     list of modified files

    By default, status is ``stat.S_IWRITE``.
    If *folder* is a file, the function changes the status of this file,
    otherwise, it will change the status of every file the folder contains.
    """
    if os.path.isfile(folder):
        if include_folder:
            dirname = os.path.dirname(folder)
            todo = [dirname, folder]
        else:
            todo = [folder]
        res = []

        for f in todo:
            mode = os.stat(f).st_mode
            if strict:
                nmode = status
                if nmode != mode:
                    os.chmod(f, nmode)
                    res.append(f)
            else:
                nmode = mode | stat.S_IWRITE
                if nmode != mode:
                    os.chmod(f, nmode)
                    res.append(f)
        return res
    else:
        res = []
        dirname = set()
        if strict:
            for f in explore_folder_iterfile(folder):
                if include_folder:
                    d = os.path.dirname(f)
                    if d not in dirname:
                        dirname.add(d)
                        mode = os.stat(d).st_mode
                        nmode = status
                        if nmode != mode:
                            os.chmod(d, nmode)
                            res.append(d)
                try:
                    mode = os.stat(f).st_mode
                except FileNotFoundError:
                    # it appends for some weird path
                    # GitHub\pyensae\src\pyensae\file_helper\pigjar\pig-0.14.0\contrib\piggybank\java\build\classes\org\apache\pig\piggybank\storage\IndexedStorage$IndexedStorageInputFormat$IndexedStorageRecordReader$IndexedStorageRecordReaderComparator.class
                    warnings.warn("[change_file_status] unable to find " + f)
                    continue
                nmode = status
                if nmode != mode:
                    os.chmod(f, nmode)
                    res.append(f)

            # we end up with the folder
            if include_folder:
                d = folder
                if d not in dirname:
                    mode = os.stat(d).st_mode
                    nmode = status
                    if nmode != mode:
                        os.chmod(d, nmode)
                        res.append(d)
        else:
            for f in explore_folder_iterfile(folder):
                if include_folder:
                    d = os.path.dirname(f)
                    if d not in dirname:
                        dirname.add(d)
                        mode = os.stat(d).st_mode
                        nmode = mode | stat.S_IWRITE
                        if nmode != mode:
                            os.chmod(d, nmode)
                            res.append(d)
                try:
                    mode = os.stat(f).st_mode
                except FileNotFoundError:
                    # it appends for some weird path
                    warnings.warn("[change_file_status] unable to find " + f)
                    continue
                nmode = mode | stat.S_IWRITE
                if nmode != mode:
                    os.chmod(f, nmode)
                    res.append(f)

            # we end up with the folder
            if include_folder:
                d = folder
                if d not in dirname:
                    mode = os.stat(d).st_mode
                    nmode = mode | stat.S_IWRITE
                    if nmode != mode:
                        os.chmod(d, nmode)
                        res.append(d)
        return res


def read_content_ufs(file_url_stream, encoding="utf8"):
    """
    read the content of a source, whether it is a url, a file, a stream
    or a string (in that case, it returns the string itself),
    we assume the content type is text

    @param      file_url_stream     file or url or stream or string
    @param      encoding            encoding
    @return                         content of the source (str)
    """
    if isinstance(file_url_stream, str  # unicode#
                  ):
        if len(file_url_stream) < 5000 and os.path.exists(file_url_stream):
            with open(file_url_stream, "r", encoding=encoding) as f:
                return f.read()
        elif len(file_url_stream) < 5000 and file_url_stream.startswith("http"):
            return read_url(file_url_stream, encoding=encoding)
        else:
            return file_url_stream
    elif isinstance(file_url_stream, io.StringIO):
        return file_url_stream.getvalue()
    elif isinstance(file_url_stream, io.BytesIO):
        return file_url_stream.getvalue().decode(encoding=encoding)
    else:
        raise TypeError(
            "unexpected type for file_url_stream: {0}".format(type(file_url_stream)))
