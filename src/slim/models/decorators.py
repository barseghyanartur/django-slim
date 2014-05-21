__title__ = 'slim.models.decorators'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('prepend_language', 'localeurl_prepend_language', 'auto_prepend_language')

from slim.utils import locale_url_is_installed

def prepend_language(func, language_field='language'):
    """
    Prepends the language from the model to the path resolved.
    """
    def inner(self, *args, **kwargs):
        return "/%s%s" % (getattr(self, language_field), func(self, *args, **kwargs))
    return inner

try:
    from localeurl.templatetags.localeurl_tags import chlocale

    def localeurl_prepend_language(func, language_field='language'):
        """
        Prepends the language from the model to the path resolved when `django-localeurl` package is used.
        """
        def inner(self, *args, **kwargs):
            return chlocale(func(self, *args, **kwargs), getattr(self, language_field))
        return inner

    # If `localeurl` is available gets the `localeurl` based decorator. Otherwise, gets `prepend_language`
    # based decorator.
    if locale_url_is_installed():
        auto_prepend_language = localeurl_prepend_language
    else:
        auto_prepend_language = prepend_language

except ImportError as e:
    from slim.exceptions import LocaleurlImportError

    def localeurl_prepend_language(func, language_field=None):
        raise LocaleurlImportError(
            "You should have localeurl installed in order to use "
            "`slim.models.localeurl_prepend_language` decorator."
            )
    # Fallback
    auto_prepend_language = prepend_language
