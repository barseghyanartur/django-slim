__title__ = 'slim.defaults'
__version__ = '0.7'
__build__ = 0x000007
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('USE_LOCALEURL', 'USE_LOCAL_LANGUAGE_NAMES', 'ENABLE_MONKEY_PATCHING')

# If set to False, `django-localeurl` usage in `slim` is force-disabled.
USE_LOCALEURL = True

# If set to True, local language names are used.
USE_LOCAL_LANGUAGE_NAMES = False

# If set to True, class methods (``snart.models.Snart`` are monkey patched to the field, thus you don't have to
# inherit from snart models.
ENABLE_MONKEY_PATCHING = False