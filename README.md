# Green-zone Rankings
Green-zone Rankings — EndCoronavirus.org

Created by: Trevor Winstral and Vincent Brunsch, see source code here
https://github.com/TrevorWinstral/County_Ranking
Generates the rankings at https://www.endcoronavirus.org/green-zone-rankings
## Visualizations
Visualizations and integration created by: Jason Li
### Usage
* To create a visualization, write a .yml file containing the required configuration.
    * Documentation is available in visualizations/layout.py
    * Any country's ranking.py should generate a .pkl, and this file's path should be included in the .yml
    * Modify the units and strings configuration variables for translation
* If a country's ranking.py is not yet integrated, please see the Germany_ranking.py git blame for a reference point
* To deploy using Docker, override the following environment variables:
  * REGION (e.g. REGION=germany)
    * Set this equal to the filename of the .yml (excluding the .yml extension)
  * BOKEH_ALLOW_WS_ORIGIN (e.g. BOKEH_ALLOW_WS_ORIGIN=localhost:5006,localhost:8080)
    * This should contain all the origins that will be used to access the server. Everything not listed will be blocked.,
    * Multiple origins can be added, separated by comma
  * BOKEH_SSL_CERTFILE (e.g. BOKEH_ALLOW_WS_ORIGIN=localhost:5006,localhost:8080)
    * This should point to a CA certfile and will enable HTTPS
### Example
![visualization example](https://raw.githubusercontent.com/aochen-jli/rankings/main/visualization_img.png)