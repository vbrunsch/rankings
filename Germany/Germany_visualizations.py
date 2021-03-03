from visualizations.server import VisualizationServer

#
# Visualization One
#
# Green Zone: 0 cases in 14 days, sort by COVID-Free days
# Phase 4: <20 new cases in 14 days
# Phase 3: <200 new cases in 14 days
# Phase 2: <1000 new cases in 14 days
# Phase 1: >1000 new cases in 14 days
#
labels = ["Green Zone", "Phase 4", "Phase 3", "Phase 2", "Phase 1"]
descriptions = ["0 cases in 14 days", "<20 new cases in 14 days", "<200 new cases in 14 days",
                "<1000 new cases in 14 days", ">1000 new cases in 14 days"]
lower_bounds = [0, 1, 20, 200, 1000]
colors = ["#25773b", "#8ac541", "#f9cc3c", "#f8961d", "#ef3e24"]
server = VisualizationServer(input_path="germany.pkl",
                             labels=labels,
                             descriptions=descriptions,
                             lower_bounds=lower_bounds,
                             colors=colors,
                             title="COVID Phases in Germany")
server.start()

