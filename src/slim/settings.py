__title__ = 'slim.settings'
__version__ = '0.6'
__build__ = 0x000006
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('USE_LOCALEURL', 'ENABLE_MONKEY_PATCHING')

from slim.conf import get_setting

USE_LOCALEURL = get_setting('USE_LOCALEURL')
ENABLE_MONKEY_PATCHING = get_setting('ENABLE_MONKEY_PATCHING')
