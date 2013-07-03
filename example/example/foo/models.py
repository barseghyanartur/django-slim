import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

from slim import Slim, LanguageField
from slim.models.decorators import auto_prepend_language

FOO_IMAGES_STORAGE_PATH = 'foo-images'


def _foo_images(instance, filename):
    """
    Store the images in their own folder. This allows us to keep thumbnailed versions of all images.
    """
    if instance.pk:
        return '%s/%s-%s' % (FOO_IMAGES_STORAGE_PATH, str(instance.pk), filename.replace(' ', '-'))
    return '%s/%s' % (FOO_IMAGES_STORAGE_PATH, filename.replace(' ', '-'))


class FooItem(models.Model, Slim):
    """
    Foo item.

    ``title`` Title of the news item.
    ``body`` Teaser of the news item. WYSIWYG.
    ``image`` Headline image of the news item.
    ``date_published`` Date item is published. On creating defaults to ``datetime.datetime.now``.
    ``language`` Language.
    """
    title = models.CharField(_("Title"), max_length=100)
    body = models.TextField(_("Body"))
    image = models.ImageField(_("Headline image"), blank=True, null=True, upload_to=_foo_images)
    date_published = models.DateTimeField(_("Date published"), blank=True, null=True, default=datetime.datetime.now())
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))

    language = LanguageField()

    date_created = models.DateTimeField(_("Date created"), blank=True, null=True, auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("Date updated"), blank=True, null=True, auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Foo item")
        verbose_name_plural = _("Foo items")

    def __unicode__(self):
        return self.title

    @auto_prepend_language
    def get_absolute_url(self):
        """
        Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        kwargs = {
            'slug': self.slug
            }
        return reverse('foo.detail', kwargs=kwargs)

    def admin_image_preview(self):
        """
        Preview of the ``image``. For admin use mainly.

        :return str:
        """
        if self.image:
            return render_to_string('foo/_image_preview.html', {'alt': self.title, 'image_file': self.image})
        else:
            return u''
    admin_image_preview.allow_tags = True
    admin_image_preview.short_description = _('Image')
