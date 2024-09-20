# Open-Imx:Icons.API

This FastAPI app allows for the retrieval of icons based on a specified IMX path and associated properties. It utilizes the [Open-Imx:Icons](https://github.com/open-imx/ImxIcons) Python library, which offers an efficient solution for icon lookup. For detailed information on icon generation, please refer to the library documentation.

**Source Code**: [https://github.com/open-imx/ImxIconsApi](https://github.com/open-imx/ImxIconsApi)

This is a personal project and is provided as-is, without any guarantees regarding functionality, accuracy, or usage.

## Quick Start

This is the initial version and serves as a demo.  
You can explore and use it by visiting: [imx-icons-api.azurewebsites.net](https://imx-icons-api.azurewebsites.net/).

### Get IMX Paths

The API provides an endpoint to view available paths. Each IMX object has a unique path. For standard objects, the path corresponds to the object’s name, while for objects with children, the path is structured as `parent.object`, ensuring uniqueness.

### Get Icon Mapping

Not all objects or property combinations generate an icon, as icon path properties and combinations may vary between IMX versions. Use the mapping endpoint to view available combinations.

### Get Icon

Two endpoints are available: one to retrieve the SVG file and another to obtain the SVG as text.
- If the `qgis` parameter is set to `true`, the SVG file will include the `qgis` attribute.

### Reporting Issues

If you encounter any issues specifically related to the API, such as endpoint functionality, request handling, or performance, please report them in the [ImxIconsApi repository](https://github.com/open-imx/ImxIconsApi/issues).

For issues related to icon generation, such as missing icons, incorrect mappings, or discrepancies in IMX path handling, please report them directly to the [Open-Imx:Icons library](https://github.com/open-imx/ImxIcons/issues) repository.

## Service vs Self-Hosting

The service currently runs on a free plan, meaning requests are rate-limited globally. If demand increases, upgrading to a SaaS model could be considered.

Since the project is open-source, you can also self-host the service at no cost.

## Versioning

We use `bumpversion` to manage versioning, following the semantic versioning strategy.

### New Library Releases

When a new version of the Open-Imx:Icons library is released, it triggers a dispatch event. This event starts the pipeline to build and deploy a new API release, updating only the build number without changing the version. This process ensures that the API stays updated with changes to the library without significant overhead.

## Contributing

Contributions are welcome! For more details on contributing, refer to the [contribution guidelines](CONTRIBUTING.md) for this project.
