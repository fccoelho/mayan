from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import messages

from forms import LocationForm


def edit_map(request):
#    folder = get_object_or_404(Folder, pk=folder_id)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = LocationForm()

    return render_to_response('generic_form.html', {
        'title': _(u'edit map for document'),#: %s') % folder,
        'form': form,
        #'object': document,
    },
    context_instance=RequestContext(request))    
