import pandas as pd
from bokeh.layouts import column, row
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, AutocompleteInput, Button, Text, HoverTool, MultiLine, Legend, LegendItem


class VisualizationLayout:
    """ VisualizationLayout generates visualizations of the COVID ranking data. It should be served with Bokeh's
        serve command.

    Data should be input as a .pkl file. It should have the columns corresponding to the keys listed in the constants.
    The parameter defaults are set in accordance with ECV's use case. Adjust as necessary.
    :param input_path is where the .pkl file is located
    :param labels are the phases' labels. the first element is always the "Green Zone" and is sorted in descending order
           with elements in time_safe_key.
    :param descriptions are used to display the legend
    :param lower_bounds are the lower bounds, inclusive, of the phases. an example is [0, 1, 20], where phase 1 only
           includes 0 incidence (>= 0 and < 1, phase 2 includes incidence >= 1 and < 20, etc.
           if you do not want a "Green Zone," you should set the first element of the labels to a dummy label and the
           first element of lower_bounds to an arbitrarily high number.
    :param colors are the colors of each phase
    :param title is the title of the visualization

    :param width is the plot width, in pixels (default: 750)
    :param height is the plot height, in pixels (default: 800)
    :param width is the legend and input area width, in pixels (default: 300)
    :param height is the legend height, in pixels (default: 200)
    :param x_range represents the range of x values represented in the plot. (default: (-3, 5))
           for reference, the box's width is 1 and it spans x = [0, 1]
    :param y_range represents the range of y values represented in the plot. (default: (-0.1, 1.1))
           for reference, the box's height is 1 and it spans y = [0, 1]
    :param min_space_x is the minimum horizontal space in between each "branched" line (default: 0.075)
    :param min_space_y is the minimum vertical space in between each county's text and line elements (default: 0.033)
    :param num_top_regions is the number of regions that appear per phase (excluding searched regions) (default = 6)

    :param region_type should describe the granularity of the input data. (default: "Region")
           for example, input "City" for city-level data. this is used in the hover tooltips.
    :param time_safe_unit should describe the unit used to count the time a region has been "safe" (e.g. day)
    :param time_safe_plural_unit should be same as time_safe_unit but plural (e.g. days)
    :param incidence_unit should describe the unit used to represent incidence (e.g. case, case per 100,000)
    :param incidence_plural_unit should be same as incidence_unit but plural (e.g. cases, cases per 100,000)

    :param region_key is used to access a region's name
    :param primary_incidence_key is used to access the disease incidence. incidence can be in case numbers, etc.
           the data stored under the primary key is used to calculate the phase categorizations, sorting, etc.
    :param secondary_incidence_key is used to access the disease incidence. incidence can be in case numbers, etc.
           the data stored under the secondary key is used just for display, unless you override it
    :param time_safe_key is used to access the number of days a region has been disease-free
    :param postcode_key is used to access a region's postcode
    :param percent_change_key is used to access the calculated percent change in incidence over a given timeframe
    :param calc_with_secondary_incidence is used as an override, with index i = True forcing the calculations for the
           category at index i to be done using the secondary incidence data. (default: [False] * number of categories)

    :param legend_title is the title displayed above the legend
    :param searchbar_placeholder is used as the placeholder for the region search bar
    :param reset_button_text is used as the text for the reset button
    :param region_name_tooltip is used to display the region name in the hovering tooltip
    :param category_tooltip is used to display the region's category in the hovering tooltip
    :param region_code_tooltip is used to display the region's code in the hovering tooltip
    :param time_safe_tooltip is used to display the time a region has been "safe" in the hovering tooltip
    :param primary_incidence_tooltip= is used to display incidence within one timeframe in the hovering tooltip
    :param secondary_incidence_tooltip= is used to display incidence within another timeframe in the hovering tooltip
    :param percent_change_tooltip= is used to display percent change between the timeframes in the hovering tooltip
    """

    def __init__(self,
                 # metadata
                 input_path, labels, descriptions, lower_bounds, colors, title,

                 # sizing stuff
                 width=700, height=800,
                 legend_width=300, legend_height=200,
                 x_range=(-3, 5), y_range=(-0.1, 1.1),
                 min_space_x=0.075, min_space_y=0.033,
                 num_top_regions=6,

                 # keys
                 region_key="District/County Town",
                 primary_incidence_key="New Cases in Last 14 Days",
                 secondary_incidence_key="Last 7 Days",
                 time_safe_key="COVID-Free Days",
                 postcode_key="Postcode",
                 percent_change_key="Pct Change",

                 # units
                 region_type="Region",
                 time_safe_unit="day",
                 time_safe_plural_unit="days",
                 incidence_unit="case",
                 incidence_plural_unit="cases",
                 calc_with_secondary_incidence=None,

                 # strings
                 legend_title="Legend",
                 searchbar_placeholder="Search for a region...",
                 reset_button_text="Reset",
                 region_name_tooltip="Region Name",
                 category_tooltip="Category",
                 region_code_tooltip="Region Code",
                 time_safe_tooltip="COVID-Free Days",
                 primary_incidence_tooltip="New Cases in Last 14 Days",
                 secondary_incidence_tooltip="New Cases in Last 7 Days",
                 percent_change_tooltip="Weekly Percent Change"
                 ):

        # Initialize metadata-like input data
        self.input_table = pd.read_pickle(input_path)
        self.labels = labels
        self.descriptions = descriptions
        self.lower_bounds_adj = lower_bounds
        self.lower_bounds_adj.append(self.input_table[primary_incidence_key].max())
        self.colors = colors
        self.title = title
        self.region_type = region_type
        self.num_categories = len(labels)

        # Initialize sizing stuff
        self.width = width
        self.height = height
        self.legend_width = legend_width
        self.legend_height = legend_height
        self.x_range = x_range
        self.y_range = y_range
        self.min_space_x = min_space_x
        self.min_space_y = min_space_y
        self.num_top_regions = num_top_regions

        # Initialize keys
        self.region_key = region_key
        self.primary_incidence_key = primary_incidence_key
        self.secondary_incidence_key = secondary_incidence_key
        self.time_safe_key = time_safe_key
        self.postcode_key = postcode_key
        self.percent_change_key = percent_change_key

        # Initialize unit stuff
        self.region_type = region_type
        self.time_safe_unit = time_safe_unit
        self.time_safe_plural_unit = time_safe_plural_unit
        self.incidence_unit = incidence_unit
        self.incidence_plural_unit = incidence_plural_unit
        self.calc_with_secondary_incidence = (calc_with_secondary_incidence if calc_with_secondary_incidence is not None
                                              else [False] * self.num_categories)

        # Initialize tooltip strings
        self.legend_title = legend_title
        self.searchbar_placeholder = searchbar_placeholder
        self.reset_button_text = reset_button_text
        self.region_name_tooltip = region_name_tooltip
        self.category_tooltip = category_tooltip
        self.region_code_tooltip = region_code_tooltip
        self.time_safe_tooltip = time_safe_tooltip
        self.primary_incidence_tooltip = primary_incidence_tooltip
        self.secondary_incidence_tooltip = secondary_incidence_tooltip
        self.percent_change_tooltip = percent_change_tooltip

        # Initialize class members which will store calculation data
        self.ratios = []
        self.categorized_entries = []
        self.top_regions = [pd.DataFrame()] * self.num_categories
        self.sort_criterias = []
        self.criteria_units = []
        self.last_searched = ""

        # Initialize data sources used for plotting
        self.source = ColumnDataSource()
        self.searched_source = ColumnDataSource()

        self.__categorize_entries__()
        self.__calculate_ratios__()
        self.__init_sorting_criteria__()
        self.__build_top_regions__()

    def __categorize_entries__(self):
        for i in range(self.num_categories):
            incidence_key = self.__get_incidence_key__(i)
            self.categorized_entries.append(
                self.input_table.loc[
                    (self.input_table[incidence_key] >=
                     self.lower_bounds_adj[i]) &
                    (self.input_table[incidence_key] <
                     self.lower_bounds_adj[i + 1])])

    def __calculate_ratios__(self):
        num_entries = len(self.input_table)
        for i in range(self.num_categories):
            self.ratios.append(len(self.categorized_entries[i]) / num_entries)

    def __init_sorting_criteria__(self):
        for i in range(self.num_categories):
            if i == 0:
                self.sort_criterias.append(self.time_safe_key)
                self.criteria_units.append(self.time_safe_unit)
            else:
                self.sort_criterias.append(self.__get_incidence_key__(i))
                self.criteria_units.append(self.incidence_unit)

    def __get_incidence_key__(self, category_index):
        if self.calc_with_secondary_incidence[category_index]:
            return self.secondary_incidence_key
        return self.primary_incidence_key

    def __build_top_regions__(self):
        for i in range(self.num_categories):
            if self.sort_criterias[i] == self.time_safe_key:
                self.top_regions[i] = self.categorized_entries[i].nlargest(
                    self.num_top_regions, self.sort_criterias[i])
            else:
                self.top_regions[i] = self.categorized_entries[i].nsmallest(
                    self.num_top_regions, self.sort_criterias[i])

    def __add_searched_region__(self, query):
        # Set last searched
        self.last_searched = query
        # Add searched region to appropriate top_regions element, then sort
        search_type = self.postcode_key if query.isnumeric() else self.region_key
        for i in range(self.num_categories):
            searched_region_entry = \
                self.categorized_entries[i][self.categorized_entries[i][search_type] == query]
            if (query != "") and \
                    (len(searched_region_entry) != 0) and \
                    (len(self.top_regions[i][self.top_regions[i][search_type] == query]) == 0):
                self.top_regions[i] = self.top_regions[i].append(searched_region_entry)
                self.top_regions[i] = self.top_regions[i]. \
                    sort_values(self.sort_criterias[i],
                                ascending=(self.sort_criterias[i] == self.__get_incidence_key__(i)))
                break

    @staticmethod
    def __new_plot_data_map__():
        return {"line_x_points": [],
                "line_y_points": [],
                "line_color": [],
                "text_x": [],
                "text_y": [],
                "text": [],
                "region_name": [],
                "category": [],
                "postcode": [],
                "time_safe": [],
                "primary_incidence": [],
                "secondary_incidence": [],
                "percent_change": []}

    def __build_plot_data__(self):
        box_top_y = 1
        last_text_y = float('inf')
        plot_data = self.__new_plot_data_map__()
        searched_plot_data = self.__new_plot_data_map__()
        for i in range(len(self.ratios)):
            curr_top = self.top_regions[i]
            sort_criteria = self.sort_criterias[i]
            criteria_unit = self.criteria_units[i]

            box_size = self.ratios[i]
            if box_size == 0:
                continue

            # Iterate through each region, calculate their plot positions with padding
            top_region_datum = curr_top[sort_criteria].max()
            bot_region_datum = curr_top[sort_criteria].min()
            padding = box_size * 0.1
            for region, datum, postcode, time_safe, primary_incidence, secondary_incidence, percent_change in zip(
                    curr_top[self.region_key],
                    curr_top[sort_criteria],
                    curr_top[self.postcode_key],
                    curr_top[self.time_safe_key],
                    curr_top[self.primary_incidence_key],
                    curr_top[self.secondary_incidence_key],
                    curr_top[self.percent_change_key]):
                line_y_relative = ((datum - bot_region_datum) / (top_region_datum - bot_region_datum)) \
                    if top_region_datum != bot_region_datum else 0.5
                line_y = box_top_y - ((box_size - (padding * 2)) * line_y_relative) - padding

                # Calculate necessary vertical adjustments to line and text
                text_y = line_y
                if last_text_y - line_y < self.min_space_y:
                    text_y = last_text_y - self.min_space_y
                line_x_points = [1, 1.25, 1.25, 1.5]
                line_y_points = [line_y, line_y, text_y, text_y]
                last_text_y = text_y

                # Store plot data for post-processing
                plot_data["line_x_points"].append(line_x_points)
                plot_data["line_y_points"].append(line_y_points)
                plot_data["line_color"].append(self.colors[i])
                plot_data["text_x"].append(line_x_points[3])
                plot_data["text_y"].append(text_y)
                plot_data["text"].append([f"{region}: {datum} {self.__determine_unit__(criteria_unit, datum)}"])
                plot_data["region_name"].append(region)
                plot_data["category"].append(self.labels[i])
                plot_data["postcode"].append(postcode)
                plot_data["time_safe"].append(time_safe)
                plot_data["primary_incidence"].append(primary_incidence)
                plot_data["secondary_incidence"].append(secondary_incidence)
                plot_data["percent_change"].append('{:.1%}'.format(percent_change / 100))

            box_top_y -= box_size

        # Postprocessing to adjust lines horizontally, ensuring no overlapping branches
        self.__adjust_branches__(data=plot_data, direction="right")

        # Isolate searched region
        for i in reversed(range(len(plot_data["postcode"]))):
            if (plot_data["region_name"][i] == self.last_searched) or \
                    (plot_data["postcode"][i] == self.last_searched):
                for key in plot_data:
                    searched_plot_data[key] = [plot_data[key][i]]
                    del plot_data[key][i]
                break

        self.source.data = plot_data
        self.searched_source.data = searched_plot_data

    def __determine_unit__(self, unit, quantity):
        if quantity == 1:
            return unit
        if unit == self.time_safe_unit:
            return self.time_safe_plural_unit
        return self.incidence_plural_unit

    def __build_layout__(self):
        # Initialize plot
        plot = figure(
            title=self.title,
            plot_width=self.width,
            plot_height=self.height,
            x_range=self.x_range,
            y_range=self.y_range,
            toolbar_location=None,
            align="center"
        )
        plot.xaxis.visible = False
        plot.yaxis.visible = False
        plot.grid.visible = False

        self.__draw_phase_boxes__(plot)
        self.__draw_glyphs__(plot)
        input_layout = self.__build_input_layout__()
        legend = self.__build_legend__()

        return row(plot, column(legend, input_layout))

    def __draw_phase_boxes__(self, plot):
        box_top_y = 1
        box_data = self.__new_plot_data_map__()
        box_data["box_top_y"] = []
        last_text_y = 99999
        for i in range(self.num_categories):
            box_size = self.ratios[i]
            box_middle = box_top_y - (box_size / 2)
            if box_size == 0:
                # add dummy entries, since there should be no box, line, nor text rendered for this category
                for _, v in box_data.items():
                    v.append(None)
                continue

            # add data for post-processing
            box_data["box_top_y"].append(box_top_y)
            box_data["text_y"].append(box_middle)
            box_data["text"].append([f"{self.labels[i]}\n{'{:.1%}'.format(box_size)}"])
            if box_size >= 0.066:
                box_data["text_x"].append(0)
                box_data["line_x_points"].append(None)
                box_data["line_y_points"].append(None)
            else:
                # override if last label will overlap with the default text location (box's middle)
                if last_text_y - box_middle < self.min_space_y:
                    box_data["text_y"][i] = last_text_y - (self.min_space_y * 2.25)

                box_data["text_x"].append(-1.5)
                box_data["line_x_points"].append([-1.475, -1.25, -1.25, -1])
                box_data["line_y_points"].append([box_data["text_y"][i],
                                                  box_data["text_y"][i],
                                                  box_middle,
                                                  box_middle])
            last_text_y = box_data["text_y"][i]
            box_top_y -= box_size

        # Post-process to ensure labels and branches don't overlap
        self.__adjust_branches__(box_data, "left")

        # Render boxes and labels
        for i in range(len(box_data["box_top_y"])):
            # skip dummy entries
            if box_data["box_top_y"][i] is None:
                continue

            # if there is a line, that means the label is offset
            is_offset = box_data["line_x_points"][i] is not None

            # Render text, the y_offset ensures that the line points to text and not the empty space between the text
            plot.vbar(0, 2, box_data["box_top_y"][i], fill_color=self.colors[i], line_color="#000000")
            plot.text(x=box_data["text_x"][i], y=box_data["text_y"][i],
                      text=box_data["text"][i],
                      text_baseline="middle",
                      y_offset=(10 if is_offset else 0),
                      text_align=("right" if is_offset else "center"))
            plot.line(x=box_data["line_x_points"][i], y=box_data["line_y_points"][i], color=self.colors[i])

    def __draw_glyphs__(self, plot):
        # Add lines
        line = MultiLine(xs="line_x_points", ys="line_y_points", line_color="line_color")
        plot.add_glyph(self.source, line)
        plot.add_glyph(self.searched_source, line)

        # Add text and hover functionality
        text = Text(x="text_x", y="text_y", text="text", text_baseline="middle", text_font_style="normal")
        text_renderer = plot.add_glyph(self.source, text)
        searched_text = Text(x="text_x", y="text_y", text="text", text_baseline="middle", text_font_style="bold")
        searched_text_renderer = plot.add_glyph(self.searched_source, searched_text)
        tooltips = [(f"{self.region_name_tooltip}", "@{region_name}"),
                    (f"{self.category_tooltip}", "@{category}"),
                    (f"{self.region_code_tooltip}", "@{postcode}"),
                    (f"{self.time_safe_tooltip}", "@{time_safe}"),
                    (f"{self.primary_incidence_tooltip}", "@{primary_incidence}"),
                    (f"{self.secondary_incidence_tooltip}", "@{secondary_incidence}"),
                    (f"{self.percent_change_tooltip}", "@{percent_change}")]
        text_hover = HoverTool(renderers=[text_renderer, searched_text_renderer], tooltips=tooltips,
                               anchor="bottom_center", attachment="above", point_policy="follow_mouse")
        plot.add_tools(text_hover)

    def __build_input_layout__(self):
        # Callbacks for the searchbar and reset button
        def handle_search(attr, old, new):
            self.__add_searched_region__(new)
            self.__build_plot_data__()

        def handle_reset(event):
            text_input.value = ""
            self.last_searched = ""
            self.__build_top_regions__()
            self.__build_plot_data__()

        # Builds input with autocompletion
        completions = []
        completions.extend(self.input_table[self.region_key].tolist())
        completions.extend(self.input_table[self.input_table[self.postcode_key] != 0][self.postcode_key].tolist())
        text_input = AutocompleteInput(completions=completions, min_characters=5, case_sensitive=False,
                                       placeholder=self.searchbar_placeholder)
        text_input.on_change('value', handle_search)

        # Reset button
        reset_button = Button(label=self.reset_button_text)
        reset_button.on_click(handle_reset)

        return column(reset_button, text_input, sizing_mode="scale_width")

    def __adjust_branches__(self, data, direction):
        # Adjusts "branches" horizontally to ensure no overlaps
        consecutive_branches = 0
        for i in reversed(range(len(data["line_x_points"]))):
            # Skip if no line exists (this occurs when drawing the phase boxes)
            if data["line_x_points"][i] is None:
                continue

            # If branched or if prior line was branched, adjust according to direction
            is_branched = data["line_y_points"][i][1] != data["line_y_points"][i][2]
            if is_branched | consecutive_branches != 0:
                adjustment = self.min_space_x * consecutive_branches
                if direction == "left":
                    adjustment *= -1
                    data["line_x_points"][i][0] += adjustment
                else:
                    data["line_x_points"][i][3] += adjustment
                data["line_x_points"][i][1] += adjustment
                data["line_x_points"][i][2] += adjustment
                data["text_x"][i] += adjustment
                consecutive_branches += 1

            if not is_branched:
                consecutive_branches = 0

    def __build_legend__(self):
        legend = Legend()
        legend_items = []
        for i in range(self.num_categories):
            legend_items.append(
                LegendItem(
                    label=f"{self.labels[i]}: {self.descriptions[i]}"
                )
            )
        legend.items = legend_items
        legend.location = "center"
        legend_plot = figure(
            title=self.legend_title,
            plot_width=self.legend_width,
            plot_height=self.legend_height,
            toolbar_location=None,
            align="center"
        )
        legend_plot.xaxis.visible = False
        legend_plot.yaxis.visible = False
        legend_plot.grid.visible = False
        legend_plot.add_layout(legend)
        return legend_plot

    def add_to_curdoc(self):
        """ add_to_curdoc displays the visualization on Bokeh's current document.
        :return: nothing
        """
        self.__build_plot_data__()
        layout = self.__build_layout__()
        curdoc().add_root(layout)
