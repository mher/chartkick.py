Chartkick.py
============

Create beautiful Javascript charts with minimal code. Python port of Chartkick_

Supports `Google Charts`_ and Highcharts_

Works with Django, Flask/Jinja2 and with most browsers (including IE 6)

.. _Chartkick: http://chartkick.com
.. _Google Charts: https://developers.google.com/chart/
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

- **Django**: Add chartkick to *INSTALLED_APPS* and *STATICFILES_DIRS*: ::

    INSTALLED_APPS = (
        'chartkick',
    )

    import chartkick
    STATICFILES_DIRS = (
        chartkick.js(),
    )

- **Flask**: Add chartkick to *jinja_env* and *static_folder*: ::

    app = Flask(__name__, static_folder=chartkick.js(), static_url_path='/static')
    app.jinja_env.add_extension("chartkick.ext.charts")

Load JS scripts:

- **Google Charts** ::

    <script src="http://www.google.com/jsapi"></script>
    <script src="static/chartkick.js"></script>

- **Highcharts** ::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src="http://code.highcharts.com/highcharts.js"></script>
    <script src="static/chartkick.js"></script>
