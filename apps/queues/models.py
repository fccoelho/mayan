from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from queues.exceptions import QueueEmpty

class Queue(models.Model):
    namespace = models.CharField(max_length=64, blank=True, verbose_name=_(u'namespace'))
    name = models.CharField(max_length=64, verbose_name=_(u'name'))
    label = models.CharField(max_length=96, verbose_name=_(u'label'))
    limit = models.PositiveIntegerField(default=0, verbose_name=_(u'limit'))
    
    class Meta:
        ordering = ('namespace', 'label')
        unique_together = ('namespace', 'name')
        verbose_name = _(u'queue')
        verbose_name_plural = _(u'queues')

    def __unicode__(self):
        return self.label
            
    def push(self, content_object):
        self.queueitem.add(content_object)
        
    def pop(self):
        try:
            queue_item = self.queueitem_set.order_by('-pk')[0]
        except IndexError:
            raise QueueEmpty
            
        content_object = queue_item.content_object
        queue_item.delete()
        return content_object
        

class QueueItem(models.Model):
    queue = models.ForeignKey(Queue, verbose_name=_(u'queue'))
    content_type = models.ForeignKey(ContentType,
        related_name='queue_item')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    class Meta:
        verbose_name = _(u'queue item')
        verbose_name_plural = _(u'queue items')

    def __unicode__(self):
        return self.label
