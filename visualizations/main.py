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
vis_config = config_data['visualizations'][0][list(config_data['visualizations'][0].keys())[0]]

# Read last updated date and add to config (if it doesn't exist, will not display it)
last_updated_path = os.getenv("LAST_UPDATED_PATH")
logconfig.log.info(f"Reading last updated time from {last_updated_path}")
last_updated_time = None
if os.path.exists(last_updated_path):
    with open(last_updated_path, 'r') as stream:
        last_updated_time = stream.readline()
logconfig.log.info(f"Last updated: {last_updated_time}")
vis_config["last_updated_time"] = last_updated_time

# Render!
layout = VisualizationLayout(**vis_config)
curdoc().title = config_data.get("page_title", "Green Zone Visualizations")
layout.render()
