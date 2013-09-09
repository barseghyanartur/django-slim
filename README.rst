Package
===================================
django-slim

Description
===================================
Simple implementation of multi-lingual models for Django. Django-admin integration works out of the box.
Supports `django-localeurl` integration.

Prerequisites
===================================
- Django 1.5.+
- Python 2.7.+, 3.3.+

Installation
===================================
Note, that Django 1.5 is required. Earlier versions are not supported.

1. Installation

Latest stable version on PyPI
-----------------------------------
    $ pip install django-slim

Latest stable version on bitbucket
-----------------------------------

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/django-slim@stable#egg=django-slim

Latest stable version on github
-----------------------------------

    $ pip install -e git+https://github.com/barseghyanartur/django-slim/@stable#egg=django-slim

2. Add `slim` to ``INSTALLED_APPS`` of you settings module.

Usage and examples
===================================
An extensive example project is available at https://github.com/barseghyanartur/django-slim/tree/stable/example
directory.

Automated example installer
-----------------------------------
An automated installer exists as well (Debian only).

Grab the latest `django-slim-example-app-install.sh`

    $ wget https://raw.github.com/barseghyanartur/django-slim/stable/django-slim-example-app-install.sh

Create a new- or switch to existing- virtual environement, assign execute rights to the installer and run
the `django-slim-example-app-install.sh`.

    $ chmod +x django-slim-example-app-install.sh

    $ ./django-slim-example-app-install.sh

You would then have a working demo within a minute.

Let's now step-by-step review our imaginary example app.

settings.py
-----------------------------------
Add `slim` to installed apps.

>>> INSTALLED_APPS = (
>>>     # ...
>>>     'slim',
>>>     # ...
>>> )

Add languages.

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
>>>     body = models.TextField(_("Body"))
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
Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
django-localeurl integration is fully supported for Python 2.6.* and 2.7.* and installes automatically
when installing django-slim. If you are using Python 3, install a forked version of django-localeurl
(since official version does not yet have support for Python 3).

Forked version from bitbucket:

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/django-localeurl@stable#egg=localeurl

Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use `slim.models.decorators.auto_prepend_language` decorator in order to have it working.

Example (have in mind our `FooItem` model.

>>> from django.core.urlresolvers import reverse
>>>
>>> from slim.models.decorators import auto_prepend_language
>>>
>>> class FooItem(models.Model):
>>>     # Some other code; have in mind previous pieces.
>>>     @auto_prepend_language
>>>     def get_absolute_url(self):
>>>         kwargs = {'slug': self.slug}
>>>         return reverse('foo.detail', kwargs=kwargs)

Do not forget to add the ``LocaleURLMiddleware`` to the ``MIDDLEWARE_CLASSES`` (as first).

>>> MIDDLEWARE_CLASSES = (
>>>     'localeurl.middleware.LocaleURLMiddleware',
>>>     # The rest...
>>> )

Also, add `localeurl` to ``INSTALLED_APPS``.

>>> INSTALLED_APPS = (
>>>     # Some apps...
>>>     'localeurl',
>>>     # Some more apps...
>>> )

License
===================================
GPL 2.0/LGPL 2.1

Support
===================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================
Artur Barseghyan <artur.barseghyan@gmail.com>
