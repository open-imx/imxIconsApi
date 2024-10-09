# Open-Imx:Icons.API

This FastAPI app enables the retrieval of icons based on a specified IMX path and a set of associated properties. 
It is utilizing the <a href="https://github.com/open-imx/ImxIcons" target="_blank">Open-Imx:Icons</a> python library that provide a efficient solution for icon lookup.
For more information about the icons generation, refer to the library documentation.

**Source Code**: <a href="https://github.com/open-imx/ImxIconsApi" target="_blank">https://github.com/open-imx/imxIconsApi</a>

This is a personal project and therefore no responsibility for the functionality, accuracy, or usage.

## Quick Start
go to: <a href="https://imx-icons-api.azurewebsites.net/" target="_blank">https://imx-icons-api.azurewebsites.net/</a>

### Get imx paths
We provide an endpoint to view the available paths. Each IMX object has a path, for standard objects the path corresponds to the IMX object's name. For objects with children the path is constructed as `parent.object`, ensuring uniqueness.

### Get icon mapping
Not all objects or property combinations will generate an icon, as the icon path properties and their combinations can vary between IMX versions. To see the specific combinations available, use the mapping endpoint.

### Get icon
There are two endpoints available: one for retrieving the SVG file and another for obtaining the SVG as text. 
- When `qgis` is set to `true`, the `qgis` parameter will be included in the svg file.

## Service vs self hosting
The service is currently running on a free app plan, which means requests are globally rate-limited. 
If the service gains sufficient usage, there is potential for an upgrade to a SaaS app.

Additionally, it is fully open-source, allowing you to self-host and use it at no cost. Currently, this is the first version and is intended as a demo.

### Backlog and Roadmap
<a href="https://github.com/orgs/open-imx/projects/4/" target="_blank">https://github.com/orgs/open-imx/projects/4/</a>

## Versioning
We use bumpversion for managing versions, following the semantic versioning strategy. 

### New library releases
When the Open-Imx:Icons library releases a new version, it triggers a dispatch event. This event initiates the pipeline to build and deploy a new release of the API, updating only the build number without changing the version.
This approach allows us to stay updated with changes in the library without adding significant overhead.

## Contributing
Contributions welcome! For more information on the design of the library, see [contribution guidelines for this project](CONTRIBUTING.md).
