__title__ = 'slim.models.__init__'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Slim', 'SlimBaseModel')

from six import PY3

from django.db import models
from django.utils.translation import ugettext_lazy as _

from slim import get_languages, default_language, get_languages_keys
from slim.translations import is_primary_language
from slim.helpers import admin_change_url, admin_add_url

class Slim(object):
    """
    Add this class to all your multi-lingual Django models, where you use ``slim.models.fields.LanguageField``.
    Alternatively, you may use the ``slim.models.SlimBaseModel``.
    """
    @property
    def is_multilingual(self):
        """
        Simple flat to use on objects to find our wheither they are multilinugal
        or not

        :return bool: Always returns boolean True
        """
        return True

    def get_redirect_to_target(self, request):
        """
        Find an acceptable redirect target. If this is a local link, then try
        to find the page this redirect references and translate it according
        to the user's language. This way, one can easily implement a localized
        "/"-url to welcome page redirection.
        """
        target = self.redirect_to
        if target and target.find('//') == -1: # Not an offsite link http://bla/blubb
            try:
                page = cls.objects.page_for_path(target)
                page = page.get_translation(getattr(request, 'LANGUAGE_CODE', None))
                target = page.get_absolute_url()
            except cls.DoesNotExist:
                pass
        return target

    def available_translations(self):
        """
        Returns available translations.

        :return interable: At this moment a list of objects.
        """
        if not self.id: # New, unsaved pages have no translations
            return []
        if is_primary_language(self.language):
            return self.translations.all()
        elif self.translation_of:
            return [self.translation_of] + list(self.translation_of.translations.exclude(
                language=self.language))
        else:
            return []

    def get_original_translation(self, *args, **kwargs):
        """
        Gets original translation of current object.

        :return obj: Object of the same class as the one queried.
        """
        if is_primary_language(self.language):
            return self
        return self.translation_of

    def translation_admin(self, *args, **kwargs):
        """
        Gets a HTML with URL to the original translation of available. For admin use.

        :return str:
        """
        if self.translation_of:
            if not PY3:
                url_title = unicode(self.translation_of)
            else:
                url_title = self.translation_of

            return admin_change_url(
                self._meta.app_label,
                self._meta.module_name,
                self.translation_of.id,
                url_title = url_title
                )
        return ''
    translation_admin.allow_tags = True
    translation_admin.short_description = _('Translation of')

    def _available_translations_admin(self, include_self=True):
        """
        Gets a HTML with all available translation URLs for current object if available. For admin use.

        :return str:
        """
        try:
            original_translation = self.original_translation
            available_translations = list(self.available_translations())
            languages_keys = get_languages_keys()
            languages = dict(get_languages())

            if include_self:
                available_translations.append(self)

            output = []
            # Processing all available translations. Adding edit links.
            if available_translations:
                for translation in available_translations:
                    if not PY3:
                        url_title = unicode(languages[translation.language])
                    else:
                        url_title = languages[translation.language]

                    output.append(
                        admin_change_url(
                            translation._meta.app_label,
                            translation._meta.module_name,
                            translation.id,
                            url_title = url_title
                            )
                        )
                    languages_keys.remove(translation.language)

            if self.pk and self.language in languages_keys:
                languages_keys.remove(self.language)

            # For all languages that are still available (original object has no translations for)
            for language in languages_keys:
                url = admin_add_url(
                        self._meta.app_label,
                        self._meta.module_name,
                        '?translation_of=%s&amp;language=%s' % (str(original_translation.id), language)
                        )
                if not PY3:
                    name = unicode(languages[language])
                else:
                    name = languages[language]

                output.append(u'<a href="%(url)s" style="color:#baa">%(name)s</a>' % {'url': url, 'name': name})
            return u' | '.join(output)
        except Exception as e:
            return u''

    def available_translations_admin(self, *args, **kwargs):
        """
        Gets a HTML with all available translation URLs for current object if available. For admin use.

        :return str:
        """
        return self._available_translations_admin(include_self=True, *args, **kwargs)
    available_translations_admin.allow_tags = True
    available_translations_admin.short_description = _('Translations')

    def available_translations_exclude_current_admin(self, *args, **kwargs):
        """
        Same as `available_translations_admin` but does not include itself to the list.

        :return str:
        """
        return self._available_translations_admin(include_self=False, *args, **kwargs)
    available_translations_exclude_current_admin.allow_tags = True
    available_translations_exclude_current_admin.short_description = _('Translations')

    @property
    def original_translation(self):
        """
        Property for ``get_original_translation`` method.

        :return obj: Object of the same class as the one queried.
        """
        return self.get_original_translation()

    def get_translation_for(self, language):
        """
        Get translation article in given language.

        :param str language: Which shall be one of the languages specified in ``LANGUAGES``
            in `settings.py`.
        :return obj: Either object of the same class as or None if no translations are
            available for the given ``language``.
        """
        if not language in get_languages_keys():
            return None
        if str(self.language) == str(language):
            return self
        if str(self.original_translation.language) == str(language):
            return self.original_translation
        try:
            return self.original_translation.translations.get(language=language)
        except Exception as e:
            return None

class SlimBaseModel(models.Model, Slim):
    """
    An abstract Django model.
    """
    class Meta:
        abstract = True
