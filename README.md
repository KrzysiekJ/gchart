gchart
======

A flexible Google Chart API wrapper.

Example
-------

```python
from gchart import gchart
chart_class = gchart.corechart.PieChartFactory(some_piechart_option='foo')
chart = chart_class(
    [("name", "string"), ("no. of donuts eaten", "number")],
    [("Joe", 3), ("Bob", 5), ("Helen", 9)],
    another_piechart_option = "bar"
)
```

The you can call `chart.initialize_html()` and `chart.render_html()`...

Note that because `corechart` and `PieChartFactory` are created dynamically, you cannot write:

```python
from gchart.gchart.corechart import PieChartFactory
```

Instead, you may do something like:

```python
import gchart
PieChartFactory = gchart.gchart.corechart.PieChartFactory
```