from __future__ import absolute_import

import json
import functools
import itertools

from django import template
from django.conf import settings


from ..template import CHART_HTML


register = template.Library()


class ChartNode(template.Node):
    id = itertools.count()

    def __init__(self, name, variable, options=None):
        self.name = name
        self.variable = template.Variable(variable)
        self.options = options or {}

        for name, value in self.options.items():
            self.options[name] = template.Variable(value)

    def render(self, context):
        options = dict(id='chart-%s' % self.id.next(), height='300px')
        options.update(self.options)

        for name, value in options.items():
            if isinstance(value, template.Variable):
                options[name] = value.resolve(context)

        data = json.dumps(self.variable.resolve(context))
        return CHART_HTML.format(name=self.name, data=data,
                                 options=json.dumps(options), **options)


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
            options = dict(map(lambda x: x.split('='), args[3:]))
        except ValueError:
            raise template.TemplateSyntaxError('Invalid arguments')

    return ChartNode(name=name, variable=args[1], options=options)


register.tag('line_chart', functools.partial(chart, 'LineChart'))
register.tag('pie_chart', functools.partial(chart, 'PieChart'))
register.tag('column_chart', functools.partial(chart, 'ColumnChart'))
