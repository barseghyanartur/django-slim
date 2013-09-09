__title__ = 'slim.defaults'
__version__ = '0.6'
__build__ = 0x000006
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('USE_LOCALEURL', 'ENABLE_MONKEY_PATCHING')

# If set to False, `django-localeurl` usage in `slim` is force-disabled.
USE_LOCALEURL = True

# If set to True, class methods (``snart.models.Snart`` are monkey patched to the field, thus you don't have to
# inherit from snart models.
ENABLE_MONKEY_PATCHING = False