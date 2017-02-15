from ..exceptions import LocaleurlImportError
from ..utils import locale_url_is_installed

LOCALE_URL_IS_IMPORTABLE = False

try:
    from localeurl.templatetags.localeurl_tags import chlocale
    LOCALE_URL_IS_IMPORTABLE = True
except ImportError:
    pass

__title__ = 'slim.models.decorators'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'prepend_language',
    'localeurl_prepend_language',
    'auto_prepend_language'
)


def prepend_language(func, language_field='language'):
    """Prepend the language from the model to the path resolved."""
    def inner(self, *args, **kwargs):
        return "/%s%s" % (getattr(self, language_field),
                          func(self, *args, **kwargs))
    return inner

if LOCALE_URL_IS_IMPORTABLE:
    # Note, that ``localeurl_prepend_language`` is to be deprecated soon.

    def localeurl_prepend_language(func, language_field='language'):
        """Prepend the language from the model to the path resolved.

        Used when `django-localeurl` package is used."""
        def inner(self, *args, **kwargs):
            return chlocale(func(self, *args, **kwargs),
                            getattr(self, language_field))
        return inner

    # If `localeurl` is available gets the `localeurl` based decorator.
    # Otherwise, gets `prepend_language` based decorator.
    if locale_url_is_installed():
        auto_prepend_language = localeurl_prepend_language
    else:
        auto_prepend_language = prepend_language

else:

    def localeurl_prepend_language(func, language_field=None):
        """Prepend the language from the model to the path resolved."""
        raise LocaleurlImportError(
            "You should have localeurl installed in order to use "
            "`slim.models.localeurl_prepend_language` decorator."
        )
    # Fallback
    auto_prepend_language = prepend_language
