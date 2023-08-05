# -*- coding: utf-8 -*-
""" fhcore.utils.image_serve
    @author: Frankhood Business Solutions
    @created: 04 apr 2018
"""
from __future__ import absolute_import, print_function, unicode_literals
import logging
import mimetypes
import os
import posixpath
import stat

from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from django.http import (StreamingHttpResponse, Http404,
                         HttpResponse, HttpResponseRedirect, HttpResponseNotModified)
from django.utils.http import http_date, parse_http_date
from django.views.static import was_modified_since, directory_index

try:
    from urllib.parse import unquote
except ImportError:  # Python 2
    from urllib import unquote

logger = logging.getLogger(__name__)


def image_serve(request, path, document_root=None, show_indexes=False):
    """
    Reimplementation of django.views.static.serve function
    The difference with the django.views.static.serve function is that
    it uses mimetype image/jpeg as default and not octet/stream...
    """
    path = posixpath.normpath(unquote(path))
    path = path.lstrip('/')
    newpath = ''
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        _drive, part = os.path.splitdrive(part)
        _head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        newpath = os.path.join(newpath, part).replace('\\', '/')
    if newpath and path != newpath:
        return HttpResponseRedirect(newpath)
    fullpath = os.path.join(document_root, newpath)
    if os.path.isdir(fullpath):
        if show_indexes:
            return directory_index(newpath, fullpath)
        raise Http404(_("Directory indexes are not allowed here."))
    if not os.path.exists(fullpath):
        raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
    # Respect the If-Modified-Since header.
    statobj = os.stat(fullpath)
    mimetype, encoding = mimetypes.guess_type(fullpath)
    mimetype = mimetype or 'image/jpeg'
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    response = StreamingHttpResponse(open(fullpath, 'rb'), content_type=mimetype)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if stat.S_ISREG(statobj.st_mode):
        response["Content-Length"] = statobj.st_size
    if encoding:
        response["Content-Encoding"] = encoding
    return response
