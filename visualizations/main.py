import os
import yaml
from bokeh.util import logconfig
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import Spacer

from visualizations.layout import VisualizationLayout

# Read and start visualization server with yaml config
config_file_path = os.getenv("CONFIG_PATH")
logconfig.log.info(f"Using config file at {config_file_path}")
with open(config_file_path, 'r') as stream:
    config_data = yaml.safe_load(stream)

# Render with horizontal spacers on the sides and vertical spacers in between visualizations
horizontal_margin = config_data.get("horizontal_margin", 25)
between_margin = config_data.get("between_margin", 25)
for i, vis_config in enumerate(config_data['visualizations']):
    curdoc().add_root(
        row(Spacer(width=horizontal_margin),
            VisualizationLayout(**vis_config[list(vis_config.keys())[0]]).generate(),
            Spacer(width=horizontal_margin)))

    if i < (len(config_data['visualizations']) - 1):
        curdoc().add_root(Spacer(height=between_margin))

curdoc().title = config_data.get("page_title", "Green Zone Visualizations")
