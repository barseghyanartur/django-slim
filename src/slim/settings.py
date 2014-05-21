__title__ = 'slim.settings'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('USE_LOCALEURL', 'USE_LOCAL_LANGUAGE_NAMES', 'ENABLE_MONKEY_PATCHING')

from slim.conf import get_setting

USE_LOCALEURL = get_setting('USE_LOCALEURL')
USE_LOCAL_LANGUAGE_NAMES = get_setting('USE_LOCAL_LANGUAGE_NAMES')
ENABLE_MONKEY_PATCHING = get_setting('ENABLE_MONKEY_PATCHING')
