__title__ = 'slim.exceptions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'LocaleurlImportError',
)


class LocaleurlImportError(ImportError):
    """LocaleUrl import error exception."""

    # This is as good as deprecated.
