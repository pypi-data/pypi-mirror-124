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

from abc import ABCMeta
from threading import RLock


class MetaClass(ABCMeta):
    """
    The meta class will be used to control python object at low level.
    ---------
    @author:    Hieu Pham.
    @created:   10.10.2021.
    @updated:   20.10.2021.
    """
    pass


class MetaObject(metaclass=MetaClass):
    """
    The meta object is low level object of all inherited objects.
    ---------
    @author:    Hieu Pham.
    @created:   10.10.2021.
    @updated:   20.10.2021.
    """

    @property
    def name(self):
        """
        Get object name.
        :return: object name.
        """
        return self._name

    @name.setter
    def name(self, value: str = None):
        """
        Set object name.
        :param value: given name.
        :return:      none.
        """
        self._name = value

    @property
    def data(self):
        """
        Get object data.
        :return: object data.
        """
        return self.__data__()

    @property
    def lock(self):
        """
        Get thread locking.
        :return: thread locking.
        """
        return self._lock

    def __init__(self, name: str = None, **kwargs):
        """
        Create new object.
        :param name:    object name.
        :param kwargs:  keyword arguments.
        """
        self._name = name
        self._lock = RLock()
        super(MetaObject, self).__init__()

    def __data__(self, **kwargs) -> dict:
        """
        Generate object data.
        :param kwargs:  keyword arguments.
        :return:        object data.
        """
        data = {'classname': self.__class__.__name__, 'module': self.__module__}
        if self._name is not None:
            data.update({'name': self._name})
        return data
