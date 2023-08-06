# -*- coding: utf-8 -*-
"""  frankhood.fhcore.views.view_mixins.py
    @author: Frankhood Business Solutions
    @date : 20/set/2013
"""
import csv
import json
import os
import  logging
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.list import BaseListView
from django.views.static import serve

__all__ = [
    'TXTResponseMixin',
    'PDFResponseMixin',
    'CSVResponseMixin',
    'FileResponseServeMixin',
    'ImageResponseServeMixin',
]

logger = logging.getLogger(__name__)

from response_view_mixin.utils import image_serve


# ===============================================================================
# TXT
# ===============================================================================
class TXTResponseMixin(object):
    file_name = None
    file_mimetype = 'text/plain'

    def get_file_name(self):
        return self.file_name

    def get_file_mimetype(self):
        return self.file_mimetype

    def build_response(self, response, context):
        for row in context['rows']:
            response.write("%s\n" % row)
        return response

    def render_to_response(self, context, **response_kwargs):
        """
        Genera una risposta nel mimetype selezionato.
        """
        file_name = self.get_file_name()
        file_mimetype = self.get_file_mimetype()
        if not file_name:
            raise Exception("Manca il nome del file")
        response = HttpResponse(content_type=file_mimetype)
        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        response = self.build_response(response, context)
        return response


# ===============================================================================
# PDF
# ===============================================================================
class PDFResponseMixin(object):
    file_name = None
    file_mimetype = "application/pdf"

    def get_file_name(self):
        return self.file_name

    def get_file_dir(self):
        # modifica se non è questo il path del file
        return os.path.join(settings.STATIC_ROOT, 'uploads', 'pdf')

    def render_to_response(self, context, **response_kwargs):
        file_path = "{0}{1}{2}".format(self.get_file_dir(), os.sep, self.get_file_name())
        with open(file_path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type=self.file_mimetype)
            response['Content-Disposition'] = 'inline;filename={0}'.format(self.get_file_name())
            return response


# ===============================================================================
# CSV
# ===============================================================================
class CSVResponseMixin(TXTResponseMixin):
    csv_delimiter = ";"
    file_mimetype = 'text/csv'

    def build_response(self, response, context):
        writer = csv.writer(response, delimiter=self.csv_delimiter)
        for row in context['rows']:
            writer.writerow([s.encode("utf-8") if isinstance(s, str) else s for s in row])
        return response


# ============================================================================
# FILES
# ============================================================================
class FileResponseServeMixin(object):
    use_private_storage = False

    """ Mixin che fa restituire un file invece di una HttpResponse """

    def get_file_path(self, **kwargs):
        raise NotImplementedError()

    def get_file_docroot(self, **kwargs):
        if self.use_private_storage:
            if not hasattr(settings, "PRIVATE_ROOT"):
                logger.error("Cannot use PRIVATE_FILE_SYSTEM without settings PRIVATE_ROOT")
                return settings.PROJECT_ROOT
            return settings.PRIVATE_ROOT
        else:
            return settings.PROJECT_ROOT

    def render_to_response(self, context, **response_kwargs):
        context = context or {}
        response = serve(self.request,
                         path=self.get_file_path(**context),
                         document_root=self.get_file_docroot())
        try:
            response['Content-Disposition'] = ('attachment; filename="{0}"'
                                               '').format(response.get('Content-Disposition',
                                                                       os.path.split(self.get_file_path(**context))[
                                                                           -1]))
        except Exception:
            logger.exception("")
        return response


class ImageResponseServeMixin(FileResponseServeMixin):
    """ Mixin che fa restituire un'immagine invece di una HttpResponse"""

    def render_to_response(self, context, **response_kwargs):
        context = context or {}
        # X l'immagine nn dobiamo scaricarla, quindi nn dobbiamo modificare l'header
        # scrivendo response['Content-Disposition'] = 'attachment; {0}'.format(response['Content-Disposition'])
        return image_serve(self.request,
                           path=self.get_file_path(**context),
                           document_root=self.get_file_docroot())
