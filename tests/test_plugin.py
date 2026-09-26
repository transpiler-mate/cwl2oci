# Copyright 2026 Terradue
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from cwl_utils.parser.cwl_v1_2 import CommandLineTool
from pydantic import AnyUrl, ValidationError
from transpiler_mate.api import (
    CreativeWork,
    PluginFailureError,
    SoftwareApplication,
    TranspilerContext,
    TranspilerContextResolver,
)

from cwl2oci.plugin import CWL2OCIOptions, cwl2oci


@pytest.fixture
def context() -> TranspilerContext:
    metadata = SoftwareApplication.model_validate(
        {
            "name": "Example application",
            "description": "First line\r\nSecond line\nThird line",
            "dateCreated": "2026-01-01",
            "softwareVersion": "1.2.3",
            "license": "https://spdx.org/licenses/Apache-2.0",
            "softwareHelp": {"url": "https://example.org/help"},
            "publisher": {"name": "Example publisher"},
            "author": {
                "givenName": "Test",
                "familyName": "Author",
                "email": "author@example.org",
                "affiliation": {"name": "Example publisher"},
            },
        }
    )
    process = CommandLineTool(
        id="https://example.org/tool.cwl#main", inputs=[], outputs=[], cwlVersion="v1.2"
    )
    return TranspilerContext(
        source=AnyUrl("https://example.org/tool.cwl"),
        process_id="main",
        metadata=metadata,
        document={"main": process},
        resolver=Mock(spec=TranspilerContextResolver),
    )


def test_registration_and_default_options() -> None:
    assert cwl2oci.name == "cwl2oci"
    assert cwl2oci.options_model is CWL2OCIOptions
    options = CWL2OCIOptions.model_validate({})
    assert options.output == Path("annotations.json")
    assert options.image_source is None
    assert options.image_revision is None


def test_options_parse_output_path() -> None:
    options = CWL2OCIOptions.model_validate({"output": "nested/annotations.json"})
    assert options.output == Path("nested/annotations.json")


def test_options_reject_unknown_fields() -> None:
    with pytest.raises(ValidationError) as error:
        CWL2OCIOptions.model_validate({"image_sorce": "https://example.org/source"})
    assert error.value.errors()[0]["type"] == "extra_forbidden"


def test_writes_manifest_with_optional_annotations(
    context: TranspilerContext, tmp_path: Path
) -> None:
    output = tmp_path / "nested" / "annotations.json"
    options = CWL2OCIOptions(
        output=output, image_source="https://example.org/source", image_revision="abc123"
    )

    cwl2oci.execute(context, options)

    assert json.loads(output.read_text()) == {
        "$manifest": {
            "org.opencontainers.image.title": "Example application",
            "org.opencontainers.image.description": "First line Second line Third line",
            "org.opencontainers.image.version": "1.2.3",
            "org.opencontainers.image.licenses": "Apache-2.0",
            "org.opencontainers.image.source": "https://example.org/source",
            "org.opencontainers.image.revision": "abc123",
            "org.cwl.entrypoint": "https://example.org/tool.cwl#main",
            "org.cwl.spec": "v1.2",
            "org.cwl.type": "CommandLineTool",
        }
    }


def test_default_output_omits_absent_annotations(
    context: TranspilerContext, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    context.resolved_process.cwlVersion = None

    cwl2oci.execute(context, CWL2OCIOptions.model_validate({}))

    manifest = json.loads((tmp_path / "annotations.json").read_text())["$manifest"]
    assert "org.opencontainers.image.source" not in manifest
    assert "org.opencontainers.image.revision" not in manifest
    assert "org.cwl.spec" not in manifest
    assert manifest["org.cwl.type"] == "CommandLineTool"


@pytest.mark.parametrize(
    ("licenses", "expected"),
    [
        (CreativeWork(identifier="MIT"), "MIT"),
        (AnyUrl("https://spdx.org/licenses/BSD-3-Clause"), "BSD-3-Clause"),
        (
            [CreativeWork(identifier="MIT"), AnyUrl("https://spdx.org/licenses/Apache-2.0")],
            "MIT OR Apache-2.0",
        ),
        ([CreativeWork(identifier="MIT")], "MIT"),
    ],
)
def test_serializes_license_identifiers(
    context: TranspilerContext,
    tmp_path: Path,
    licenses: CreativeWork | AnyUrl | list[CreativeWork | AnyUrl],
    expected: str,
) -> None:
    context.metadata.license = licenses
    output = tmp_path / "annotations.json"

    cwl2oci.execute(context, CWL2OCIOptions(output=output))

    manifest = json.loads(output.read_text())["$manifest"]
    assert manifest["org.opencontainers.image.licenses"] == expected


def test_overwrites_existing_output(context: TranspilerContext, tmp_path: Path) -> None:
    output = tmp_path / "annotations.json"
    output.write_text("obsolete content" * 100)

    cwl2oci.execute(context, CWL2OCIOptions(output=output))

    assert json.loads(output.read_text())["$manifest"]["org.cwl.spec"] == "v1.2"


@pytest.mark.parametrize("operation", ["mkdir", "open", "dump"])
def test_serialization_failures_preserve_cause_and_output_path(
    context: TranspilerContext, tmp_path: Path, operation: str
) -> None:
    output = tmp_path / "annotations.json"
    failure = OSError("storage unavailable")
    target = "cwl2oci.plugin.json.dump" if operation == "dump" else f"pathlib.Path.{operation}"

    with patch(target, side_effect=failure), pytest.raises(PluginFailureError) as error:
        cwl2oci.execute(context, CWL2OCIOptions(output=output))

    assert error.value.__cause__ is failure
    assert str(output.absolute()) in str(error.value)
