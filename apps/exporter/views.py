import os

from django.utils import simplejson
from django.http import HttpResponse

from documents.models import Document, DocumentType
from metadata.models import MetadataType, MetadataSet

from exporter.api import export_queryset, get_hash
    
FORMAT_VERSION = 1.0

'''
comments
tags
folders    

pages
pages transformation
metadata
doc_type metadata

sources
sources transform

users

class DocumentTypeDefaults(models.Model):
    """
    Default preselected metadata types and metadata set per document
    type
    """    
    document_type = models.ForeignKey(DocumentType, verbose_name=_(u'document type'))
    default_metadata_sets = models.ManyToManyField(MetadataSet, blank=True, verbose_name=_(u'default metadata sets'))
    default_metadata = models.ManyToManyField(MetadataType, blank=True, verbose_name=_(u'default metadata'))


'''

def export_test(request):
    big_list = []
    big_list.append({'version': FORMAT_VERSION})
    
    big_list.append(export_queryset(MetadataType.objects.all(), {
        'title': 'metadata_types', 'elements': [
            {'attribute': 'name'},
            {'attribute': 'title'},
            {'attribute': 'default'},
            {'attribute': 'lookup'},
        ]
    }))
    
    big_list.append(export_queryset(MetadataSet.objects.all(), {
        'title': 'metadata_set', 'elements': [
            {'title': 'id', 'attribute': lambda x: get_hash(x.title)},
            {'title': 'name', 'attribute': 'title'},
            {'sub_element': {
                'title': 'metadata_types',
                'queryset': lambda x: x.metadatasetitem_set.all(),
                'elements': [
                    {'title': 'name', 'attribute': lambda x: x.metadata_type.name}
                ]}
            }
        ]
    }))
        
    big_list.append(export_queryset(DocumentType.objects.all(), {
        'title': 'document_types', 'elements': [
            {'title': 'id', 'attribute': lambda x: get_hash(x.name)},
            {'attribute': 'name'},
            {
                'sub_element': {
                    'title': 'filenames',
                    'queryset': lambda x: x.documenttypefilename_set.all(),
                    'elements': [
                        {'attribute': 'filename'},
                        {'attribute': 'enabled'}
                    ]
                }
            },
            {
                'sub_element': {
                    'title': 'metadata_defaults',
                    'queryset': lambda x: x.documenttypedefaults_set.all(),
                    'elements': [
                        {
                            'sub_element': {
                                'title': 'metadata_types',
                                'queryset': lambda x: x.default_metadata.all(),
                                'elements': [
                                    {'attribute': 'name'}
                                ]
                            }
                        },
                        {
                            'sub_element': {
                                'title': 'metadata_sets',
                                'queryset': lambda x: x.default_metadata_sets.all(),
                                'elements': [
                                    {'title': 'id', 'attribute': lambda x: get_hash(x.title)}
                                ]
                            }
                         }                     
                    ]
                }
            }
        ]
    }))
    
    
    big_list.append(export_queryset(Document.objects.all()[:10], {
        'title': 'documents', 'elements': [
            {'title': 'document_type', 'attribute': lambda x: get_hash(x.document_type)},
            {'title': 'filename', 'attribute': lambda x: os.extsep.join([x.file_filename, x.file_extension])},
            {'attribute': 'uuid'},
            {'title': 'description', 'attribute': lambda x: unicode(x.description) if x.description else None},
            {
                'sub_element': {
                    'title': 'tags',
                    'queryset': lambda x: x.tags.all(),
                    'elements': [
                        {'title': 'id', 'attribute': lambda x: get_hash(x)},
                    ]
                }
            },
            {
                'sub_element': {
                    'title': 'folders',
                    'queryset': lambda x: x.folderdocument_set.all(),
                    'elements': [
                        {'title': 'id', 'attribute': lambda x: get_hash(x.folder)},
                    ]
                }
            },
            {
                'sub_element': {
                    'title': 'comments',
                    'queryset': lambda x: x.comments.all(),
                    'elements': [
                        {'attribute': 'comment'},
                        {'title': 'user', 'attribute': lambda x: unicode(x.user)},
                        {'title': 'submit_date', 'attribute': lambda x: unicode(x.submit_date)},
                    ]
                }
            },   
        ]
    }))    
    '''
        'versions': [
            {
                1.0: {
                    'mimetype': document.file_mimetype,
                    'encoding': document.file_mime_encoding,
                    #'date_updated'
                    'checksum': document.checksum,
                }
            }
        ]
    '''
    return HttpResponse(simplejson.dumps(big_list, indent=4, ensure_ascii=True), mimetype='application/json')
