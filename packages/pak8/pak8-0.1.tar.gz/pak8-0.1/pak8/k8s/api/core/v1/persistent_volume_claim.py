from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.k8s.resources.core.v1.persistent_volume_claim import PersistentVolumeClaim
from pak8.k8s.resources.core.v1.persistent_volume_claim_spec import (
    PersistentVolumeClaimSpec,
)
from pak8.k8s.resources.core.v1.resource_requirements import ResourceRequirements
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreatePVCData(BaseModel):
    name: str
    access_modes: List[k8s_enums.PVCAccessMode] = [
        k8s_enums.PVCAccessMode.READWRITEONCE
    ]
    request_storage: str
    storage_class_name: str


def create_pvc_resource(
    group_name: str,
    namespace: str,
    pvc: CreatePVCData,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[PersistentVolumeClaim]:
    """Creates a PersistentVolumeClaim resource."""
    # logger.debug(f"Creating PersistentVolumeClaim Resource: {pvc.name}")

    if pvc is None:
        return None

    pvc_name = pvc.name
    pvc_labels = create_component_labels_dict(
        component_name=pvc_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    _pvc = PersistentVolumeClaim(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.PERSISTENTVOLUMECLAIM,
        metadata=ObjectMeta(
            name=pvc_name,
            namespace=namespace,
            labels=pvc_labels,
        ),
        spec=PersistentVolumeClaimSpec(
            access_modes=pvc.access_modes,
            resources=ResourceRequirements(requests={"storage": pvc.request_storage}),
            storage_class_name=pvc.storage_class_name,
        ),
    )

    # logger.info(
    #     f"PersistentVolumeClaim {pvc_name}:\n{_pvc.json(exclude_defaults=True, indent=2)}"
    # )
    return _pvc
