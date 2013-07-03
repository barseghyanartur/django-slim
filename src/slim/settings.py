__all__ = ('USE_LOCALEURL', 'ENABLE_MONKEY_PATCHING')

from slim.conf import get_setting

USE_LOCALEURL = get_setting('USE_LOCALEURL')
ENABLE_MONKEY_PATCHING = get_setting('ENABLE_MONKEY_PATCHING')
