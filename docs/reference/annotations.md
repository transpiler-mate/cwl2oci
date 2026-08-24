# Annotation and output reference

The output is compact JSON with one top-level target, `$manifest`:

```json
{
  "$manifest": {
    "org.opencontainers.image.title": "Example"
  }
}
```

This is the
[ORAS annotation-file format](https://oras.land/docs/how_to_guides/manifest_annotations/):
`$manifest` tells ORAS to apply the enclosed map to the OCI manifest itself. All
annotation values emitted by this plugin are strings. Keys whose values are
`None` are omitted.

## Generated annotations

| Annotation | Source | Required in output | Transformation |
| --- | --- | --- | --- |
| `org.opencontainers.image.title` | `context.metadata.name` | Yes | Copied unchanged. |
| `org.opencontainers.image.description` | `context.metadata.description` | Yes | Carriage returns are removed; newlines become spaces. |
| `org.opencontainers.image.version` | `context.metadata.software_version` | Yes | Copied unchanged. |
| `org.opencontainers.image.licenses` | `context.metadata.license` | Yes | Converted as described below. |
| `org.opencontainers.image.source` | `options.image_source` | No | Omitted when unset. |
| `org.opencontainers.image.revision` | `options.image_revision` | No | Omitted when unset. |
| `org.cwl.entrypoint` | `context.resolved_process.id` | Yes | Copied unchanged. |
| `org.cwl.spec` | `context.resolved_process.cwlVersion` | No | Converted to a string; omitted when unset. |
| `org.cwl.type` | `context.resolved_process.class_` | Yes | Copied unchanged. |

The `org.opencontainers.image.*` keys are defined by the
[OCI Image Specification](https://specs.opencontainers.org/image-spec/annotations/).
The `org.cwl.*` keys are cwl2oci extensions using a separate reverse-domain
namespace.

## License conversion

For a Schema.org `CreativeWork`, the plugin converts `identifier` to a string. For
a URL, it uses the final slash-separated component. For example,
`https://spdx.org/licenses/Apache-2.0` becomes `Apache-2.0`.

When metadata contains a list of licenses, the converted values are joined with
` OR `. The result is used as the OCI SPDX license expression; the plugin does
not independently validate the expression.

## File behavior

- The default path is `annotations.json` relative to the process working
  directory.
- The file is opened in text write mode, so an existing destination is replaced.
- Parent directories are not created.
- JSON is emitted without indentation or a trailing newline.
- A successful execution returns `None`; the file is the result.
