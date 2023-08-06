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

from typing import Any
from cerebro.objects import MetaObject


class Stack(MetaObject):
    """
    Stack is an implementation of first in last out structure.
    ---------
    @author:    Hieu Pham.
    @created:   13.10.2021.
    @updated:   20.10.2021.
    """

    @property
    def size(self):
        """
        Get stack size.
        :return: size.
        """
        return len(self._stack)

    def __init__(self, **kwargs):
        """
        Create new object.
        :param kwargs:  keyword arguments.
        """
        self._stack = list()
        super(Stack, self).__init__(**kwargs)

    def push(self, obj: Any = None, **kwargs):
        """
        Push object into stack.
        :param obj:     object to be pushed.
        :param kwargs:  keyword arguments.
        :return:        object.
        """
        if obj is not None:
            self.lock.acquire()
            self._stack.append(obj)
            self.lock.release()
            return obj

    def pop(self, **kwargs):
        """
        Pop object from stack.
        :param kwargs:  keyword arguments.
        :return:        object.
        """
        self.lock.acquire()
        result = self._stack.pop()
        self.lock.release()
        return result

    def get(self, index: int = 0):
        """
        Get item based on index.
        :param index:   index.
        :return:        item.
        """
        return self._stack[index]

    def clean(self, **kwargs):
        """
        Pop all objects from stack.
        :param kwargs:  keyword arguments.
        :return:        object.
        """
        self.lock.acquire()
        result = [self._stack.pop() for i in range(len(self._stack))]
        self.lock.release()
        return result
