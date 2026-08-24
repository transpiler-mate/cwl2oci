# CWL 2 OCI

`cwl2oci` is a [Transpiler-Mate API](https://github.com/sim13pods/transpiler-mate-api)
plugin that converts normalized CWL software metadata and one selected CWL
process into an [OCI image annotation](https://specs.opencontainers.org/image-spec/annotations/)
map.

It writes an `annotations.json` file shaped like this:

```json
{
  "$manifest": {
    "org.opencontainers.image.title": "Hello workflow",
    "org.opencontainers.image.version": "1.0.0",
    "org.cwl.entrypoint": "main",
    "org.cwl.type": "Workflow"
  }
}
```

The plugin generates metadata only. It does not build or publish an OCI image,
and it does not provide a standalone CLI.

## Choose your path

- [Generate your first annotation file](tutorials/first-steps.md) in a guided
  Python tutorial.
- [Install and configure the plugin](how-to/index.md) for a specific task.
- Look up the exact [plugin contract](reference/api.md) or
  [annotation mapping](reference/annotations.md).
- Understand the [architecture and data flow](explanation/architecture.md).

## Requirements

- Python 3.10 or newer
- A Transpiler-Mate-compatible host when the plugin is not invoked directly
- A context containing normalized software metadata and a selected CWL process
