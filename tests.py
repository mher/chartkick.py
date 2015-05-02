import re
import unittest

from django.template import Template, Context
from django.template import TemplateSyntaxError as DjangoTemplateSyntaxError
from django.conf import settings

from jinja2 import TemplateSyntaxError as Jinja2TemplateSyntaxError
from jinja2 import Environment
from jinja2 import FileSystemLoader

import chartkick


# python 2.6 support
if not hasattr(unittest.TestCase, 'assertIn'):
    import unittest2 as unittest


settings.configure()
settings.INSTALLED_APPS = ('chartkick',)
settings.STATICFILES_DIRS = (chartkick.js(),)
settings.STATIC_URL = ''


import django
django.setup()


class TestsBase(object):

    TemplateSyntaxError = None

    def render(self, template, context=None):
        raise NotImplementedError

    def test_missing_vaiable(self):
        self.assertRaises(self.TemplateSyntaxError,
                          self.render, '{% line_chart %}')

    def test_empty(self):
        chart = self.render('{% line_chart data %}', dict(data={}))
        self.assertIn('Chartkick.LineChart', chart)
        self.assertIn('id', chart)
        self.assertIn('height', chart)

    def test_line_chart(self):
        chart = self.render('{% line_chart data %}', dict(data={}))
        self.assertIn('Chartkick.LineChart', chart)
        self.assertNotIn('Chartkick.PieChart', chart)
        self.assertNotIn('Chartkick.ColumnChart', chart)
        self.assertNotIn('Chartkick.BarChart', chart)
        self.assertNotIn('Chartkick.AreaChart', chart)

    def test_pie_chart(self):
        chart = self.render('{% pie_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertIn('Chartkick.PieChart', chart)
        self.assertNotIn('Chartkick.ColumnChart', chart)
        self.assertNotIn('Chartkick.BarChart', chart)
        self.assertNotIn('Chartkick.AreaChart', chart)

    def test_column_chart(self):
        chart = self.render('{% column_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertNotIn('Chartkick.PieChart', chart)
        self.assertIn('Chartkick.ColumnChart', chart)
        self.assertNotIn('Chartkick.BarChart', chart)
        self.assertNotIn('Chartkick.AreaChart', chart)

    def test_bar_chart(self):
        chart = self.render('{% bar_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertNotIn('Chartkick.PieChart', chart)
        self.assertNotIn('Chartkick.ColumnChart', chart)
        self.assertIn('Chartkick.BarChart', chart)
        self.assertNotIn('Chartkick.AreaChart', chart)

    def test_area_chart(self):
        chart = self.render('{% area_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertNotIn('Chartkick.PieChart', chart)
        self.assertNotIn('Chartkick.ColumnChart', chart)
        self.assertNotIn('Chartkick.BarChart', chart)
        self.assertIn('Chartkick.AreaChart', chart)

    def test_all_charts(self):
        template = """{% line_chart data %}
                      {% pie_chart data %}
                      {% column_chart data %}
                      {% bar_chart data %}
                      {% area_chart data %}"""
        chart = self.render(template, dict(data={}))

        self.assertIn('Chartkick.LineChart', chart)
        self.assertIn('Chartkick.PieChart', chart)
        self.assertIn('Chartkick.ColumnChart', chart)
        self.assertIn('Chartkick.BarChart', chart)
        self.assertIn('Chartkick.AreaChart', chart)

    @unittest.skip('Embedded data is not implemented yet')
    def test_data_embeded(self):
        chart = self.render('{% line_chart {"foo":35,"bar":12} %}')
        self.assertIn('foo', chart)
        self.assertIn('bar', chart)

    def test_data_context(self):
        chart = self.render('{% line_chart foo %}', dict(foo='bar'))
        self.assertNotIn('foo', chart)
        self.assertIn('bar', chart)

    def test_missing_with(self):
        self.assertRaises(self.TemplateSyntaxError,
                          self.render, '{% line_chart data x=y %}')

    def test_options_embeded(self):
        chart = self.render('{% line_chart foo with library={"title": "eltit"} %}',
                            dict(foo='bar'))
        self.assertNotIn('foo', chart)
        self.assertIn('bar', chart)
        self.assertIn('library', chart)
        self.assertIn('title', chart)
        self.assertIn('eltit', chart)

    def test_options_context(self):
        chart = self.render('{% line_chart "" with foo=bar %}',
                            dict(bar=123))
        self.assertNotIn('data', chart)
        self.assertIn('foo', chart)
        self.assertNotIn('bar', chart)
        self.assertIn('123', chart)

    def test_spaces(self):
        templates = ('{%line_chart data %}', '{%  line_chart data %}',
                     '{% line_chart  data  %}', '{%  line_chart data%}',
                     '{%  line_chart  data  with  x="foo  bar" %}',
                     '{%  line_chart  data with  x=1%}')

        for template in templates:
            chart = self.render(template, dict(data='foo'))
            self.assertIn('Chartkick.LineChart', chart)
            self.assertNotIn('data', chart)
            self.assertIn('foo', chart)

    def test_id(self):
        chart1 = self.render('{% line_chart "" with id=123 %}')
        chart2 = self.render('{% line_chart "" %}{% line_chart "" %}')
        ids = re.findall('id=\"(.*?)\"', chart2)

        self.assertIn('123', chart1)
        self.assertIn('id', chart1)
        self.assertNotEqual(ids[0], ids[1])

    def test_invalid_options(self):
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library= %}')
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library={"title":"test" %}')
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library="title":"test" %}')
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library={"title: "test"} %}')
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library={"title": "test} %}')
        self.assertRaises(self.TemplateSyntaxError, self.render,
                '{% line_chart "" with library={"title": } %}')


class DjangoTests(unittest.TestCase, TestsBase):

    TemplateSyntaxError = DjangoTemplateSyntaxError

    def render(self, template, context=None):
        context = context or {}
        template = '{% load chartkick %}' + template
        t = Template(template)
        c = Context(context)
        return t.render(c)


class Jinja2Tests(unittest.TestCase, TestsBase):

    TemplateSyntaxError = Jinja2TemplateSyntaxError

    def render(self, template, context=None):
        context = context or {}
        env = Environment(extensions=['chartkick.ext.charts'])
        env.loader = FileSystemLoader('.')
        return env.from_string(template).render(context)


if __name__ == '__main__':
    unittest.main()
