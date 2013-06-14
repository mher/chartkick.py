import unittest

from django.template import Template, Context, TemplateSyntaxError
from django.conf import settings

import chartkick


settings.configure()
settings.INSTALLED_APPS = ('chartkick',)
settings.STATICFILES_DIRS = (chartkick.js(),)
settings.STATIC_URL = ''


class TestCharts(unittest.TestCase):

    def render(self, template, context=None):
        context = context or {}
        template = '{% load chartkick %}' + template
        t = Template(template)
        c = Context(context)
        return t.render(c)

    def test_include_chartkick_scripts(self):
        header = self.render('{% include_chartkick_scripts %}')
        self.assertIn('google.com', header)
        self.assertNotIn('highcharts.com', header)

        header = self.render('{% include_chartkick_scripts "googlecharts" %}')
        self.assertIn('google.com', header)
        self.assertNotIn('highcharts.com', header)

        header = self.render('{% include_chartkick_scripts "highcharts" %}')
        self.assertIn('highcharts.com', header)
        self.assertNotIn('google.com', header)

    def test_missing_vaiable(self):
        self.assertRaises(TemplateSyntaxError, self.render, '{% line_chart %}')

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

    def test_pie_chart(self):
        chart = self.render('{% pie_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertIn('Chartkick.PieChart', chart)
        self.assertNotIn('Chartkick.ColumnChart', chart)

    def test_column_chart(self):
        chart = self.render('{% column_chart data %}', dict(data={}))
        self.assertNotIn('Chartkick.LineChart', chart)
        self.assertNotIn('Chartkick.PieChart', chart)
        self.assertIn('Chartkick.ColumnChart', chart)

    def test_data_embeded(self):
        pass

    def test_data_context(self):
        chart = self.render('{% line_chart foo %}', dict(foo='bar'))
        self.assertNotIn('foo', chart)
        self.assertIn('bar', chart)

    def test_missing_with(self):
        self.assertRaises(TemplateSyntaxError,
                          self.render, '{% line_chart data x=y %}')

    def test_options_embeded(self):
        pass

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
        chart = self.render('{% line_chart "" with id=123 %}')
        self.assertIn('"id": 123', chart)


if __name__ == '__main__':
    unittest.main()
