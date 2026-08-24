# Plugin API

The package exports version information from `cwl2oci`; the plugin registration
and its options model live in `cwl2oci.plugin`.

## Registration

```python
from cwl2oci.plugin import cwl2oci
```

| Attribute | Value |
| --- | --- |
| Entry-point group | `transpiler_mate.plugins` |
| Entry-point name | `cwl2oci` |
| Entry-point object | `cwl2oci.plugin:cwl2oci` |
| Registration name | `cwl2oci` |
| Options model | `CWL2OCIOptions` |
| Execution return value | `None` |

`cwl2oci` is a `transpiler_mate.api.PluginRegistration`, not a function. Invoke
the transformation with `cwl2oci.execute(context, options)`.

## Options

```python
from cwl2oci.plugin import CWL2OCIOptions
```

| Field | Type | Default | Meaning |
| --- | --- | --- | --- |
| `output` | `pathlib.Path` | `annotations.json` | File written by the plugin. |
| `image_source` | `str \| None` | `None` | Source-code URL placed in `org.opencontainers.image.source`. |
| `image_revision` | `str \| None` | `None` | Source-control revision placed in `org.opencontainers.image.revision`. |

Unknown option fields are forbidden. Pydantic performs construction and
validation before plugin execution when the host follows the API contract.

## Input requirements

The `TranspilerContext` must contain a selected process in `resolved_process`.
When it is `None`, execution raises `PluginExecutionError` with a request to add a
`#<process-id>` fragment to the source location.

The implementation reads these metadata fields:

- `name`
- `description`
- `software_version`
- `license`

It also reads `id`, `cwlVersion`, and `class_` from the selected CWL process.

## Errors

| Condition | Exception |
| --- | --- |
| No selected process | `PluginExecutionError` |
| Opening, serializing, or writing the output fails | `PluginFailureError`, with the original exception chained as `__cause__` |
| Invalid options | Pydantic `ValidationError` during option construction |
