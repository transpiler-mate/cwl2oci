# Apply annotations with ORAS

The JSON written by `cwl2oci` follows the ORAS annotation-file format. After
generating `annotations.json`, pass it to an ORAS command that creates a
manifest.

For example, to push `workflow.cwl` as an artifact:

```console
oras push \
  --annotation-file annotations.json \
  --artifact-type application/cwl \
  registry.example.com/workflows/hello:1.0.0 \
  workflow.cwl:application/cwl
```

ORAS treats the `$manifest` entry as annotations for the new manifest. Verify the
result:

```console
oras manifest fetch \
  registry.example.com/workflows/hello:1.0.0 \
  --pretty
```

The fetched manifest contains the generated values in its `annotations` field.
Authentication, registry naming, artifact media types, and publication policy
are outside `cwl2oci`; adapt those values to your registry.

See the ORAS guide to
[manifest annotation files](https://oras.land/docs/how_to_guides/manifest_annotations/)
for other targets such as `$config` and individual layer filenames.
