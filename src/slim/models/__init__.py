from six import PY3, text_type

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..helpers import (
    get_languages,
    # default_language,
    get_languages_keys,
    admin_change_url,
    admin_add_url
)
from ..translations import is_primary_language

__title__ = 'slim.models'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Slim', 'SlimBaseModel')


class Slim(object):
    """Main multi-lingual class.

    Add this class to all your multi-lingual Django models, where you
    use ``slim.models.fields.LanguageField``. Alternatively, you may use
    the ``slim.models.SlimBaseModel``.
    """

    @property
    def is_multilingual(self):
        """If multi-lingual or not.

        Simple flat to use on objects to find our whether they are
        multi-lingual or not.

        :return bool: Always returns boolean True
        """
        return True

    def available_translations(self):
        """Returnavailable translations.

        :return iterable: At this moment a list of objects.
        """
        # New, unsaved pages have no translations
        if not self.id:
            return []
        if is_primary_language(self.language):
            return self.translations.all()
        elif self.translation_of:
            return [self.translation_of] + \
                   list(
                       self.translation_of.translations.exclude(
                           language=self.language
                       )
                   )
        else:
            return []

    def get_original_translation(self, *args, **kwargs):
        """Get original translation of current object.

        :return obj: Object of the same class as the one queried.
        """
        if is_primary_language(self.language):
            return self
        return self.translation_of

    def translation_admin(self, *args, **kwargs):
        """Get a HTML with URL to the original translation of available.
        For admin use.

        :return str:
        """
        if self.translation_of:
            url_title = text_type(self.translation_of)

            return admin_change_url(
                self._meta.app_label,
                self._meta.module_name,
                self.translation_of.id,
                url_title=url_title
            )
        return ''
    translation_admin.allow_tags = True
    translation_admin.short_description = _('Translation of')

    def _available_translations_admin(self, include_self=True):
        """Get HTML with all available translation URLs for current object.

        Get HTML with all available translation URLs for current object if
        available. For admin use.

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
                url_title = text_type(languages[translation.language])
                for translation in available_translations:

                    output.append(
                        admin_change_url(
                            translation._meta.app_label,
                            translation._meta.module_name,
                            translation.id,
                            url_title=url_title
                        )
                    )
                    languages_keys.remove(translation.language)

            if self.pk and self.language in languages_keys:
                languages_keys.remove(self.language)

            # For all languages that are still available (original object has
            # no translations for).
            for language in languages_keys:
                url = admin_add_url(
                    self._meta.app_label,
                    self._meta.module_name,
                    '?translation_of=%s&amp;language=%s' % (
                        text_type(original_translation.id),
                        language
                    )
                )
                name = text_type(languages[language])

                output.append(
                    u'<a href="%(url)s" style="color:#baa">%(name)s</a>' % {
                        'url': url,
                        'name': name
                    }
                )
            return u' | '.join(output)
        except Exception:
            return u''

    def available_translations_admin(self, *args, **kwargs):
        """Get a HTML with all available translation URLs for current object.

        Get a HTML with all available translation URLs for current object if
        available. For admin use.

        :return str:
        """
        return self._available_translations_admin(
            include_self=True, *args, **kwargs
        )
    available_translations_admin.allow_tags = True
    available_translations_admin.short_description = _('Translations')

    def available_translations_exclude_current_admin(self, *args, **kwargs):
        """Same as ``available_translations_admin`` but does not append itself.

        Does not append itself to the list.

        :return str:
        """
        return self._available_translations_admin(include_self=False,
                                                  *args,
                                                  **kwargs)
    available_translations_exclude_current_admin.allow_tags = True
    available_translations_exclude_current_admin.short_description = _(
        'Translations'
    )

    @property
    def original_translation(self):
        """Property for ``get_original_translation`` method.

        :return obj: Object of the same class as the one queried.
        """
        return self.get_original_translation()

    def get_translation_for(self, language):
        """
        Get translation article in given language.

        :param str language: Which shall be one of the languages specified
            in ``LANGUAGES`` in `settings.py`.
        :return obj: Either object of the same class as or None if no
            translations are available for the given ``language``.
        """
        if language not in get_languages_keys():
            return None
        if str(self.language) == str(language):
            return self
        if str(self.original_translation.language) == text_type(language):
            return self.original_translation
        try:
            return self.original_translation.translations.get(language=language)
        except Exception:
            return None


class SlimBaseModel(models.Model, Slim):
    """An abstract Django model."""

    class Meta:
        """Meta."""

        abstract = True
