from django.contrib import admin

from queues.models import Queue, QueueItem


class QueueItemInline(admin.StackedInline):
    model = QueueItem
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class QueueAdmin(admin.ModelAdmin):
    inlines = [QueueItemInline]
    #list_display = ('name', 'label', 'state')


admin.site.register(Queue, QueueAdmin)
admin.site.register(QueueItem)#, QueueAdmin)
