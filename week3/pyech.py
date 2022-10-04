
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.globals import ChartType, SymbolType

geo = Geo(init_opts=opts.InitOpts(width="600px",height="400px",bg_color="white"))
geo.add_schema(maptype='北京')

