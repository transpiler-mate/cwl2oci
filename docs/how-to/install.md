# Install cwl2oci

`cwl2oci` requires Python 3.10 or newer.

## Install the current source tree

```console
git clone https://github.com/Transpiler-Mate/cwl2oci.git
cd cwl2oci
python -m pip install .
```

The current project metadata obtains `transpiler-mate-api` from its Git
repository, so installing from source requires Git and network access.

The package installs a plugin entry point named `cwl2oci` in the
`transpiler_mate.plugins` group. It does not install a standalone `cwl2oci`
command. A compatible host runtime is responsible for discovering and invoking
the entry point.

## Verify the installation

Inspect the registration from Python:

```console
python -c "from cwl2oci.plugin import cwl2oci; print(cwl2oci.name)"
```

The command prints `cwl2oci`.
