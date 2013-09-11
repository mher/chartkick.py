# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import itertools

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateNotFound

from .template import CHART_HTML
from .options import Options


class ChartExtension(Extension):
    tags = set(['line_chart', 'pie_chart', 'column_chart',
                'bar_chart', 'area_chart'])

    id = itertools.count()
    _library = None

    def __init__(self, environment):
        super(ChartExtension, self).__init__(environment)

        environment.extend(
            options=dict(height='300px'),
        )

    def parse(self, parser):
        # parse chart name
        chart_tag = parser.stream.next()

        args = [parser.parse_expression()]

        # parse 'with' statement
        if parser.stream.current.type != 'block_end':
            token = parser.stream.next()
            if token.value != 'with':
                parser.fail("expected 'with' statement", token.lineno)

        # parse options
        while parser.stream.current.type != 'block_end':
            lineno = parser.stream.current.lineno

            target = parser.parse_assign_target()
            parser.stream.expect('assign')
            expr = parser.parse_expression()

            args.append(nodes.Assign(target, expr, lineno=lineno))

        self.environment.options['name'] = self._chart_name(chart_tag.value)
        self.environment.options['id'] = self._chart_id()

        return nodes.CallBlock(self.call_method('_render', args),
                               [], [], []).set_lineno(chart_tag.lineno)

    def _render(self, data, caller, **kwargs):
        # jinja2 prepends 'l_' to keys
        kwargs = dict((k[2:], v) for (k, v) in kwargs.items())

        if self._library is None:
            self._library = self.load_library()
        id = kwargs.get('id', self.environment.options['id'])
        library = self._library.get(id, {})

        # apply options from a tag
        library.update(kwargs.get('library', {}))
        # apply options from chartkick.json
        kwargs.update(library=library)

        self.environment.options.update(kwargs)
        return CHART_HTML.format(data=data, options=json.dumps(kwargs),
                                 **self.environment.options)

    def _chart_name(self, tag_name):
        "converts chart tag name to chart name"
        return ''.join(map(str.title, tag_name.split('_')))

    def _chart_id(self):
        "generates a chart id"
        return 'chart-%s' % self.id.next()

    def load_library(self):
        "loads configuration options"
        try:
            filename = self.environment.get_template('chartkick.json').filename
        except TemplateNotFound:
            return {}
        else:
            options = Options()
            options.load(filename)
            return options


charts = ChartExtension
