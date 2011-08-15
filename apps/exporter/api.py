import hashlib

from django.template.defaultfilters import slugify

from common.utils import return_attrib

HASH_FUNCTION = lambda x: hashlib.sha256(x).hexdigest()


def get_hash(obj):
    if obj:
        return u'%s_%s' % (HASH_FUNCTION(unicode(obj)), slugify(unicode(obj)))
    else:
        return None


def export_queryset(queryset, definition_set):
    records = []
    
    for record in queryset:
        records.append(export_record(record, definition_set['elements']))
        
    return {definition_set['title']: records}
            
            
def export_record(record, elements):
    result = {}
    for element in elements:
        if 'sub_element' in element:
            sub_element = element['sub_element']
            result.update(export_queryset(return_attrib(record, sub_element['queryset']), sub_element))
        else:
            title = element.get('title', element['attribute'])
            result[title] = return_attrib(record, element['attribute'])
        
    return result
