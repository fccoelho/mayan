from django.utils.translation import ugettext_lazy as _

from navigation.api import register_links, register_top_menu, register_multi_item_links
from permissions.api import register_permission, set_namespace_title
from project_tools.api import register_tool

from queues.models import Queue, QueueItem


#Permissions
#PERMISSION_QUEUE_DOCUMENT = {'namespace': 'ocr', 'name': 'ocr_document', 'label': _(u'Submit document for OCR')}
#PERMISSION_OCR_QUEUE_DELETE = {'namespace': 'ocr', 'name': 'ocr_document_delete', 'label': _(u'Delete document for OCR queue')}
#PERMISSION_OCR_QUEUE_ENABLE_DISABLE = {'namespace': 'ocr', 'name': 'ocr_queue_enable_disable', 'label': _(u'Can enable/disable an OCR queue')}
#PERMISSION_OCR_CLEAN_ALL_PAGES = {'namespace': 'ocr', 'name': 'ocr_clean_all_pages', 'label': _(u'Can execute an OCR clean up on all document pages')}
#PERMISSION_OCR_QUEUE_EDIT = {'namespace': 'ocr_setup', 'name': 'ocr_queue_edit', 'label': _(u'Can edit an OCR queue properties')}

#set_namespace_title('ocr', _(u'OCR'))
#register_permission(PERMISSION_OCR_DOCUMENT)
#register_permission(PERMISSION_OCR_DOCUMENT_DELETE)
#register_permission(PERMISSION_OCR_QUEUE_ENABLE_DISABLE)
#register_permission(PERMISSION_OCR_CLEAN_ALL_PAGES)

#set_namespace_title('ocr_setup', _(u'OCR Setup'))
#register_permission(PERMISSION_OCR_QUEUE_EDIT)

#Links
#submit_document = {'text': _('submit to OCR queue'), 'view': 'submit_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
#re_queue_document = {'text': _('re-queue'), 'view': 're_queue_document', 'args': 'object.id', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
#re_queue_multiple_document = {'text': _('re-queue'), 'view': 're_queue_multiple_document', 'famfam': 'hourglass_add', 'permissions': [PERMISSION_OCR_DOCUMENT]}
queue_list = {'text': _(u'queues'), 'view': 'queue_list', 'famfam': 'hourglass', 'icon': 'hourglass.png'}#, 'permissions': [PERMISSION_OCR_ITEM_DELETE]}
queue_items = {'text': _(u'items'), 'view': 'queue_item_list', 'args': 'object.id', 'famfam': 'hourglass_go'}#, 'permissions': [PERMISSION_OCR_ITEM_DELETE]}
queue_item_delete = {'text': _(u'delete'), 'view': 'queue_item_delete', 'args': 'object.id', 'famfam': 'hourglass_delete'}#, 'permissions': [PERMISSION_OCR_ITEM_DELETE]}
queue_item_multiple_delete = {'text': _(u'delete'), 'view': 'queue_item_multiple_delete', 'famfam': 'hourglass_delete'}#, 'permissions': [PERMISSION_OCR_ITEM_DELETE]}

#document_queue_disable = {'text': _(u'stop queue'), 'view': 'document_queue_disable', 'args': 'queue.id', 'famfam': 'control_stop_blue', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}
#document_queue_enable = {'text': _(u'activate queue'), 'view': 'document_queue_enable', 'args': 'queue.id', 'famfam': 'control_play_blue', 'permissions': [PERMISSION_OCR_QUEUE_ENABLE_DISABLE]}

#all_document_ocr_cleanup = {'text': _(u'clean up pages content'), 'view': 'all_document_ocr_cleanup', 'famfam': 'text_strikethrough', 'permissions': [PERMISSION_OCR_CLEAN_ALL_PAGES], 'description': _(u'Runs a language filter to remove common OCR mistakes from document pages content.')}

#queue_document_list = {'text': _(u'queue document list'), 'view': 'queue_document_list', 'famfam': 'hourglass', 'permissions': [PERMISSION_OCR_DOCUMENT]}
#ocr_tool_link = {'text': _(u'OCR'), 'view': 'queue_document_list', 'famfam': 'hourglass', 'icon': 'text.png', 'permissions': [PERMISSION_OCR_DOCUMENT]}

#node_active_list = {'text': _(u'active tasks'), 'view': 'node_active_list', 'famfam': 'server_chart', 'permissions': [PERMISSION_OCR_DOCUMENT]}

#register_links(OCRLog, [document_queue_disable, document_queue_enable, setup_queue_transformation_list])
#register_links(QueueTransformation, [setup_queue_transformation_edit, setup_queue_transformation_delete])


register_links(Queue, [queue_items])
register_multi_item_links(['queue_item_list'], [queue_item_multiple_delete]), #re_queue_multiple_document] )
register_tool(queue_list)
