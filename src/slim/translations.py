__title__ = 'slim.translations'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('short_language_code', 'is_primary_language')

from django.utils import translation

from slim.helpers import default_language


def short_language_code(code=None):
    """
    Extracts the short language code from its argument (or return the default language code).

    :param str code:
    :return str:

    from django.conf import settings
    >>> short_language_code('de')
    'de'
    >>> short_language_code('de-at')
    'de'
    """
    if code is None:
        code = translation.get_language()

    pos = code.find('-')
    if pos > -1:
        return code[:pos]
    return code


def is_primary_language(language=None):
    """
    Returns true if current or passed language is the primary language for this site.
    (The primary language is defined as the first language in settings.LANGUAGES.)

    :param str language:
    :return bool:
    """
    if not language:
        language = translation.get_language()

    return language == default_language
