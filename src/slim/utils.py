__title__ = 'slim.utils'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('locale_url_is_installed',)

from django.conf import settings

from slim.settings import USE_LOCALEURL


def locale_url_is_installed():
    """
    Checks if localeurl is installed in the Django project.

    :return bool:
    """
    if USE_LOCALEURL is True and 'localeurl' in settings.INSTALLED_APPS and \
       'localeurl.middleware.LocaleURLMiddleware' in settings.MIDDLEWARE_CLASSES:
       return True
    return False
