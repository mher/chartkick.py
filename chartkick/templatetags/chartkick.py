from __future__ import absolute_import

import os
import ast
import json
import functools
import itertools

from django import template
from django.template import Engine
from django.template.loaders.filesystem import Loader

from ..template import CHART_HTML
from ..options import Options


register = template.Library()


class ChartNode(template.Node):
    id = itertools.count()
    _library = None

    def __init__(self, name, variable, options=None):
        self.name = name
        self.variable = template.Variable(variable)
        self.options = options or {}

        for name, value in self.options.items():
            try:
                self.options[name] = ast.literal_eval(value)
            except ValueError:
                self.options[name] = template.Variable(value)
            except SyntaxError as e:
                raise template.TemplateSyntaxError(e)

    def render(self, context):
        for name, value in self.options.items():
            if isinstance(value, template.Variable):
                self.options[name] = value.resolve(context)

        options = dict(id='chart-%s' % next(self.id), height='300px')
        id = self.options.get('id', None) or options['id']

        # apply options from chartkick.json
        options.update(library=self.library(id))
        # apply options from a tag
        options.update(self.options)

        data = json.dumps(self.variable.resolve(context))
        return CHART_HTML.format(name=self.name, data=data,
                                 options=json.dumps(options), **options)

    @classmethod
    def library(cls, chart_id):
        if cls._library is None:
            loader = Loader(Engine())
            for filename in loader.get_template_sources('chartkick.json'):
                if os.path.exists(filename):
                    oprtions = Options()
                    oprtions.load(filename)
                    cls._library = oprtions
                    break
            else:
                cls._library = Options()

        return cls._library.get(chart_id, {})


def chart(name, parser, token):
    args = token.split_contents()

    if len(args) < 2:
        raise template.TemplateSyntaxError(
                '%r statement requires at least one argument' %
                token.split_contents()[0])

    options = None
    if len(args) > 2:
        if args[2] != 'with':
            raise template.TemplateSyntaxError("Expected 'with' statement")

        try:
            options = parse_options(' '.join(args[3:]))
        except ValueError:
            raise template.TemplateSyntaxError('Invalid options')

    return ChartNode(name=name, variable=args[1], options=options)


def parse_options(source):
    """parses chart tag options"""
    options = {}
    tokens = [t.strip() for t in source.split('=')]

    name = tokens[0]
    for token in tokens[1:-1]:
        value, next_name = token.rsplit(' ', 1)
        options[name.strip()] = value
        name = next_name
    options[name.strip()] = tokens[-1].strip()
    return options


register.tag('line_chart', functools.partial(chart, 'LineChart'))
register.tag('pie_chart', functools.partial(chart, 'PieChart'))
register.tag('column_chart', functools.partial(chart, 'ColumnChart'))
register.tag('bar_chart', functools.partial(chart, 'BarChart'))
register.tag('area_chart', functools.partial(chart, 'AreaChart'))
