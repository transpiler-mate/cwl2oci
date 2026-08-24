# Generate your first annotation file

This tutorial runs the `cwl2oci` plugin directly in Python. You will construct the
small context normally supplied by a Transpiler-Mate runtime and generate an
`annotations.json` file.

## Prerequisites

You need Python 3.10 or newer and an installed copy of `cwl2oci`. See
[Install cwl2oci](../how-to/install.md) if you have not installed it yet.

## Create the example

Create `first_annotations.py`:

```python
from pathlib import Path

from cwl_utils.parser.cwl_v1_2 import Workflow
from pydantic import AnyUrl
from transpiler_mate.api import SoftwareApplication, TranspilerContext

from cwl2oci.plugin import CWL2OCIOptions, cwl2oci


class UnusedResolver:
    def resolve(self, location: str) -> TranspilerContext:
        raise NotImplementedError


process = Workflow(
    id="main",
    cwlVersion="v1.2",
    inputs=[],
    outputs=[],
    steps=[],
)

# A runtime normally validates and supplies this metadata. model_construct keeps
# this standalone example focused on the fields read by cwl2oci.
metadata = SoftwareApplication.model_construct(
    name="Hello workflow",
    description="A minimal CWL workflow",
    software_version="1.0.0",
    license=AnyUrl("https://spdx.org/licenses/Apache-2.0"),
)

context = TranspilerContext(
    source=AnyUrl(Path("workflow.cwl").absolute().as_uri()),
    document=process,
    resolved_process=process,
    metadata=metadata,
    resolver=UnusedResolver(),
)

options = CWL2OCIOptions(
    image_source="https://github.com/example/hello-workflow",
    image_revision="abc123",
)
cwl2oci.execute(context, options)
```

The decorated `cwl2oci` value is a plugin registration. Its `execute` method
accepts a `TranspilerContext` and validated `CWL2OCIOptions`.

## Run the example

```console
python first_annotations.py
```

The command creates `annotations.json` in the current directory:

```json
{"$manifest": {"org.opencontainers.image.title": "Hello workflow", "org.opencontainers.image.description": "A minimal CWL workflow", "org.opencontainers.image.version": "1.0.0", "org.opencontainers.image.source": "https://github.com/example/hello-workflow", "org.opencontainers.image.revision": "abc123", "org.opencontainers.image.licenses": "Apache-2.0", "org.cwl.entrypoint": "main", "org.cwl.spec": "v1.2", "org.cwl.type": "Workflow"}}
```

`$manifest` identifies the target for tools that consume the generated file. Its
value is the string-to-string annotation map for the OCI manifest.

## What you learned

You generated annotations from normalized software metadata and a selected CWL
process. In normal use, a Transpiler-Mate runtime constructs the context and
discovers the plugin; the runtime's documentation defines its command-line or
service interface.

Next, see the [annotation reference](../reference/annotations.md) for the complete
field mapping or [choose a destination](../how-to/configure-output.md).
