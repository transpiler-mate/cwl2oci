# Copyright 2026 Transpiler-Mate
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

"""transpiler-mate plugin for CWL 2 OCI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from loguru import logger
from pydantic import AnyUrl, BaseModel, ConfigDict, Field
from transpiler_mate.api import (
    CreativeWork,
    PluginFailureError,
    SoftwareApplication,
    transpiler_plugin,
)

from .oci_annotations_models import OciAnnotations

if TYPE_CHECKING:
    from transpiler_mate.api import TranspilerContext


class CWL2OCIOptions(BaseModel):
    """Options accepted by the CWL 2 OCI plugin."""

    model_config = ConfigDict(extra="forbid")

    image_source: Annotated[
        str | None, Field(description="URL to get source code for building the image")
    ] = None
    image_revision: Annotated[
        str | None,
        Field(
            description="Source control revision identifier for the packaged software"
        ),
    ] = None
    output: Annotated[
        Path,
        Field(default=Path("annotations.json"), description="The output file path"),
    ]


def _to_license_spdx(license: CreativeWork | AnyUrl) -> str:
    if isinstance(license, CreativeWork):
        return str(license.identifier)
    return str(license).split("/")[-1]


@transpiler_plugin(
    name="cwl2oci",
    description="CWL2OCI Transpiler-Mate Plugin.",
    options_model=CWL2OCIOptions,
)
def cwl2oci(context: TranspilerContext, options: CWL2OCIOptions) -> None:
    """CWL2OCI Transpiler-Mate Plugin."""

    metadata: SoftwareApplication = context.metadata
    resolved_process = context.resolved_process

    oci_annotations: OciAnnotations = OciAnnotations(
        # org.opencontainers.image.* properties
        org_opencontainers_image_title=metadata.name,
        org_opencontainers_image_description=(
            metadata.description.replace("\n", " ").replace("\r", "")
        ),
        org_opencontainers_image_version=(metadata.software_version),
        org_opencontainers_image_licenses=(
            " OR ".join(
                [_to_license_spdx(license) for license in metadata.license]
            )
            if isinstance(metadata.license, list)
            else _to_license_spdx(metadata.license)
        ),
        org_opencontainers_image_source=options.image_source,
        org_opencontainers_image_revision=options.image_revision,
        # org.cwl.* properties
        org_cwl_entrypoint=resolved_process.id,
        org_cwl_spec=str(resolved_process.cwlVersion)
        if resolved_process.cwlVersion
        else None,
        org_cwl_type=resolved_process.class_,
    )

    annotations: dict[str, Any] = {
        "$manifest": oci_annotations.model_dump(by_alias=True, exclude_none=True)
    }

    try:
        logger.info(f"Serializing OCI Annotations to {options.output.absolute()}")

        with options.output.open("w") as output_stream:
            json.dump(annotations, output_stream, indent=2)

        logger.success(f"OCI Annotations successfully serialized to {options.output.absolute()}")
    except Exception as e:
        raise PluginFailureError(
            f"An error occurred when serializing to {options.output.absolute()}, see nested exception"
        ) from e
