import os
import yaml
from visualizations.layout import VisualizationLayout

# Read and start visualization server with yaml config
with open(os.getenv("CONFIG_PATH"), 'r') as stream:
    config_data = yaml.safe_load(stream)
for vis_config in config_data['visualizations']:
    VisualizationLayout(**vis_config[list(vis_config.keys())[0]]).add_to_curdoc()
