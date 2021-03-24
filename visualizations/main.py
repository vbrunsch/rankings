import os
import yaml
from bokeh.util import logconfig
from bokeh.io import curdoc, show

from visualizations.layout import VisualizationLayout

# Read yaml config
config_file_path = os.getenv("CONFIG_PATH")
logconfig.log.info(f"Using config file at {config_file_path}")
with open(config_file_path, 'r') as stream:
    config_data = yaml.safe_load(stream)
vis_config = config_data['visualizations'][0]

# Render!
layout = VisualizationLayout(**vis_config[list(vis_config.keys())[0]])
curdoc().title = config_data.get("page_title", "Green Zone Visualizations")
curdoc().add_root(layout.get_plot())
curdoc().add_root(layout.get_searchbar())
curdoc().add_root(layout.get_reset_button())
