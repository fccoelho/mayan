from django.conf.urls.defaults import patterns, url

from sources.literals import SOURCE_CHOICE_WEB_FORM, SOURCE_CHOICE_STAGING, \
    SOURCE_CHOICE_WATCH

urlpatterns = patterns('sources.views',
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/preview/$', 'staging_file_preview', (), 'staging_file_preview'),
    url(r'^staging_file/type/(?P<source_type>\w+)/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/delete/$', 'staging_file_delete', (), 'staging_file_delete'),
    url(r'^staging_file/type/staging_folder/(?P<source_id>\d+)/(?P<staging_file_id>\w+)/thumbnail/$', 'staging_file_thumbnail', (), 'staging_file_thumbnail'),

    url(r'^upload/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/$', 'upload_interactive', (), 'upload_interactive'),
    url(r'^upload/interactive/$', 'upload_interactive', (), 'upload_interactive'),

    #Setup views

    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_WEB_FORM, 'setup_source_list', {'source_type': SOURCE_CHOICE_WEB_FORM}, 'setup_web_form_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_STAGING, 'setup_source_list', {'source_type': SOURCE_CHOICE_STAGING}, 'setup_staging_folder_list'),
    url(r'^setup/interactive/%s/list/$' % SOURCE_CHOICE_WATCH, 'setup_source_list', {'source_type': SOURCE_CHOICE_WATCH}, 'setup_watch_folder_list'),

    url(r'^setup/interactive/(?P<source_type>\w+)/list/$', 'setup_source_list', (), 'setup_source_list'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/edit/$', 'setup_source_edit', (), 'setup_source_edit'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/delete/$', 'setup_source_delete', (), 'setup_source_delete'),
    url(r'^setup/interactive/(?P<source_type>\w+)/create/$', 'setup_source_create', (), 'setup_source_create'),

    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/transformation/list/$', 'setup_source_transformation_list', (), 'setup_source_transformation_list'),
    url(r'^setup/interactive/(?P<source_type>\w+)/(?P<source_id>\d+)/transformation/create/$', 'setup_source_transformation_create', (), 'setup_source_transformation_create'),
    url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/edit/$', 'setup_source_transformation_edit', (), 'setup_source_transformation_edit'),
    url(r'^setup/interactive/source/transformation/(?P<transformation_id>\d+)/delete/$', 'setup_source_transformation_delete', (), 'setup_source_transformation_delete'),
)
