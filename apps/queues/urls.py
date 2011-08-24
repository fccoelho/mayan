from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('queues.views',
    url(r'^list/$', 'queue_list', (), 'queue_list'),
    url(r'^(?P<queue_id>\d+)/item/list/$', 'queue_item_list', (), 'queue_item_list'),

    url(r'^item/(?P<queue_item_id>\d+)/delete/$', 'queue_item_delete', (), 'queue_item_delete'),
    url(r'^item/multiple/delete/$', 'queue_item_multiple_delete', (), 'queue_item_multiple_delete'),
)
