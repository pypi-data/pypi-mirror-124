# ------------------------------------------------------------------------------
#  MIT License
#
#  Copyright (c) 2021 Hieu Pham. All rights reserved.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
# ------------------------------------------------------------------------------

import os
import shutil
from copy import copy
from datetime import datetime
from pathlib import Path as BasePath


class Path:
    """
    This class is used to handle a path.
    ---------
    @author:    Hieu Pham.
    @created:   19.10.2021.
    @updated:   20.10.2021.
    """

    def __init__(self, path: str = None, **kwargs):
        """
        Created new object.
        :param path:    given path.
        :param kwargs:  keyword arguments.
        """
        super().__init__()
        self._path = BasePath(os.path.expanduser(path))

    def __str__(self):
        """
        Get string represent of path.
        :return:    path string.
        """
        return str(self._path)

    def insert(self, index, candidate, **kwargs):
        """
        Insert a candidate into current path.
        :param index:       index to insert.
        :param candidate:   candidate to insert.
        :param kwargs:      keyword arguments.
        :return:            path object.
        """
        parts = list(self._path.parts)
        parts.insert(index, candidate)
        self._path = BasePath(*parts)
        return self

    def remove(self, index, **kwargs):
        """
        Remove a candidate from current path.
        :param index:   index to be removed.
        :param kwargs:  keyword arguments.
        :return:        path object.
        """
        parts = list(self._path.parts)
        parts.pop(index)
        self._path = BasePath(*parts)
        return self

    def change(self, index, candidate, **kwargs):
        """
        Change a part of path with a candidate.
        :param index:       index to be replaced.
        :param candidate:   candidate to replace.
        :param kwargs:      keyword arguments.
        :return:            path object.
        """
        parts = list(self._path.parts)
        parts[index] = candidate
        self._path = BasePath(*parts)
        return self

    def with_suffix(self, suffix: str = None):
        """
        Replace suffix with another.
        :param suffix:  desired suffix.
        :return:        path object.
        """
        if suffix is not None:
            self._path = self._path.with_suffix(suffix)
        return self

    def unique(self, **kwargs):
        """
        Insert unique number to suffix to prevent duplicate.
        :param kwargs:  keyword arguments.
        :return:        path object.
        """
        count = 0
        while True:
            stem = '%s-%s' % (self._path.stem, count) if count > 0 else self._path.stem
            new_path = copy(self._path)
            new_path.with_stem(stem)
            if new_path.is_dir() or new_path.is_file():
                count += 1
                continue
            self._path = new_path
            return self

    def datetime(self, formats: str = '-%Y-%m-%d-%H-%M-%S', **kwargs):
        """
        Insert datetime to suffix to prevent duplicate.
        :param formats: string format of time.
        :param kwargs:  keyword arguments.
        :return:        path object.
        """
        stem = '%s-%s' % (self._path.stem, datetime.now().strftime(formats))
        self._path = self._path.with_stem(stem)
        return self

    def mkdir(self, **kwargs):
        """
        Make sure the directory is exist.
        :param kwargs:  additional keyword arguments.
        :return:        none.
        """
        if len(self._path.suffixes) == 0:
            os.makedirs(self._path, exist_ok=True)
        else:
            os.makedirs(self._path.parent, exist_ok=True)
        return self

    def copy(self, dst=None, **kwargs):
        """
        Copy file or directory of this path to a desired destination.
        :param dst:     desired destination.
        :param kwargs:  additional keyword arguments.
        :return:        none.
        """
        assert isinstance(dst, Path), 'Destination must be a path object.'
        # In case both of source and destination is directory.
        if len(self._path.suffixes) == 0 and len(dst._path.suffixes) == 0:
            shutil.copytree(str(self), str(dst))
        # In case both of source and destination is file.
        if len(self._path.suffixes) != 0 and len(dst._path.suffixes) != 0:
            shutil.copy2(str(self), str(dst))
        # Otherwise, raise error.
        raise IOError('Source and destination are not same type.')

    def move(self, dst=None, **kwargs):
        """
        Move file or directory of this path to a desired destination.
        :param dst:     desired destination.
        :param kwargs:  additional keyword arguments.
        :return:        none.
        """
        assert isinstance(dst, Path), 'Destination must be a path object.'
        shutil.move(str(self), str(dst))

    def rm(self, **kwargs):
        """
        Remove file or directory of this path.
        :param kwargs:  additional keyword arguments.
        :return:        none.
        """
        if self._path.is_file():
            os.remove(str(self))
        else:
            shutil.rmtree(str(self))
