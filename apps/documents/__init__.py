import tempfile

from django.utils.translation import ugettext_lazy as _

from common.utils import validate_path, encapsulate
from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_tool
from permissions.api import register_permission, set_namespace_title
from tags.widgets import get_tags_inline_widget_simple
from history.api import register_history_type
from metadata.api import get_metadata_string

from documents.models import Document, DocumentPage, \
    DocumentPageTransformation, DocumentType, DocumentTypeFilename
from documents.literals import PERMISSION_DOCUMENT_CREATE, \
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_VIEW, \
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD, \
    PERMISSION_DOCUMENT_TRANSFORM, PERMISSION_DOCUMENT_TOOLS, \
    PERMISSION_DOCUMENT_EDIT
from documents.literals import PERMISSION_DOCUMENT_TYPE_EDIT, \
    PERMISSION_DOCUMENT_TYPE_DELETE, PERMISSION_DOCUMENT_TYPE_CREATE
from documents.literals import HISTORY_DOCUMENT_CREATED, \
    HISTORY_DOCUMENT_EDITED, HISTORY_DOCUMENT_DELETED
from documents.conf.settings import ZOOM_MAX_LEVEL
from documents.conf.settings import ZOOM_MIN_LEVEL
from documents.conf import settings as document_settings
from documents.widgets import document_thumbnail


# Document page links expressions
def is_first_page(context):
    return context['page'].page_number <= 1


def is_last_page(context):
    return context['page'].page_number >= context['page'].document.documentpage_set.count()


def is_min_zoom(context):
    return context['zoom'] <= ZOOM_MIN_LEVEL


def is_max_zoom(context):
    return context['zoom'] >= ZOOM_MAX_LEVEL

# Permission setup
set_namespace_title('documents', _(u'Documents'))
register_permission(PERMISSION_DOCUMENT_CREATE)
register_permission(PERMISSION_DOCUMENT_PROPERTIES_EDIT)
register_permission(PERMISSION_DOCUMENT_EDIT)
register_permission(PERMISSION_DOCUMENT_VIEW)
register_permission(PERMISSION_DOCUMENT_DELETE)
register_permission(PERMISSION_DOCUMENT_DOWNLOAD)
register_permission(PERMISSION_DOCUMENT_TRANSFORM)
register_permission(PERMISSION_DOCUMENT_TOOLS)

# Document type permissions
set_namespace_title('documents_setup', _(u'Documents setup'))
register_permission(PERMISSION_DOCUMENT_TYPE_EDIT)
register_permission(PERMISSION_DOCUMENT_TYPE_DELETE)
register_permission(PERMISSION_DOCUMENT_TYPE_CREATE)

# History setup
register_history_type(HISTORY_DOCUMENT_CREATED)
register_history_type(HISTORY_DOCUMENT_EDITED)
register_history_type(HISTORY_DOCUMENT_DELETED)

document_list = {'text': _(u'all documents'), 'view': 'document_list', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_list_recent = {'text': _(u'recent documents'), 'view': 'document_list_recent', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_create_multiple = {'text': _(u'upload new documents'), 'view': 'document_create_multiple', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_CREATE], 'children_view_regex': ['upload']}
document_create_siblings = {'text': _(u'clone metadata'), 'view': 'document_create_siblings', 'args': 'object.id', 'famfam': 'page_copy', 'permissions': [PERMISSION_DOCUMENT_CREATE]}
document_view_simple = {'text': _(u'details'), 'view': 'document_view_simple', 'args': 'object.id', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_view_advanced = {'text': _(u'properties'), 'view': 'document_view_advanced', 'args': 'object.id', 'famfam': 'page_gear', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_delete = {'text': _(u'delete'), 'view': 'document_delete', 'args': 'object.id', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_multiple_delete = {'text': _(u'delete'), 'view': 'document_multiple_delete', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_edit = {'text': _(u'edit'), 'view': 'document_edit', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_preview = {'text': _(u'preview'), 'class': 'fancybox', 'view': 'document_preview', 'args': 'object.id', 'famfam': 'magnifier', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_download = {'text': _(u'download'), 'view': 'document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_find_duplicates = {'text': _(u'find duplicates'), 'view': 'document_find_duplicates', 'args': 'object.id', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_find_all_duplicates = {'text': _(u'find all duplicates'), 'view': 'document_find_all_duplicates', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'description': _(u'Search all the documents\' checksums and return a list of the exact matches.')}
document_clear_transformations = {'text': _(u'clear transformations'), 'view': 'document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_multiple_clear_transformations = {'text': _(u'clear transformations'), 'view': 'document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_print = {'text': _(u'print'), 'view': 'document_print', 'args': 'object.id', 'famfam': 'printer', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_history_view = {'text': _(u'history'), 'view': 'history_for_object', 'args': ['"documents"', '"document"', 'object.id'], 'famfam': 'book_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'page.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_create = {'text': _(u'create new transformation'), 'class': 'no-parent-history', 'view': 'document_page_transformation_create', 'args': 'page.pk', 'famfam': 'pencil_add', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_edit = {'text': _(u'edit'), 'class': 'no-parent-history', 'view': 'document_page_transformation_edit', 'args': 'transformation.pk', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_delete = {'text': _(u'delete'), 'class': 'no-parent-history', 'view': 'document_page_transformation_delete', 'args': 'transformation.pk', 'famfam': 'pencil_delete', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}

document_page_view = {'text': _(u'page image'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'page.pk', 'famfam': 'page_white_picture', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_text = {'text': _(u'page text'), 'class': 'no-parent-history', 'view': 'document_page_text', 'args': 'page.pk', 'famfam': 'page_white_text', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_edit = {'text': _(u'edit page text'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'page.pk', 'famfam': 'page_white_edit', 'permissions': [PERMISSION_DOCUMENT_EDIT]}
document_page_navigation_next = {'text': _(u'next page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_next', 'args': 'page.pk', 'famfam': 'resultset_next', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page}
document_page_navigation_previous = {'text': _(u'previous page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_previous', 'args': 'page.pk', 'famfam': 'resultset_previous', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page}
document_page_navigation_first = {'text': _(u'first page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_first', 'args': 'page.pk', 'famfam': 'resultset_first', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_first_page}
document_page_navigation_last = {'text': _(u'last page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_last', 'args': 'page.pk', 'famfam': 'resultset_last', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_last_page}
document_page_zoom_in = {'text': _(u'zoom in'), 'class': 'no-parent-history', 'view': 'document_page_zoom_in', 'args': 'page.pk', 'famfam': 'zoom_in', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_max_zoom}
document_page_zoom_out = {'text': _(u'zoom out'), 'class': 'no-parent-history', 'view': 'document_page_zoom_out', 'args': 'page.pk', 'famfam': 'zoom_out', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'conditional_disable': is_min_zoom}
document_page_rotate_right = {'text': _(u'rotate right'), 'class': 'no-parent-history', 'view': 'document_page_rotate_right', 'args': 'page.pk', 'famfam': 'arrow_turn_right', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_rotate_left = {'text': _(u'rotate left'), 'class': 'no-parent-history', 'view': 'document_page_rotate_left', 'args': 'page.pk', 'famfam': 'arrow_turn_left', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_view_reset = {'text': _(u'reset view'), 'class': 'no-parent-history', 'view': 'document_page_view_reset', 'args': 'page.pk', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_missing_list = {'text': _(u'Find missing document files'), 'view': 'document_missing_list', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

# Document type related links
document_type_list = {'text': _(u'document type list'), 'view': 'document_type_list', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_document_list = {'text': _(u'documents of this type'), 'view': 'document_type_document_list', 'args': 'document_type.id', 'famfam': 'page_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_edit = {'text': _(u'edit'), 'view': 'document_type_edit', 'args': 'document_type.id', 'famfam': 'layout_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_delete = {'text': _(u'delete'), 'view': 'document_type_delete', 'args': 'document_type.id', 'famfam': 'layout_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_DELETE]}
document_type_create = {'text': _(u'create document type'), 'view': 'document_type_create', 'famfam': 'layout_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_CREATE]}

document_type_filename_list = {'text': _(u'filenames'), 'view': 'document_type_filename_list', 'args': 'document_type.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_filename_create = {'text': _(u'add filename to document type'), 'view': 'document_type_filename_create', 'args': 'document_type.id', 'famfam': 'database_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_edit = {'text': _(u'edit'), 'view': 'document_type_filename_edit', 'args': 'filename.id', 'famfam': 'database_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_delete = {'text': _(u'delete'), 'view': 'document_type_filename_delete', 'args': 'filename.id', 'famfam': 'database_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}

document_type_views = ['setup_document_type_metadata', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete', 'document_type_create', 'document_type_filename_list', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_delete']

# Register document type links
register_links(DocumentType, [document_type_document_list, document_type_filename_list, document_type_edit, document_type_delete])
register_links(DocumentTypeFilename, [document_type_filename_edit, document_type_filename_delete])

register_links(['setup_document_type_metadata', 'document_type_filename_delete', 'document_type_create', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_list', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete'], [document_type_create], menu_name='sidebar')
register_links(['document_type_filename_create', 'document_type_filename_list', 'document_type_filename_edit', 'document_type_filename_delete'], [document_type_filename_create], menu_name='sidebar')

# Register document links
register_links(Document, [document_edit, document_print, document_delete, document_download, document_find_duplicates, document_clear_transformations, document_create_siblings])
register_multi_item_links(['document_find_duplicates', 'folder_view', 'index_instance_list', 'document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent'], [document_multiple_clear_transformations, document_multiple_delete])

secondary_menu_links = [document_list_recent, document_list, document_create_multiple]

register_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_interactive', 'staging_file_delete'], secondary_menu_links, menu_name='secondary_menu')
register_links(Document, secondary_menu_links, menu_name='secondary_menu')

# Document page links
register_links(DocumentPage, [
    document_page_transformation_list, document_page_view,
    document_page_text, document_page_edit,
])

# Document page navigation links
register_links(DocumentPage, [
    document_page_navigation_first, document_page_navigation_previous,
    document_page_navigation_next, document_page_navigation_last
], menu_name='related')

register_links(['document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out, document_page_view_reset], menu_name='form_header')

register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
register_links('document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
register_links('document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
register_links(['document_page_transformation_edit', 'document_page_transformation_delete'], [document_page_transformation_create], menu_name='sidebar')

register_diagnostic('documents', _(u'Documents'), document_missing_list)

register_tool(document_find_all_duplicates, namespace='documents', title=_(u'documents'))


def document_exists(document):
    try:
        if document.exists():
            return u'<span class="famfam active famfam-tick"></span>'
        else:
            return u'<span class="famfam active famfam-cross"></span>'
    except Exception, exc:
        return exc

register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            encapsulate(lambda x: document_thumbnail(x))
        },
        {'name':_(u'tags'), 'attribute':
            encapsulate(lambda x: get_tags_inline_widget_simple(x))
        },
        {'name':_(u'metadata'), 'attribute':
            encapsulate(lambda x: get_metadata_string(x))
        },
    ])

register_top_menu(
    'documents',
    link={'famfam': 'page', 'text': _(u'documents'), 'view': 'document_list_recent'},
    children_path_regex=[
        r'^documents/[^t]', r'^metadata/[^s]', r'comments', r'tags/document', r'grouping/[^s]', r'history/list/for_object/documents'
    ],
    children_views=['document_folder_list', 'folder_add_document', 'document_index_list'],
    position=0
)

register_sidebar_template(['document_list_recent'], 'recent_document_list_help.html')
register_sidebar_template(['document_type_list'], 'document_types_help.html')

register_links(Document, [document_view_simple], menu_name='form_header', position=0)
register_links(Document, [document_view_advanced], menu_name='form_header', position=1)
register_links(Document, [document_history_view], menu_name='form_header')

if (validate_path(document_settings.CACHE_PATH) == False) or (not document_settings.CACHE_PATH):
    setattr(document_settings, 'CACHE_PATH', tempfile.mkdtemp())
