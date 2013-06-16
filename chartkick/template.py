from __future__ import absolute_import


CHART_HTML = """
<div id="{id}" style="height: {height}; text-align: center; color: #999;
                      line-height: {height}; font-size: 14px;
                      font-family: Lucida Grande, Lucida Sans Unicode,
                      Verdana, Arial, Helvetica, sans-serif;">
    Loading...
</div>
<script>
//<![CDATA[
new Chartkick.{name}(document.getElementById("{id}"), {data}, {options});
//]]>
</script>
"""
