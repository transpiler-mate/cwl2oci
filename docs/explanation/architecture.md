# Architecture and data flow

`cwl2oci` is a transformation plugin, not a command-line application. It depends
on the framework-neutral contracts in `transpiler-mate-api`; a host runtime owns
source resolution, metadata preparation, option transport, and plugin discovery.

```text
host runtime
  resolves CWL and selects #process-id
  normalizes SoftwareApplication metadata
  validates CWL2OCIOptions
           |
           v
cwl2oci plugin registration
  maps metadata and the selected process
  validates the annotation model
  serializes {"$manifest": {...}}
           |
           v
annotations.json
```

## Why a process must be selected

A CWL document can contain multiple processes. Values such as the entry point,
CWL version, and process class must describe one target, so the plugin rejects a
context whose `resolved_process` is `None`. Selecting a `#<process-id>` is a
runtime responsibility.

## Two annotation namespaces

The plugin combines two kinds of metadata:

- `org.opencontainers.image.*` describes the packaged software using keys
  standardized by the OCI Image Specification.
- `org.cwl.*` records CWL-specific execution identity and has no claim on OCI's
  reserved namespace.

OCI permits namespaced extension annotations and requires consumers to tolerate
unknown keys. This lets CWL-specific metadata travel in the same string map as
standard image metadata.

## The `$manifest` envelope

OCI defines an `annotations` map inside manifests and descriptors, but it does
not define the `$manifest` wrapper written here. `$manifest` comes from the ORAS
annotation-file format and directs ORAS to apply the map to a manifest. `cwl2oci`
only generates the JSON file; it does not build an image or modify an OCI
manifest itself.

## Model boundary

`schemas/oci_annotations.yaml` defines the generated `OciAnnotations` Pydantic
model. The plugin constructs this model before serialization, which enforces the
required annotation values and aliases Python field names to dotted annotation
keys. Optional provenance and CWL-version fields disappear when unset.
