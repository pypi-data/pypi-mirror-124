from typing import Any, Dict, Optional

from kubernetes.client.models.v1_local_object_reference import V1LocalObjectReference
from pydantic import BaseModel


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#localobjectreference-v1-core
class LocalObjectReference(BaseModel):
    name: str

    def get_k8s_object(self) -> V1LocalObjectReference:

        # Return a V1LocalObjectReference object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_local_object_reference.py
        _v1_local_object_reference = V1LocalObjectReference(name=self.name)
        return _v1_local_object_reference

    class Config:
        arbitrary_types_allowed = True
