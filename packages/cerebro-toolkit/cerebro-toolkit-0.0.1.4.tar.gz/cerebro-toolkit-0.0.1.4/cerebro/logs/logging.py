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
import io
import sys
import base64
import logging
from cerebro.io import Path
from cerebro.designs import Singleton
from .records import VisualRecord
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
from PIL import Image



# Store supported log levels.
LOG_LEVELS = {'none': logging.NOTSET, 'info': logging.INFO, 'debug': logging.DEBUG, 'warning': logging.WARNING,
              'error': logging.ERROR, 'critical': logging.CRITICAL}

# Default log format.
FORMAT = '%(asctime)s: %(levelname)s: %(message)s'

# Define logger name.
DEFAULT_LOGGER = 'cerebro_logger'
VISUAL_LOGGER = 'cerebro_visual_logger'


class Logging(metaclass=Singleton):
    """

    """

    @staticmethod
    def get_env_level():
        """
        Get log level from os environment.
        :return:    log level.
        """
        level = os.environ.get('DEBUG', 'none').lower()
        return LOG_LEVELS[level] if level in LOG_LEVELS else LOG_LEVELS['none']

    def __init__(self,
                 level=None,
                 log_dir: str = os.path.join(os.getcwd(), 'logs'),
                 log_file: str = 'log.txt',
                 fmt: str = FORMAT,
                 **kwargs):
        """
        Create new object.
        :param level:       log level.
        :param log_dir:     log directory.
        :param log_file:    log file.
        :param fmt:         log format.
        """
        super(Logging, self).__init__()
        self._filepath = None
        self._level = None
        self.setup(level, log_dir, log_file, fmt, **kwargs)

    def setup(self,
              level=None,
              log_dir: str = os.path.join(os.getcwd(), 'logs'),
              log_file: str = 'log.txt',
              fmt: str = FORMAT,
              **kwargs):
        """
        Setup the logging.
        :param level:       log level.
        :param log_dir:     log directory.
        :param log_file:    log file.
        :param fmt:         log format.
        :param kwargs:      keyword arguments.
        :return:            none.
        """
        level = os.environ.get('DEBUG', 'none').lower() if level is None else level
        level = LOG_LEVELS[level] if level in LOG_LEVELS else LOG_LEVELS['none']
        self._level = level
        # Initialize
        formatter = logging.Formatter(fmt)
        self._filepath = Path(os.path.join(log_dir, log_file))
        # Initialize logger.
        logger = logging.getLogger(DEFAULT_LOGGER)
        logger.setLevel(level)
        logger.handlers.clear()
        # Add console handler.
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        # Add file handler.
        file_handler = logging.FileHandler(str(self._filepath.mkdir()), delay=True)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        # Initialize visual logger.
        visual_logger = logging.getLogger(VISUAL_LOGGER)
        visual_logger.setLevel(level)
        visual_logger.handlers.clear()
        # Add visual handler
        visual_handler = logging.FileHandler(str(self._filepath.mkdir().with_suffix('.html')), delay=True)
        visual_logger.addHandler(visual_handler)
        # Return result.
        return self

    @staticmethod
    def make_visual_log(title="", images=None, content="", fmt="jpg"):
        """
        Create a visual record for visual logging.
        :param title:   title of record.
        :param images:  images of record.
        :param content: content of record.
        :param fmt:     image format.
        :return:        visual record.
        """
        return VisualRecord(title, images, content, fmt)

    def info(self, msg):
        """
        Write info log.
        :param msg: message.
        :return:    logging.
        """
        if isinstance(msg, VisualRecord):
            logging.getLogger(VISUAL_LOGGER).info(str(msg))
            if self._level == logging.INFO:
                for image in msg.images:
                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_title(msg.footnotes, wrap=True)
                    ax.imshow(image)
                    fig.show()
        else:
            logging.getLogger(DEFAULT_LOGGER).info(str(msg))
        return self

    def debug(self, msg):
        """
        Write debug log.
        :param msg: message.
        :return:    logging.
        """
        if isinstance(msg, VisualRecord):
            logging.getLogger(VISUAL_LOGGER).debug(str(msg))
            if self._level == logging.DEBUG:
                for image in msg.images:
                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_title(msg.footnotes, wrap=True)
                    ax.imshow(image)
                    fig.show()
        else:
            logging.getLogger(DEFAULT_LOGGER).debug(str(msg))
        return self

    def warning(self, msg):
        """
        Write warning log.
        :param msg: message.
        :return:    logging.
        """
        if isinstance(msg, VisualRecord):
            logging.getLogger(VISUAL_LOGGER).warning(str(msg))
            if self._level == logging.WARNING:
                for image in msg.images:
                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_title(msg.footnotes, wrap=True)
                    ax.imshow(image)
                    fig.show()
        else:
            logging.getLogger(DEFAULT_LOGGER).warning(str(msg))
        return self

    def error(self, msg):
        """
        Write error log.
        :param msg: message.
        :return:    logging.
        """
        if isinstance(msg, VisualRecord):
            logging.getLogger(VISUAL_LOGGER).error(str(msg))
            if self._level == logging.ERROR:
                for image in msg.images:
                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_title(msg.footnotes, wrap=True)
                    ax.imshow(image)
                    fig.show()
        else:
            logging.getLogger(DEFAULT_LOGGER).error(str(msg))
        return self

    def critical(self, msg):
        """
        Write critical log.
        :param msg: message.
        :return:    logging.
        """
        if isinstance(msg, VisualRecord):
            logging.getLogger(VISUAL_LOGGER).critical(str(msg))
            if self._level == logging.CRITICAL:
                for image in msg.images:
                    fig = plt.figure()
                    ax = fig.add_subplot(1, 1, 1)
                    ax.set_title(msg.footnotes, wrap=True)
                    ax.imshow(image)
                    fig.show()
        else:
            logging.getLogger(DEFAULT_LOGGER).critical(str(msg))
        return self
