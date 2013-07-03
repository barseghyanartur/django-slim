from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation

from slim.helpers import get_language_from_request

from foo.models import FooItem


def browse(request, template_name='foo/browse.html'):
    """
    In the template, we show all available FooItems for current language.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    language = get_language_from_request(request)

    results_kwargs = {}

    if language is not None:
        translation.activate(language)
        results_kwargs.update({'language': language})

    queryset = FooItem._default_manager.filter(**results_kwargs).order_by('-date_published')

    context = {'items': queryset}

    return render_to_response(template_name, context, context_instance=RequestContext(request))


def detail(request, slug, template_name='foo/detail.html'):
    """
    Foo item detail. In the template, we show the title and the body of the FooItem and links to all its' all
    available translations.

    :param django.http.HttpRequest request:
    :param str slug: Foo item slug.
    :param str template_name:
    :return django.http.HttpResponse:
    """
    language = get_language_from_request(request)

    if language is not None:
        translation.activate(language)

    results_kwargs = {'slug': slug}

    try:
        queryset = FooItem._default_manager.filter(**results_kwargs)

        item = queryset.get(**results_kwargs)
    except Exception, e:
        raise Http404

    context = {'item': item}

    return render_to_response(template_name, context, context_instance=RequestContext(request))
