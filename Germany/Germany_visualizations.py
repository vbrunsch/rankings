from visualizations.layout import VisualizationLayout

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
viz = VisualizationLayout(input_path="germany.pkl",
                          labels=labels,
                          descriptions=descriptions,
                          lower_bounds=lower_bounds,
                          colors=colors,
                          title="COVID Phases in Germany")
viz.add_to_curdoc()

#
# Visualization Two
#
# Green Zone: 0 cases in 14 days, sort by COVID-Free days
# Phase 1: <10 cases per 100k
# Phase 2: >=10 cases per 100k
#
labels = ["Green Zone", "Phase 1", "Phase 2"]
descriptions = ["0 cases in 14 days", "<10 cases per 100,000 people", ">=10 cases per 100,000 people"]
lower_bounds = [0, 1, 10]
colors = ["#25773b", "#f9cc3c", "#ef3e24"]
viz_incidence = VisualizationLayout(input_path="germany.pkl",
                                    labels=labels,
                                    descriptions=descriptions,
                                    lower_bounds=lower_bounds,
                                    colors=colors,
                                    title="COVID Phases in Germany (Cases per 100,000)",
                                    incidence_unit="case",
                                    incidence_plural_unit="cases",
                                    primary_incidence_key="Cases per 100k (Last 7 Days)",
                                    secondary_incidence_key="Cases per 100k (Last 14 Days)",
                                    primary_incidence_tooltip="Cases per 100,000 (Last 7 Days)",
                                    secondary_incidence_tooltip="Cases per 100,000 (Last 14 Days)",
                                    calc_with_secondary_incidence=[True, False, False],
                                    legend_width=325,
                                    legend_height=150)
viz_incidence.add_to_curdoc()
