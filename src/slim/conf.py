__title__ = 'slim.conf'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('get_setting',)

from django.conf import settings

from slim import defaults

def get_setting(setting, override=None):
    """
    Get a setting from ``slim`` conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'SLIM_%s' % setting):
        return getattr(settings, 'SLIM_%s' % setting)
    else:
        return getattr(defaults, setting)
