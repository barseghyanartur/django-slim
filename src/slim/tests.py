from __future__ import print_function

__title__ = 'slim.tests'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import unittest
import os

from six import text_type

PROJECT_DIR = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

PRINT_INFO = True

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        print('\n\n{0}'.format(func.__name__))
        print('============================')
        if func.__doc__:
            print('""" {0} """'.format(func.__doc__.strip()))
        print('----------------------------')
        if result is not None:
            print(result)
        print('\n++++++++++++++++++++++++++++')

        return result
    return inner

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import sys

PY3 = sys.version_info[0] == 3

_ = lambda s: s

# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):

    from foo.models import FooItem

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    class SlimTest(unittest.TestCase): #unittest.TestCase
        """
        Tests of ``slim.models`` module.
        """

        def setUp(self):
            super(SlimTest, self).setUp()

            self.FOO_ITEM_EN_TITLE = "Foo title EN"
            self.FOO_ITEM_EN_BODY = "Foo body EN"
            self.FOO_ITEM_EN_SLUG = "foo-title-en"
            self.FOO_ITEM_EN_LANGUAGE = "en"

            self.FOO_ITEM_HY_TITLE = "Foo title HY"
            self.FOO_ITEM_HY_BODY = "Foo body HY"
            self.FOO_ITEM_HY_SLUG = "foo-title-hy"
            self.FOO_ITEM_HY_LANGUAGE = "hy"

            self.FOO_ITEM_NL_TITLE = "Foo title NL"
            self.FOO_ITEM_NL_BODY = "Foo body NL"
            self.FOO_ITEM_NL_SLUG = "foo-title-nl"
            self.FOO_ITEM_NL_LANGUAGE = "nl"

            self.FOO_ITEM_RU_TITLE = "Foo title RU"
            self.FOO_ITEM_RU_BODY = "Foo body RU"
            self.FOO_ITEM_RU_SLUG = "foo-title-ru"
            self.FOO_ITEM_RU_LANGUAGE = "ru"

        def __get_or_create_foo_items(self):
            # *************************************
            # ******** Creating main item *********
            # *************************************
            try:
                foo_item_en = FooItem._default_manager.get(slug=self.FOO_ITEM_EN_SLUG)

            except Exception as e:
                foo_item_en = FooItem(
                    title = self.FOO_ITEM_EN_TITLE,
                    body = self.FOO_ITEM_EN_BODY,
                    slug = self.FOO_ITEM_EN_SLUG,
                    language = self.FOO_ITEM_EN_LANGUAGE
                    )
                foo_item_en.save()

            # *************************************
            # ********* Armenian translation ******
            # *************************************
            try:
                foo_item_hy = FooItem._default_manager.get(slug=self.FOO_ITEM_HY_SLUG)

            except Exception as e:
                foo_item_hy = FooItem(
                    title = self.FOO_ITEM_HY_TITLE,
                    body = self.FOO_ITEM_HY_BODY,
                    slug = self.FOO_ITEM_HY_SLUG,
                    language = self.FOO_ITEM_HY_LANGUAGE,
                    translation_of = foo_item_en
                    )
                foo_item_hy.save()

                # *************************************
                # ********* Dutch translation *********
                # *************************************
            try:
                foo_item_nl = FooItem._default_manager.get(slug=self.FOO_ITEM_NL_SLUG)

            except Exception as e:
                foo_item_nl = FooItem(
                    title = self.FOO_ITEM_NL_TITLE,
                    body = self.FOO_ITEM_NL_BODY,
                    slug = self.FOO_ITEM_NL_SLUG,
                    language = self.FOO_ITEM_NL_LANGUAGE,
                    translation_of = foo_item_en
                    )
                foo_item_nl.save()

                # *************************************
                # ********* Russian translation *******
                # *************************************
            try:
                foo_item_ru = FooItem._default_manager.get(slug=self.FOO_ITEM_RU_SLUG)

            except Exception as e:
                foo_item_ru = FooItem(
                    title = self.FOO_ITEM_RU_TITLE,
                    body = self.FOO_ITEM_RU_BODY,
                    slug = self.FOO_ITEM_RU_SLUG,
                    language = self.FOO_ITEM_RU_LANGUAGE,
                    translation_of = foo_item_en
                    )
                foo_item_ru.save()

            return (foo_item_en, foo_item_hy, foo_item_nl, foo_item_ru)

        @print_info
        def test_01_get_translations(self):
            """
            Test ``get_translation_for`` method.
            """
            flow = []

            foo_item_en, foo_item_hy, foo_item_nl, foo_item_ru = self.__get_or_create_foo_items()

            flow.append(foo_item_en)

            # Test Armenian translation
            self.assertTrue(foo_item_en.get_translation_for('hy') == foo_item_hy)

            flow.append(foo_item_hy)

            # Test Dutch translation
            self.assertTrue(foo_item_en.get_translation_for('nl') == foo_item_nl)

            flow.append(foo_item_nl)

            # Test Russian translation
            self.assertTrue(foo_item_en.get_translation_for('ru') == foo_item_ru)

            flow.append(foo_item_ru)

            return flow

        @print_info
        def test_02_available_translations(self):
            """
            Test ``available_translations`` method.
            """
            flow = []

            foo_item_en, foo_item_hy, foo_item_nl, foo_item_ru = self.__get_or_create_foo_items()

            available_translations = [foo_item.pk for foo_item in foo_item_en.available_translations()]
            available_translations.sort()

            translations = [foo_item_hy.pk, foo_item_nl.pk, foo_item_ru.pk]
            translations.sort()

            self.assertTrue(available_translations == translations)

            flow.append(available_translations)
            flow.append(translations)

            return flow

        @print_info
        def test_03_auto_prepend_language_model_decorator(self):
            """
            Test the ``auto_prepend_language`` model decorator.
            """
            flow = []

            foo_item_en, foo_item_hy, foo_item_nl, foo_item_ru = self.__get_or_create_foo_items()

            self.assertTrue(
                text_type(foo_item_en.get_absolute_url()) == \
                text_type('/{0}/foo/{1}/').format(self.FOO_ITEM_EN_LANGUAGE, self.FOO_ITEM_EN_SLUG)
                )

            flow.append(foo_item_en.get_absolute_url())

            self.assertTrue(
                text_type(foo_item_hy.get_absolute_url()) == \
                text_type('/{0}/foo/{1}/').format(self.FOO_ITEM_HY_LANGUAGE, self.FOO_ITEM_HY_SLUG)
                )

            flow.append(foo_item_hy.get_absolute_url())

            self.assertTrue(
                text_type(foo_item_nl.get_absolute_url()) == \
                text_type('/{0}/foo/{1}/').format(self.FOO_ITEM_NL_LANGUAGE, self.FOO_ITEM_NL_SLUG)
                )

            flow.append(foo_item_nl.get_absolute_url())

            self.assertTrue(
                text_type(foo_item_ru.get_absolute_url()) == \
                text_type('/{0}/foo/{1}/').format(self.FOO_ITEM_RU_LANGUAGE, self.FOO_ITEM_RU_SLUG)
                )

            flow.append(foo_item_ru.get_absolute_url())

            return flow

        @print_info
        def test_04_original_translation(self):
            """
            Test ``original_translation`` method.
            """
            flow = []

            foo_item_en, foo_item_hy, foo_item_nl, foo_item_ru = self.__get_or_create_foo_items()

            self.assertTrue(foo_item_hy.original_translation == foo_item_en)
            self.assertTrue(foo_item_nl.original_translation == foo_item_en)
            self.assertTrue(foo_item_ru.original_translation == foo_item_en)

            #return flow


if __name__ == "__main__":
    # Tests
    unittest.main()