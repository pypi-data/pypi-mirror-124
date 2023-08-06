from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
    CustomResourceDefinition,
)
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition_spec import (
    CustomResourceDefinitionSpec,
)
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition_spec import (
    CustomResourceDefinitionNames,
)
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateCRDName(BaseModel):
    kind: str
    plural: str
    singular: str


class CreateCRDData(BaseModel):
    name: str
    group: str
    version: str
    names: CreateCRDName
    scope: Optional[str] = "Namespaced"


def create_crd_resource(
    group_name: str,
    crd: CreateCRDData,
) -> Optional[CustomResourceDefinition]:
    """Creates a CustomResourceDefinition resource."""
    # logger.debug(f"Creating CRD Resource: {group_name}")

    if crd is None:
        return None

    crd_name = crd.name
    crd_labels = create_component_labels_dict(
        component_name=crd_name,
        part_of=group_name,
    )

    _crd = CustomResourceDefinition(
        api_version=k8s_enums.ApiVersion.APIEXTENSIONS_V1BETA1,
        kind=k8s_enums.Kind.CUSTOMRESOURCEDEFINITION,
        metadata=ObjectMeta(
            name=crd_name,
            labels=crd_labels,
        ),
        spec=CustomResourceDefinitionSpec(
            group=crd.group,
            names=CustomResourceDefinitionNames(
                kind=crd.names.kind,
                plural=crd.names.plural,
                singular=crd.names.singular,
            ),
            scope=crd.scope,
            version=crd.version,
        ),
    )

    # logger.info(f"CRD {crd_name}:\n{_crd.json(exclude_defaults=True, indent=2)}")
    return _crd
