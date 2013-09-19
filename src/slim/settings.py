__title__ = 'slim.settings'
__version__ = '0.7'
__build__ = 0x000007
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('USE_LOCALEURL', 'USE_LOCAL_LANGUAGE_NAMES', 'ENABLE_MONKEY_PATCHING')

from slim.conf import get_setting

USE_LOCALEURL = get_setting('USE_LOCALEURL')
USE_LOCAL_LANGUAGE_NAMES = get_setting('USE_LOCAL_LANGUAGE_NAMES')
ENABLE_MONKEY_PATCHING = get_setting('ENABLE_MONKEY_PATCHING')
