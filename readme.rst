Package
===================================
django-slim

Description
===================================
Simple implementation of multi-lingual models for Django. Django-admin integration works out of the box.
Supports `django-localeurl` integration.

Installation
===================================
1. Installation

To install latest stable version from pypi:

    $ pip install django-slim

To install latest stable version from source:

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/django-slim@stable#egg=django-slim

2. Add `slim` to ``INSTALLED_APPS`` of you settings module.

Usage and examples
===================================
An extensive example project is available at https://bitbucket.org/barseghyanartur/django-slim/src (see `example`
directory). An automated installer exists as well (Debian only). Grab the latest `django-slim-example-app-install.sh`
file from root directory, create a new- or switch to existing- virtual environement and run the
`django-slim-example-app-install.sh`. You would then have a working demo within a minute.

Let's now step-by-step review our imaginary example app.

settings.py
-----------------------------------
>>> INSTALLED_APPS = (
>>>     # ...
>>>     'slim',
>>>     # ...
>>> )

>>> LANGUAGES = (
>>>     ('en', gettext("English")), # Main language!
>>>     ('am', gettext("Armenian")),
>>>     ('nl', gettext("Dutch")),
>>>     ('ru', gettext("Russian")),
>>> )

example/models.py
-----------------------------------
>>> from django.db import models
>>>
>>> from slim import LanguageField, Slim
>>>
>>> class FooItem(models.Model, Slim):
>>>     title = models.CharField(_("Title"), max_length=100)
>>>     slug = models.SlugField(unique=True, verbose_name=_("Slug"))
>>>     body = HTMLField(_("Body"))
>>>     language = LanguageField()

example/admin.py
-----------------------------------
>>> from django.contrib import admin
>>>
>>> from slim.admin import SlimAdmin
>>>
>>> class FooItemAdmin(SlimAdmin):
>>>     list_display = ('title',)
>>>     fieldsets = (
>>>         (None, {
>>>             'fields': ('title', 'slug', 'body')
>>>         }),
>>>     )
>>>
>>> admin.site.register(FooItem, FooItemAdmin)

example/views.py
-----------------------------------
We assume that language code is kept in the request object (django-localeurl behaviour, which you're advised to use).

>>> from slim import get_language_from_request
>>>
>>> from example.models import FooItem
>>>
>>> def browse(request, template_name='foo/browse.html'):
>>>     language = get_language_from_request(request)
>>>     queryset = FooItem._default_manager.filter(language=language)
>>>
>>>     # The rest of the code

More on ORM filtering
-----------------------------------
>>> from example.models import FooItem
>>> foo = FooItem._default_manager.all()[0]
<FooItem: Lorem ipsum>

Let's assume, we have such record and it has been translated to Armenian (`am`) and Dutch (`nl`). Original
translation is named `Lorem ipsum`. Other translations have the language code appended to the title.

>>> armenian_foo = foo.get_translation_for('am')
<FooItem: Lorem ipsum AM>
>>> dutch_foo = foo.get_translation_for('nl')
<FooItem: Lorem ipsum NL>

If we have a translated object, we can always get the main translation.

>>> armenian_foo.original_translation == foo
True

All available translations for ``foo``:

>>> foo.available_translations.all()
[<FooItem: Lorem ipsum AM>, <FooItem: Lorem ipsum NL>]

All available translations for Armenian ``foo``.

>>> armenian_foo.available_translations.all()
[<FooItem: Lorem ipsum>, <FooItem: Lorem ipsum NL>]

See https://bitbucket.org/barseghyanartur/django-slim/src (example) directory for a working example.

django-localeurl integration
-----------------------------------
django-localeurl integration is supported. Use `slim.models.decorators.auto_prepend_language` decorator
in order to have it working.

Example (have in mind our `FooItem` model.

>>> from django.core.urlresolvers import reverse
>>>
>>> from slim.models.decorators import auto_prepend_language
>>>
>>> class FooItem(models.Model):
>>>     # Some other code; have in mind previous pieces.
>>>     @auto_prepend_language
>>>     def get_absolute_url(self):
>>>         kwargs = {
>>>             'slug': self.slug
>>>             }
>>>         return reverse('foo.detail', kwargs=kwargs)

License
===================================
GPL 2.0/LGPL 2.1

Support
===================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================
Artur Barseghyan <artur.barseghyan@gmail.com>
