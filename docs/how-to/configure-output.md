# Configure the generated file

Pass plugin settings through the host runtime using the names below. Because the
Transpiler-Mate API does not define a command-line syntax, consult the runtime's
documentation for how it accepts plugin options.

To construct the settings directly in Python:

```python
from pathlib import Path

from cwl2oci.plugin import CWL2OCIOptions, cwl2oci

options = CWL2OCIOptions(
    output=Path("build/annotations.json"),
    image_source="https://github.com/example/project",
    image_revision="4f8c2ad",
)
cwl2oci.execute(context, options)
```

The parent directory must already exist. The plugin replaces an existing file at
the destination and reports file-system or serialization failures as
`PluginFailureError`.

Omit `image_source` or `image_revision` when that provenance is unknown. Omitted
values do not appear in the output.
