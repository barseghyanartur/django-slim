===========
django-slim
===========
Simple implementation of multi-lingual models for Django. Django-admin
integration works out of the box.

Prerequisites
=============
- Django 1.5, 1.6, 1.7
- Python 2.7, 3.4, 3.5, 3.6

Installation
============
Note, that Django 1.5 is required. Earlier versions are not supported.

1. Installation

Latest stable version on PyPI:

.. code-block:: sh

    pip install django-slim

Latest stable version on BitBucket:

.. code-block:: sh

    pip install https://bitbucket.org/barseghyanartur/django-slim/get/stable.tar.gz

Latest stable version on GitHub:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-slim/archive/stable.tar.gz

2. Add ``slim`` to ``INSTALLED_APPS`` of you settings module.

Usage and examples
==================
An extensive `example project
<https://github.com/barseghyanartur/django-slim/tree/stable/example>`_ is
available.

Screen shots are present in `documentation
<http://pythonhosted.org/django-slim/#screenshots>`_ on PythonHosted.

Demo
----
In order to be able to quickly evaluate the django-slim, a demo app (with a
quick installer) has been created (Debian only). Follow the instructions below
for having the demo running within a minute.

Grab the latest ``django_slim_example_app_installer.sh``:

.. code-block:: sh

    wget https://raw.github.com/barseghyanartur/django-slim/stable/example/django_slim_example_app_installer.sh

Create a new- or switch to existing- virtual environment, assign execute rights
to the installer and run the ``django-slim-example-app-install.sh``.

.. code-block:: sh

   chmod +x django_slim_example_app_installer.sh

    ./django_slim_example_app_installer.sh

Go to the front/back -end and test the app.

.. code-block:: text

   - Front-end URL: http://127.0.0.1:8001/en/foo/
   - Admin URL: http://127.0.0.1:8001/admin/foo/fooitem/
   - Admin username: admin
   - Password: test

Let's now step-by-step review our imaginary example app.

settings.py
-----------
Add ``slim`` to installed apps.

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'slim',
        # ...
    )

Add languages.

.. code-block:: python

    LANGUAGES = (
        ('en', gettext("English")),  # Main language!
        ('hy', gettext("Armenian")),
        ('nl', gettext("Dutch")),
        ('ru', gettext("Russian")),
    )

example/models.py
-----------------
.. code-block:: python

    from django.db import models

    from slim import LanguageField, Slim

    class FooItem(models.Model, Slim):

        title = models.CharField(_("Title"), max_length=100)
        slug = models.SlugField(unique=True, verbose_name=_("Slug"))
        body = models.TextField(_("Body"))
        language = LanguageField()

example/admin.py
----------------
.. code-block:: python

    from django.contrib import admin

    from slim.admin import SlimAdmin

    class FooItemAdmin(SlimAdmin):

        list_display = ('title',)
        fieldsets = (
            (None, {
                'fields': ('title', 'slug', 'body')
            }),
        )

    admin.site.register(FooItem, FooItemAdmin)

example/views.py
----------------
We assume that language code is kept in the request object (django-localeurl
behaviour, which you're advised to use).

.. code-block:: python

    from slim import get_language_from_request

    from example.models import FooItem

    def browse(request, template_name='foo/browse.html'):
        language = get_language_from_request(request)
        queryset = FooItem._default_manager.filter(language=language)

        # The rest of the code

More on ORM filtering
---------------------
.. code-block:: python

    from example.models import FooItem
    foo = FooItem._default_manager.all()[0]

.. code-block:: text

    <FooItem: Lorem ipsum>

Let's assume, we have such record and it has been translated to
Armenian (``hy``) and Dutch (``nl``). Original translation is named
``Lorem ipsum``. Other translations have the language code appended to the
title.

.. code-block:: python

    armenian_foo = foo.get_translation_for('hy')

.. code-block:: text

    <FooItem: Lorem ipsum HY>

.. code-block:: python

    dutch_foo = foo.get_translation_for('nl')

.. code-block:: text

    <FooItem: Lorem ipsum NL>

If we have a translated object, we can always get the main translation.

.. code-block:: python

    armenian_foo.original_translation == foo

.. code-block:: text

    True

All available translations for ``foo``:

.. code-block:: python

    foo.available_translations()

.. code-block:: text

    [<FooItem: Lorem ipsum HY>, <FooItem: Lorem ipsum NL>]

All available translations for Armenian ``foo``.

.. code-block:: python

    armenian_foo.available_translations()

.. code-block:: text

    [<FooItem: Lorem ipsum>, <FooItem: Lorem ipsum NL>]

See `example directory
<https://github.com/barseghyanartur/django-slim/tree/stable/example>`_ for a
working example.

django-localeurl integration
----------------------------
Note, that ``django-localeurl`` usage is deprecated. We're moving to nowadays
approaches. This version (0.8) is the last version to support
``django-localeurl``.

Installation
~~~~~~~~~~~~
django-localeurl integration is fully supported for Python 2.6.* and 2.7.* and
installs automatically when installing django-slim. If you are using Python 3,
install a forked version of django-localeurl (since official version does not
yet have support for Python 3).

Forked version from BitBucket:

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/django-localeurl@stable#egg=localeurl

Integration
~~~~~~~~~~~
Use ``slim.models.decorators.auto_prepend_language`` decorator in order to have it working.

Example (have in mind our `FooItem` model.

     from django.core.urlresolvers import reverse

     from slim.models.decorators import auto_prepend_language

     class FooItem(models.Model):
         # Some other code; have in mind previous pieces.
         @auto_prepend_language
         def get_absolute_url(self):
             kwargs = {'slug': self.slug}
             return reverse('foo.detail', kwargs=kwargs)

Do not forget to add the ``LocaleURLMiddleware`` to the ``MIDDLEWARE_CLASSES`` (as first).

     MIDDLEWARE_CLASSES = (
         'localeurl.middleware.LocaleURLMiddleware',
         # The rest...
     )

Also, add `localeurl` to ``INSTALLED_APPS``.

     INSTALLED_APPS = (
         # Some apps...
         'localeurl',
         # Some more apps...
     )

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
