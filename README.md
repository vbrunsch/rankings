# Green-zone Rankings
Green-zone Rankings — EndCoronavirus.org

Created by: Trevor Winstral and Vincent Brunsch, see source code here
https://github.com/TrevorWinstral/County_Ranking
Generates the rankings at https://www.endcoronavirus.org/green-zone-rankings
# Green-zone Visualizations
Visualizations, integration, and deployment pipeline created by Jason Li
* All changes pushed to this repository are automatically deployed
* Pipeline is available for monitoring at https://concourse.nocovid.group
* Visualizations are served at https://nocovid.group/{region}
### Adding new regions
1. Modify a region's ranking.py to generate a .pkl with the required and/or optional columns.
    * Required columns are region name, category, time safe, and primary incidence (e.g. cases in 7 days)
    * Optional columns are postcode, secondary incidence (e.g. cases per 100k in 14 days), and percent change (use if primary and secondary incidence are of the same unit and measured over different periods of time)
    * The .pkl file should be saved to the visualizations/pickles folder
2. Create a .yml file in the visualizations/config folder containing the required configuration.
    * Documentation of all configuration options is available in [visualizations/layout.py](https://github.com/vbrunsch/rankings/blob/6eba3b322aaf5939d9c0ae9c02862b57094059fe/visualizations/layout.py#L49)
        * Make sure the required configuration options are set!
    * You can refer to the sample.yml or germany.yml for an example
    * Must be .yml, not .yaml
3. Add the region to the regions section of ci/helm/visualizations/values.yaml
    * It should be typed exactly the same as the filename of the region's .yml config file, just without the .yml extension (e.g. germany.yml -> germany)
    * Additionally, you should add any websites you will embed the visualization on in the allowedOrigins section
4. After the pipeline finishes running, the visualization should be available at https://nocovid.group/{region}.
### Modifying or translating regions
* To modify a region's visualization, you just need to modify the region's config file (or the .pkl generation) and changes will automatically be applied
* To translate a region, use the label and string configuration options. Consult the saxony.yml config file for reference.
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
### Kubernetes Deployment
* All deployments should be handled by the CI/CD pipeline. To set up the pipeline, see [here](https://github.com/aochen-jli/rankings-cicd).
### Example
![visualization example](https://raw.githubusercontent.com/vbrunsch/rankings/main/visualization_img.png)
