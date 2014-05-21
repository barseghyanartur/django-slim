__title__ = 'slim.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('get_default_language', 'default_language', 'get_languages', 'get_languages_keys', \
           'get_language_from_request', 'get_languages_dict', 'admin_change_url', 'admin_add_url', 'smart_resolve')

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import get_language_info

from slim.settings import USE_LOCAL_LANGUAGE_NAMES

def get_default_language():
    """
    Gets default language.

    :return str:
    """
    return settings.LANGUAGES[0][0]
default_language = get_default_language()


def get_languages():
    """
    Gets available languages.

    :return iterable:
    """
    if not USE_LOCAL_LANGUAGE_NAMES:
        return settings.LANGUAGES
    else:
        languages = []
        for lang_code, lang_name in settings.LANGUAGES:
            try:
                lang_name = get_language_info(lang_code)['name_local']
            except Exception as e:
                pass
            languages.append((lang_code, lang_name))
        return languages


def get_languages_keys():
    """
    Returns just languages keys.

    :return list:
    """
    return [key for key, name in get_languages()]


def get_languages_dict():
    """
    Returns just languages dict.

    :return dict:
    """
    return dict(get_languages())


def get_language_from_request(request, default=default_language):
    """
    Gets language from HttpRequest

    :param django.http.HttpRequest:
    :param str default:
    :return str:
    """
    if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
        return request.LANGUAGE_CODE
    else:
        return default


def admin_change_url(app_label, module_name, object_id, extra_path='', url_title=None):
    """
    Gets an admin change URL for the object given.

    :param str app_label:
    :param str module_name:
    :param int object_id:
    :param str extra_path:
    :param str url_title: If given, an HTML a tag is returned with `url_title` as the tag title. If left to None
        just the URL string is returned.
    :return str:
    """
    try:
        url = reverse('admin:%s_%s_change' %(app_label, module_name), args=[object_id]) + extra_path
        if url_title:
            return u'<a href="%s">%s</a>' %(url, url_title)
        else:
            return url
    except:
        return None


def admin_add_url(app_label, module_name, extra_path='', url_title=None):
    """
    Gets an admin edit URL for the object given.

    :param str app_label:
    :param str module_name:
    :param str extra_path:
    :param str url_title: If given, an HTML a tag is returned with `url_title` as the tag title. If left to None
        just the URL string is returned.
    :return str:
    """
    try:
        url = reverse('admin:%s_%s_add' %(app_label, module_name)) + extra_path
        if url_title:
            return u'<a href="%s">%s</a>' %(url, url_title)
        else:
            return url
    except:
        return None


def smart_resolve(var, context):
    """
    Resolves variable from context in a smart way. First trying to resolve from context
    and when result is None checks if variable is not None and returns just variable
    when not. Otherwise returns None.

    :param str var:
    :param Context context:
    :return mixed:
    """
    if var is None:
        return None

    ret_val = None
    try:
        ret_val = var.resolve(context, True)
    except:
        ret_val = var
    if ret_val is None:
        ret_val = var

    return ret_val
