<!--
Copyright 2026 Transpiler-Mate

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# CWL 2 OCI

`cwl2oci` is a Transpiler-Mate plugin that generates OCI image annotations from
normalized software metadata and a selected CWL process.

The plugin writes a JSON document containing standard
`org.opencontainers.image.*` properties and CWL-specific `org.cwl.*` properties:

```json
{
  "$manifest": {
    "org.opencontainers.image.title": "Example workflow",
    "org.opencontainers.image.version": "1.0.0",
    "org.cwl.entrypoint": "main",
    "org.cwl.type": "Workflow"
  }
}
```

It implements the
[Transpiler-Mate API](https://github.com/sim13pods/transpiler-mate-api) plugin
contract and registers `cwl2oci.plugin:cwl2oci` in the
`transpiler_mate.plugins` entry-point group. It does not install a standalone
command-line program or build an OCI image.

## Installation

```console
git clone https://github.com/Transpiler-Mate/cwl2oci.git
cd cwl2oci
python -m pip install .
```

Python 3.10 or newer is required. A compatible Transpiler-Mate host supplies the
CWL context and defines how plugins are invoked.

## Documentation

The documentation follows Diátaxis and is published at
<https://Transpiler-Mate.github.io/cwl2oci/>:

- tutorials for guided learning;
- how-to guides for specific tasks;
- reference for the exact plugin and output contracts;
- explanation for architecture and design context.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Submit issues at
<https://github.com/Transpiler-Mate/cwl2oci/issues>.

## License

Licensed under the [Apache License 2.0](LICENSE).
