from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.k8s.resources.storage_k8s_io.v1.storage_class import StorageClass
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta
from pak8.k8s.exceptions import StorageClassTypeNotFoundException


class CreateStorageClassData(BaseModel):
    name: str
    storage_class_type: k8s_enums.StorageClassType


def create_storage_class_resource(
    group_name: str,
    namespace: str,
    storage_class: CreateStorageClassData,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[StorageClass]:
    """Creates a StorageClass resource."""
    # logger.debug(f"Creating StorageClass Resource: {group_name}")

    if storage_class is None:
        return None

    storage_class_name = storage_class.name
    storage_class_type = storage_class.storage_class_type
    storage_class_labels = create_component_labels_dict(
        component_name=storage_class_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    _provisioner: Optional[str] = None
    _parameters: Optional[Dict[str, str]] = None
    if storage_class_type == k8s_enums.StorageClassType.GCE_SSD:
        _provisioner = "kubernetes.io/gce-pd"
        _parameters = {"type": "pd-ssd"}
    elif storage_class_type == k8s_enums.StorageClassType.GCE_STANDARD:
        _provisioner = "kubernetes.io/gce-pd"
        _parameters = {"type": "pd-standard"}
    else:
        raise StorageClassTypeNotFoundException(f"{storage_class_type} not found")

    _storage_class = StorageClass(
        api_version=k8s_enums.ApiVersion.STORAGE_V1,
        kind=k8s_enums.Kind.STORAGECLASS,
        metadata=ObjectMeta(
            name=storage_class_name,
            namespace=namespace,
            labels=storage_class_labels,
        ),
        provisioner=_provisioner,
        parameters=_parameters,
    )

    # logger.info(
    #     f"StorageClass {storage_class_name}:\n{_storage_class.json(exclude_defaults=True, indent=2)}"
    # )
    return _storage_class
