"""Configuration options for the django locking app"""

DEFAULT_LOCK_TIMEOUT_VALUE = 10

try:
    from smart_settings.api import register_settings

    register_settings(
        namespace=u'lock_manager',
        module=u'lock_manager.conf.settings',
        settings=[
            {'name': u'DEFAULT_LOCK_TIMEOUT', 'global_name': u'LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT', 'default': DEFAULT_LOCK_TIMEOUT_VALUE},
        ]
    )

except ImportError:
    from django.conf import settings


    DEFAULT_LOCK_TIMEOUT = getattr(settings, 'LOCK_MANAGER_DEFAULT_LOCK_TIMEOUT', DEFAULT_LOCK_TIMEOUT_VALUE)
