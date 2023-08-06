from typing import Any, Dict, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
    CreateCRDData,
)
from pak8.utils.log import logger
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_object import CustomObject
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateCustomObjectData(BaseModel):
    name: str
    crd: CreateCRDData
    spec: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None


def create_custom_object_resource(
    group_name: str,
    namespace: str,
    custom_object: CreateCustomObjectData,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[CustomObject]:
    """Creates a CustomObject resource."""
    # logger.debug(f"Creating CustomObject Resource: {group_name}")

    if custom_object is None:
        return None

    custom_object_name = custom_object.name
    custom_object_labels = create_component_labels_dict(
        component_name=custom_object_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    _object_api_version: str = "{}/{}".format(
        custom_object.crd.group, custom_object.crd.version
    )
    try:
        _api_version: k8s_enums.ApiVersion = k8s_enums.ApiVersion.from_str(_object_api_version)  # type: ignore
    except NotImplementedError as e:
        logger.error(f"{_object_api_version} is not a valid API version")
        return None

    try:
        _kind: k8s_enums.Kind = k8s_enums.Kind.from_str(custom_object.crd.names.kind)  # type: ignore
    except NotImplementedError as e:
        logger.error(f"{custom_object.crd.names.kind} is not a valid Kind")
        return None

    _custom_object = CustomObject(
        api_version=_api_version,
        kind=_kind,
        metadata=ObjectMeta(name=custom_object_name, labels=custom_object_labels),
        group=custom_object.crd.group,
        version=custom_object.crd.version,
        plural=custom_object.crd.names.plural,
        spec=custom_object.spec,
        body=custom_object.body,
    )

    # logger.info(f"CustomObject {custom_object_name}:\n{_custom_object.json(exclude_defaults=True, indent=2)}")
    # logger.info(f"CustomObject {custom_object_name}:\n{_custom_object.set_and_get_custom_object_body()}")
    return _custom_object
