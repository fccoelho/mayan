"""Configuration options for the ocr app"""

from django.utils.translation import ugettext_lazy as _

from smart_settings.api import register_settings

register_settings(
    namespace=u'ocr',
    module=u'ocr.conf.settings',
    settings=[
        {'name': u'TESSERACT_PATH', 'global_name': u'OCR_TESSERACT_PATH', 'default': u'/usr/bin/tesseract', 'exists': True},
        {'name': u'TESSERACT_LANGUAGE', 'global_name': u'OCR_TESSERACT_LANGUAGE', 'default': u'eng'},
        {'name': u'REPLICATION_DELAY', 'global_name': u'OCR_REPLICATION_DELAY', 'default': 10, 'description': _(u'Amount of seconds to delay OCR of documents to allow for the node\'s storage replication overhead.')},
        {'name': u'NODE_CONCURRENT_EXECUTION', 'global_name': u'OCR_NODE_CONCURRENT_EXECUTION', 'default': 1, 'description': _(u'Maximum amount of concurrent document OCRs a node can perform.')},
        {'name': u'AUTOMATIC_OCR', 'global_name': u'OCR_AUTOMATIC_OCR', 'default': False, 'description': _(u'Automatically queue newly created documents for OCR.')},
        {'name': u'QUEUE_PROCESSING_INTERVAL', 'global_name': u'OCR_QUEUE_PROCESSING_INTERVAL', 'default': 10},
        {'name': u'CACHE_URI', 'global_name': u'OCR_CACHE_URI', 'default': None, 'description': _(u'URI in the form: "memcached://127.0.0.1:11211/" to specify a cache backend to use for locking. Multiple hosts can be specified separated by a semicolon.')},
        {'name': u'UNPAPER_PATH', 'global_name': u'OCR_UNPAPER_PATH', 'default': u'/usr/bin/unpaper', 'description': _(u'File path to unpaper program.'), 'exists': True},
    ]
)
