try:
    from psycopg2 import OperationalError
except ImportError:
    class OperationalError(Exception):
        pass

import datetime

from django.db.utils import DatabaseError
from django.db.utils import IntegrityError
from django.db import transaction
from django.db import models


class QueueManager(models.Manager):
    @transaction.commit_manually
    def get_queue(self, *args, **kwargs):
        try:
            queue, created = self.model.objects.get_or_create(*args, **kwargs)
            transaction.commit()
            return queue
        except DatabaseError:
            transaction.rollback()
            # Special case for ./manage.py syncdb
        except (OperationalError, ImproperlyConfigured):
            transaction.rollback()
            # Special for DjangoZoom, which executes collectstatic media
            # doing syncdb and creating the database tables
    #    else:
    #        transaction.commit()
    #        return 
