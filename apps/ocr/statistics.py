from django.utils.translation import ugettext as _

#from ocr.models import DocumentQueue, QueueDocument
from ocr.api import ocr_queue


def get_statistics():
    paragraphs = [
        _(u'Queued documents: %d') % ocr_queue.count()
    ]

    return {
        'title': _(u'OCR statistics'),
        'paragraphs': paragraphs
    }
