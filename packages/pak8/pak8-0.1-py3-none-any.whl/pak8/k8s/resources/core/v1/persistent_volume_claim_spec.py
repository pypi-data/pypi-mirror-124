from typing import List

from kubernetes.client.models.v1_persistent_volume_claim_spec import (
    V1PersistentVolumeClaimSpec,
)
from pydantic import BaseModel, Field

import pak8.k8s.enums as k8s_enums
from pak8.k8s.resources.core.v1.resource_requirements import ResourceRequirements


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim_spec.py
class PersistentVolumeClaimSpec(BaseModel):

    access_modes: List[k8s_enums.PVCAccessMode] = Field(..., alias="accessModes")
    resources: ResourceRequirements
    storage_class_name: str = Field(..., alias="storageClassName")

    def get_k8s_object(
        self,
    ) -> V1PersistentVolumeClaimSpec:

        # Return a V1PersistentVolumeClaimSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim_spec.py
        _v1_persistent_volume_claim_spec = V1PersistentVolumeClaimSpec(
            access_modes=self.access_modes,
            resources=self.resources.get_k8s_object(),
            storage_class_name=self.storage_class_name,
        )
        return _v1_persistent_volume_claim_spec

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
