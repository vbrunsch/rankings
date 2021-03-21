# Green-zone Rankings
Green-zone Rankings — EndCoronavirus.org

Created by: Trevor Winstral and Vincent Brunsch, see source code here
https://github.com/TrevorWinstral/County_Ranking
Generates the rankings at https://www.endcoronavirus.org/green-zone-rankings
## Visualizations
Visualizations, integration, and deployment pipeline created by: Jason Li
* Pipeline is available for monitoring at concourse.nocovid.group
* Visualizations are available at nocovid.group/{region name}
### Adding new regions
1. Modify a country's ranking.py to generate a .pkl with the required and/or optional columns.
    * Required columns are region name, category, time safe, and primary incidence
    * Optional columns are postcode, secondary incidence, and percent change
    * The .pkl file should be saved to the visualizations/pickles folder
2. Create a .yml file in the visualizations/config folder containing the required configuration.
    * Documentation of all configuration options is available in visualizations/layout.py
        * Make sure the required configuration options are set!
    * You can refer to the sample.yml or germany.yml for an example
    * Must be .yml, not .yaml
3. Add the region to the regions section of ci/helm/visualizations/values.yaml
    * It should be typed exactly the same as the filename of the region's .yml config file, just without the .yml extension (e.g. germany.yml -> germany)
### Deployment with Docker
* To deploy using the Dockerfile, override the following environment variables:
  * REGION (e.g. REGION=germany)
    * Set this equal to the filename of the .yml (excluding the .yml extension)
  * BOKEH_ALLOW_WS_ORIGIN (e.g. BOKEH_ALLOW_WS_ORIGIN=localhost,endcoronavirus.org)
    * This should contain all the origins that will be used to access the server. Everything not listed will be blocked.
    * Multiple origins can be added, separated by comma
  * Optional, but allows for SSL termination:
      * BOKEH_SSL_CERTFILE (path to public cert, e.g. BOKEH_SSL_CERTFILE=cert.pem)
      * BOKEH_SSL_KEYFILE (path to private key, e.g. BOKEH_KEY_CERTFILE=key.pem)
### Example
![visualization example](https://raw.githubusercontent.com/vbrunsch/rankings/main/visualization_img.png)
