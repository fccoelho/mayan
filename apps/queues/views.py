from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.views.generic.list_detail import object_list
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from common.utils import encapsulate

from queues.models import Queue, QueueItem


def queue_list(request):
    return render_to_response('generic_list.html', {
        'object_list': Queue.objects.all(),
        'title': _(u'queues'),
        'hide_link': True,
        'extra_columns': [
            {'name': _(u'items'), 'attribute': 'count'},
            {'name': _(u'size'), 'attribute': encapsulate(lambda x: x.size if x.size else _(u'Infinite'))},
            {'name': _(u'input'), 'attribute': encapsulate(lambda x: _(u'Locked') if x.input_locked else _(u'Unlocked'))},
            {'name': _(u'output'), 'attribute': encapsulate(lambda x: _(u'Locked') if x.output_locked else _(u'Unlocked'))},
            {'name': _(u'duplicates'), 'attribute': encapsulate(lambda x: _(u'Yes') if x.allow_duplicates else _(u'No'))},
        ],
    }, context_instance=RequestContext(request))    


def queue_item_list(request, queue_id):
    queue = get_object_or_404(Queue, pk=queue_id)

    return render_to_response('generic_list.html', {
        'object_list': queue.queueitem_set.all(),
        'title': _(u'items in queue: %s') % queue,
        'hide_links': True,
        #'hide_object': True,
        'multi_select_as_buttons': True,
        'extra_columns': [
            #{'name': _(u'items'), 'attribute': 'count'},
            #{'name': _(u'task id'), 'attribute': 'task_id'},
            #{'name': _(u'task name'), 'attribute': 'task_name'},
            #{'name': _(u'related object'), 'attribute': lambda x: display_link(x['related_object']) if x['related_object'] else u''}
        ],
    }, context_instance=RequestContext(request))    


def queue_item_delete(request, queue_item_id=None, queue_item_id_list=None):
    if queue_item_id:
        queue_items = [get_object_or_404(QueueItem, pk=queue_item_id)]
    elif queue_item_id_list:
        queue_items = [get_object_or_404(QueueItem, pk=queue_item_id) for queue_item_id in queue_item_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one queue item.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    post_action_redirect = reverse('queue_item_list', args=[queue_items[0].queue.pk])
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for queue_item in queue_items:
            try:
                queue_item.delete()
                messages.success(request, _(u'Queue item: %(queue_item)s deleted successfully.') % {
                    'queue_item': queue_item})
            except Exception, err:
                messages.error(request, _(u'Error deleting queue item: %(queue_item)s; error: %(errors)s.') % {
                    'queue_item': queue_item, 'error': err})
        return HttpResponseRedirect(next)

    context = {
        'next': next,
        'previous': previous,
        'delete_view': True,
        'form_icon': u'hourglass_delete.png',
    }

    if len(queue_items) == 1:
        context['object'] = queue_items[0]
        context['title'] = _(u'Are you sure you wish to delete queue item: %s?') % ', '.join([unicode(d) for d in queue_items])
    elif len(queue_items) > 1:
        context['title'] = _(u'Are you sure you wish to delete queue items: %s?') % ', '.join([unicode(d) for d in queue_items])

    return render_to_response('generic_confirm.html', context,
        context_instance=RequestContext(request))


def queue_item_multiple_delete(request):
    return queue_item_delete(request, queue_item_id_list=request.GET.get('id_list', []))
