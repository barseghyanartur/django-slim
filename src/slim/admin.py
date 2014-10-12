__title__ = 'slim.admin'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SlimAdmin',)

from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from slim.helpers import default_language


class SlimAdmin(admin.ModelAdmin):
    """
    SlimAdmin.

    ``list_view_primary_only`` - if set to True, onlt primary language items would be shown in the list
    view. Default value is False.

    ``language_field`` - name of the language field defined in your model. Default value `language`.

    ``auto_add_edit_view`` - if set to True, extra fields for language editing are added to the list view.
    Do NOT set this value to False!

    ``collapse_slim_fieldset`` if set to True, the language fieldset is shown collapsed.
    """
    # If set to True, only primary language objects are shown in the list view.
    list_view_primary_only = False

    # Language field in your model
    language_field = 'language'

    # If set to True, languages fields are added to the edit view (as a fieldset)
    auto_add_edit_view = True

    # If set to True, languages fieldset is auto added to the list view
    auto_add_list_view = True

    # If set to True, the fieldset is shown collapsed.
    collapse_slim_fieldset = True

    def queryset(self, *args, **kwargs):
        # For faster admin load we use ``prefetch_related``. Note, that this doesn't work on Django < 1.5.
        queryset = super(SlimAdmin, self).queryset(*args, **kwargs) \
                                         .prefetch_related('translations') \
                                         .select_related('translation_of')

        if self.list_view_primary_only is True:
            f = {self.language_field: default_language}
            queryset = queryset.filter(**f)

        return queryset
    get_queryset = queryset

    def get_list_display(self, *args, **kwargs):
        list_display = super(SlimAdmin, self).get_list_display(*args, **kwargs)

        if self.auto_add_list_view:
            list_display = list(list_display)
            list_display.extend(
                (self.language_field, 'available_translations_admin')
            )

        return list_display

    def get_readonly_fields(self, *args, **kwargs):
        readonly_fields = super(SlimAdmin, self).get_readonly_fields(*args, **kwargs)

        if self.auto_add_list_view:
            readonly_fields = list(readonly_fields)
            readonly_fields.extend(
                ('available_translations_exclude_current_admin',)
            )

        return readonly_fields

    def get_list_filter(self, *args, **kwargs):
        list_filter = super(SlimAdmin, self).get_list_filter(*args, **kwargs)

        if list_filter is None:
            return [self.language_field]
        else:
            list_filter = list(list_filter)
            list_filter.append(self.language_field)

        return list_filter

    def _django17_declared_fieldsets(self):
        if self.fieldsets:
            return self.fieldsets
        elif self.fields:
            return [(None, {'fields': self.fields})]
        return None

    def _declared_fieldsets(self, *args, **kwargs):
        try:
            declared_fieldsets = super(SlimAdmin, self)._declared_fieldsets(*args, **kwargs)
        except AttributeError as e:
            declared_fieldsets = self._django17_declared_fieldsets(*args, **kwargs)

        if self.auto_add_edit_view:
            declared_fieldsets = list(declared_fieldsets)
            declared_fieldsets.append(
                (_("Translations"), {
                    'classes': ('collapse' if self.collapse_slim_fieldset else '',),
                    'fields': (self.language_field, 'translation_of', 'available_translations_exclude_current_admin',)
                }),
            )

        return declared_fieldsets
    declared_fieldsets = property(_declared_fieldsets)
