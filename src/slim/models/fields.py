__title__ = 'slim.models.fields'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('LanguageField', 'SimpleLanguageField')

from six import PY3

from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from slim import get_languages, default_language, get_languages_keys
from slim.settings import ENABLE_MONKEY_PATCHING
from slim.monkey_patches import monkeypatch_method, monkeypatch_property
from slim.helpers import admin_change_url, admin_add_url

class LanguageField(models.CharField):
    """
    LanguageField model. Stores language string in a ``CharField`` field.

    Using `contrib_to_class` melthod adds `translation_of` field, which is simply a ``ForeignKey``
    to the same class.
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        """
        Create new field. Argument ``populate`` will be sent as-is to the form field.
        """
        defaults = {
            'verbose_name': _('Language'),
            'populate': None,
            'max_length': 10,
            'choices': get_languages(),
            'default': default_language
        }
        defaults.update(kwargs)
        self.populate = defaults.pop('populate', None)
        super(LanguageField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
        """
        Returns best form field to represent this model field
        """
        defaults = {
            'form_class': LanguageField,
            'populate': self.populate,
        }
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)

    def validate(self, value, model_instance):
        """
        Validating the field.

        We shall make sure that there are double translations for the same language for the same object. That's
        why, in case if model is not yet saved (``translated_object`` does not yet have a primary key), we check
        if there are already translations of the same object in the language we specify now.

        Otherwise, if ``model_instance`` already has a primary key, we anyway try to get a ``translated_object``
        and compare it with our ``model_instance``. In case if ``translated_object`` exists and not equal to our
        ``model_instance`` we raise an error.

        NOTE: This has nothing to do with unique fields in the original ``model_instance``. Make sure you have
        properly specified all unique attributes with respect to ``LanguageField` of your original
        ``model_instance`` if you need those records to be unique.
        """
        if model_instance.original_translation:
            translated_object = model_instance.original_translation.get_translation_for(value)
        else:
            translated_object = None
        if not model_instance.pk:
            if translated_object and translated_object.pk:
                raise exceptions.ValidationError("Translation in language %s for this object already exists." % value)
        else:
            if translated_object and translated_object.pk and model_instance != translated_object:
                raise exceptions.ValidationError("Translation in language %s for this object already exists." % value)
        super(LanguageField, self).validate(value, model_instance)

    def contribute_to_class(self, cls, name):
        """
        Language field consists of more than one database record. We have ``lanaguage`` (CharField)
        and ``translation_of`` (ForeignKey to ``cls``) in order to identify translated and
        primary objects.

        We have a set of very useful methods implemented in order to get translations easily.
        """
        self.name = name
        self.translation_of = models.ForeignKey(cls, blank=True, null=True, verbose_name=_('Translation of'), \
                                                related_name='translations', \
                                                limit_choices_to={'language': default_language}, \
                                                help_text=_('Leave this empty for entries in the primary language.'))
        cls.add_to_class('translation_of', self.translation_of)
        super(LanguageField, self).contribute_to_class(cls, name)

        if ENABLE_MONKEY_PATCHING:
            @monkeypatch_property(cls)
            def is_multilingual(self):
                """
                Simple flat to use on objects to find our wheither they are multilinugal
                or not

                :return bool: Always returns boolean True
                """
                return True

            @monkeypatch_method(cls)
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

            @monkeypatch_method(cls)
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

            @monkeypatch_method(cls)
            def get_original_translation(self, *args, **kwargs):
                """
                Gets original translation of current object.

                :return obj: Object of the same class as the one queried.
                """
                if is_primary_language(self.language):
                    return self
                return self.translation_of

            @monkeypatch_method(cls)
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

            @monkeypatch_method(cls)
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
                    return ' | '.join(output)
                except Exception as e:
                    return ''

            @monkeypatch_method(cls)
            def available_translations_admin(self, *args, **kwargs):
                """
                Gets a HTML with all available translation URLs for current object if available. For admin use.

                :return str:
                """
                return self._available_translations_admin(include_self=True, *args, **kwargs)
            available_translations_admin.allow_tags = True
            available_translations_admin.short_description = _('Translations')

            @monkeypatch_method(cls)
            def available_translations_exclude_current_admin(self, *args, **kwargs):
                """
                Same as `available_translations_admin` but does not include itself to the list.

                :return str:
                """
                return self._available_translations_admin(include_self=False, *args, **kwargs)
            available_translations_exclude_current_admin.allow_tags = True
            available_translations_exclude_current_admin.short_description = _('Translations')

            @monkeypatch_property(cls)
            def original_translation(self):
                """
                Property for ``get_original_translation`` method.

                :return obj: Object of the same class as the one queried.
                """
                return self.get_original_translation()

            @monkeypatch_method(cls)
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


class SimpleLanguageField(models.CharField):
    """
    SimpleLanguageField model. Stores language string in a ``CharField`` field.
    """

    def __init__(self, *args, **kwargs):
        """
        Create new field. Argument ``populate`` will be sent as-is to the form field.
        """
        defaults = {
            'verbose_name': _('Language'),
            'populate': None,
            'max_length': 10,
            'choices': get_languages(),
            'default': default_language
        }
        defaults.update(kwargs)
        self.populate = defaults.pop('populate', None)
        super(SimpleLanguageField, self).__init__(*args, **defaults)

    def formfield(self, **kwargs):
        """
        Returns best form field to represent this model field
        """
        defaults = {
            'form_class': SimpleLanguageField,
            'populate': self.populate,
        }
        defaults.update(kwargs)
        return super(models.CharField, self).formfield(**defaults)

# Add schema's for South
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        rules=[((LanguageField,), [], {'populate': ('populate', {'default':None}),})], \
        patterns=['slim.models\.fields\.LanguageField', 'slim.models\.fields\.SimpleLanguageField']
        )
except ImportError:
    pass
