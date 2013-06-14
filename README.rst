Chartkick.py
============

Create beautiful Javascript charts with minimal code. Python port of Chartkick_

Supports Google Charts and Highcharts_ and works with most browsers (including IE 6)

.. _Chartkick: http://chartkick.com
.. _Highcharts: http://highcharts.com

Usage
-----

Load charkick from a template: ::

    {% load chartkick %}

And draw charts: ::

    {% line_chart data %}

    {% pie_chart data with height='400px' %}

    {% column_chart data with min=400 max=1000 %}

*data* is a context variable passed to the template: ::

    def view(request):
        data = {'Strawberry': 23, 'Apple': 21, 'Grape': 13, 'Blueberry': 44, 'Banana': 22}
        return render(request, 'template.html', {'data': data})

To draw users join chart: ::

    def view(request):
        qs = User.objects.values('join_date').order_by('-join_date')
        data = qs.annotate(count=Count('join_date'))

        data = dict(map(lambda x: (x['join_date'], x['count']), data))
        return render(request, 'template.html', {'data': data})

Installation
------------

Install chartkick: ::

    $ pip install chartkick

Add chartkick to INSTALLED_APPS and STATICFILES_DIRS: ::

    INSTALLED_APPS = (
        'chartkick',
    )

    import chartkick
    STATICFILES_DIRS = (
        chartkick.js(),
    )

And chartkick scripts to the header of base template: ::

    {% include_chartkick_scripts 'GoogleCharts' %}

Or: ::

    {% include_chartkick_scripts 'HighCharts' %}

TODO
----

- Flask/Jinja2 support
