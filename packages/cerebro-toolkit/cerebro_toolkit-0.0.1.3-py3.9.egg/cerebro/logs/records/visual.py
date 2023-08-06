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

import cv2
import base64
import numpy as np
from string import Template
from io import BytesIO as StringIO


def render_opencv(image, fmt="jpg"):
    """
    Render OpenCV image to base64.
    :param image:   given image.
    :param fmt:     image format.
    :return:        rendered image.
    """
    if not isinstance(image, np.ndarray):
        return None
    if image.shape[0] > 800:
        image = cv2.resize(image, [800, int(800 * image.shape[1] / image.shape[0])])
    if image.shape[1] > 800:
        image = cv2.resize(image, [int(800 * image.shape[0] / image.shape[1]), 800])
    val, buf = cv2.imencode(".%s" % fmt, image)
    return None if not val else buf, "image/%s" % fmt


def render_pil(image, fmt="jpg"):
    """
    Render PIL Image to base64.
    :param image:   given image.
    :param fmt:     image format.
    :return:        rendered image.
    """
    if not callable(getattr(image, "save", None)):
        return None
    output = StringIO()
    image.save(output, format=fmt)
    contents = output.getvalue()
    output.close()
    return contents, "image/%s" % fmt


def render_pylab(figure, fmt="jpg"):
    """
    Render figure to base64 image.
    :param figure:  given figure.
    :param fmt:     image format.
    :return:        rendered image.
    """
    if not callable(getattr(figure, "savefig", None)):
        return None
    output = StringIO()
    figure.savefig(output, format=fmt)
    contents = output.getvalue()
    output.close()
    return contents, "image/%s" % fmt


RENDERERS = [render_opencv, render_pil, render_pylab]


class VisualRecord(object):
    """
    This class is used to write visual log record.
    ---------
    @author:    Hieu Pham.
    @created:   20.10.2021.
    @updated:   20.10.2021.
    """

    def __init__(self, title="", images=None, content="", fmt="jpg"):
        """
        Create new object
        :param title:   title of log.
        :param images:  image of log.
        :param content: content of log.
        :param fmt:     image format.
        """
        self.title = title
        self.fmt = fmt
        # Assign image.
        if images is None:
            images = []
        self.images = images
        # Validate images.
        if not isinstance(images, (list, tuple, set, frozenset)):
            self.images = [self.images]
        # Assign footnotes.
        self.footnotes = content

    def __str__(self):
        """
        Get presentation string of object.
        :return:    string
        """
        t = Template(
            """
            <h4>$title</h4>
            $imgs
            $footnotes
            <hr/>""")
        # Return result.
        return t.substitute({
            "title": self.title,
            "imgs": self.render_images(),
            "footnotes": self.render_footnotes()
        })

    def render_images(self, no_html=False):
        """
        Render given images.
        :param no_html: no render html.
        :return:        rendered images.
        """
        rendered = []
        # Render images.
        for image in self.images:
            for renderer in RENDERERS:
                # Trying renderers we have one by one
                res = renderer(image, self.fmt)
                if res is None:
                    continue
                else:
                    rendered.append(res)
                    break
        # Return result.
        return "".join(
            Template('<img src="data:$mime;base64,$data" />').substitute({
                "data": base64.b64encode(data).decode(),
                "mime": mime
            }) for data, mime in rendered) if not no_html else [(np.squeeze(data), mine) for data, mine in rendered]

    def render_footnotes(self):
        """
        Render footnotes.
        :return:    rendered content.
        """
        if not self.footnotes:
            return ""
        # Return result.
        return Template("<pre>$footnotes</pre>").substitute({
            "footnotes": self.footnotes
        })
