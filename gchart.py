# encoding: utf-8

import copy

# If there is no Django available, we make a dummy mark_safe function that does nothing
try:
    from django.utils.safestring import mark_safe
except ImportError:
    mark_safe = lambda text: text

class Chart(object):
    u'''Abstract class for chart backends.'''

    class_options = {}
    
    def __init__(self, schema, data, **options):
        self.schema = schema
        self.data = data
        self.html_id = 'gchart-{}'.format(id(self))
        self.instance_options = options
        self.options = self._get_options()

    def initialize_html(self):
        u'''Code used to initalize charts, included in <head> section.'''

        return mark_safe(u'')

    def render_html(self):
        u'''Code included in <body> section where chart is meant to be displayed.'''

        return mark_safe(u'')

    def _get_options(self):
        options = copy.copy(self.class_options)
        options.update(self.instance_options)
        return options
    
    def __str__(self):
        return self.render_html()

class GoogleChart(Chart):
    def initialize_html(self):
        # TODO: separate library and package loading to be done only once
        return mark_safe(u'''
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
  google.load("visualization", "1", {{packages:["{package}"]}});
  google.setOnLoadCallback(drawChart);
  function drawChart() {{
    var data = new google.visualization.DataTable({data}, 0.6);

    var options = {{
      {options}
    }};

    var chart = new google.visualization.{chart_class}(document.getElementById('{html_id}'));
    chart.draw(data, options);
  }}
</script>
'''.format(
                data = self._serialize_data(),
                html_id = self.html_id,
                chart_class = self.name,
                options = u',\n'.join(u'{0}: "{1}"'.format(keyword, value) for keyword, value in self.options.items()),
                package = self.package
                ))
    def render_html(self):
        return mark_safe(u'''<div id="{0}" class="gchart"></div>'''.format(self.html_id))

    def _serialize_data(self):
        from gviz_api import DataTable

        table = DataTable(self.schema)
        table.LoadData(self.data)
        return table.ToJSon()
    
class GoogleChartWrapper(object):
    u'''A thin wrapper for Google charts.'''

    def __getattr__(self, name):
        package_name = name
        class PackageWrapper(object):
            def __getattr__(self, name):
                if name.endswith('Factory'):
                    chart_name = name[:-len('Factory')]
                else:
                    raise AttributeError("'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name))
                
                def chart_factory(**options):
                    return type(name, (GoogleChart,), {'class_options': options, 'package': package_name, 'name': chart_name})
                chart_factory.__name__ = name
                
                return chart_factory
        return PackageWrapper()

# CONSIDER: Maybe this should be named differently?
gchart = GoogleChartWrapper()

# CONSIDER: Maybe this should be a class method for Chart?
def rearrange_columns(*column_indices):
    u'''Returns class decorator that rearranges presence and ordering of schema's and data's items.'''

    def columns_decorator(ChartClass):
        class DecoratedChart(ChartClass):
            def __init__(self, schema, data, **kwargs):
                rearranged_schema = [schema[j] for j in column_indices]
                rearranged_data = [[row[j] for j in column_indices] for row in data]
                return super(DecoratedChart, self).__init__(rearranged_schema, rearranged_data, **kwargs)
        DecoratedChart.__name__ = ChartClass.__name__
        return DecoratedChart
    return columns_decorator
