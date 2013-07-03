from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from slim.admin import SlimAdmin

from foo.models import FooItem

class FooItemAdmin(SlimAdmin):
    """
    Foo item admin.
    """
    # If you don't inherit the SlimAdmin, append 'language' and 'available_translations_admin' to ``list_display``.
    list_display = ('title', 'admin_image_preview', 'date_published')

    # If you don't inherit the SlimAdmin, uncomment the following line.
    #list_filter = ('language',)

    # If you don't inherit the SlimAdmin, append 'available_translations_exclude_current_admin' to ``readonly_fields``.
    readonly_fields = ('date_created', 'date_updated', )

    prepopulated_fields = {'slug': ('title',)}

    collapse_slim_fieldset = False

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body', 'image')
        }),
        (_("Publication date"), {
            'classes': ('',),
            'fields': ('date_published',)
        }),
        # If you don't inherit the SlimAdmin, uncomment the following lines.
        #(_("Translations"), {
        #    'classes': ('collapse',),
        #    'fields': ('language', 'translation_of', 'available_translations_exclude_current_admin',)
        #}),
        (_("Additional"), {
            'classes': ('collapse',),
            'fields': ('date_created', 'date_updated') #,
        })
    )

    class Meta:
        app_label = _('Foo item')

admin.site.register(FooItem, FooItemAdmin)
