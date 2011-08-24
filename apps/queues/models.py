from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from lock_manager.models import Lock
from lock_manager.exceptions import LockError

from queues.exceptions import QueueEmpty, QueueFull, QueueInputLocked, \
    QueueOutputLocked, AlreadyQueued, AlreadyLocked, AlreadyUnlocked
from queues.managers import QueueManager

QUEUE_LOCK_TIMEOUT = 10


class Queue(models.Model):
    namespace = models.CharField(max_length=64, blank=True, verbose_name=_(u'namespace'))
    name = models.CharField(max_length=64, verbose_name=_(u'name'))
    label = models.CharField(max_length=96, verbose_name=_(u'label'))
    size = models.PositiveIntegerField(default=0, verbose_name=_(u'size'))
    input_locked = models.BooleanField(default=False, verbose_name=_(u'input locked'))
    output_locked = models.BooleanField(default=False, verbose_name=_(u'output locked'))
    allow_duplicates = models.BooleanField(default=True, verbose_name=_(u'allow duplicates'))
    
    objects = QueueManager()
    
    class Meta:
        ordering = ('namespace', 'label')
        unique_together = ('namespace', 'name')
        verbose_name = _(u'queue')
        verbose_name_plural = _(u'queues')

    def __unicode__(self):
        return self.label
            
    def push(self, content_object):
        if self.size !=0 and self.queueitem.count() > self.size:
            raise QueueFull
        if self.input_locked:
            raise QueueInputLocked
        # TODO:
        #if not allow_duplicates and content_object in 
        #raise AlreadyQueued
        self.queueitem_set.create(content_object=content_object)
        
    def pop(self):
        if self.output_locked:
            raise QueueOutputLocked   
        
        try:
            queue_item = self.queueitem_set.order_by('-pk')[0]
        except IndexError:
            # There are no queue entries
            raise QueueEmpty
        
        try:
            lock_name = u'queue_for_%d_%d' % (queue_item.content_type.pk, queue_item.object_id)
            lock = Lock.objects.acquire_lock(lock_name, QUEUE_LOCK_TIMEOUT)
            #content_object = current_item.content_object
            # Since the locked was obtained, delete the queue's oldes
            # entry's and return it's content_object
            queue_item.delete()
            lock.release()
            return queue_item.content_object
        except LockError:
            pass
            
    def lock_input(self):
        if self.input_locked:
            raise AlreadyLocked
        else:
            self.input_locked = True
            self.save()

    def unlock_input(self):
        if not self.input_locked:
            raise AlreadyUnLocked
        else:
            self.input_locked = False
            self.save()

    def lock_output(self):
        if self.output_locked:
            raise AlreadyLocked
        else:
            self.output_locked = True
            self.save()

    def unlock_output(self):
        if not self.output_locked:
            raise AlreadyUnLocked
        else:
            self.output_locked = False
            self.save()
            
    def count(self):
        return self.queueitem_set.count()
        

class QueueItem(models.Model):
    queue = models.ForeignKey(Queue, verbose_name=_(u'queue'))
    content_type = models.ForeignKey(ContentType, related_name='queue_item')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    class Meta:
        verbose_name = _(u'queue item')
        verbose_name_plural = _(u'queue items')

    def __unicode__(self):
        return unicode(self.content_object)
