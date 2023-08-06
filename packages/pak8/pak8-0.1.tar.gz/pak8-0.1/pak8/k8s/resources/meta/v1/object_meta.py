from typing import Any, Dict, Optional

from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from pydantic import BaseModel


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#objectmeta-v1-meta
class ObjectMeta(BaseModel):
    name: str
    namespace: Optional[str] = None
    labels: Dict[str, str]

    def get_k8s_object(self) -> V1ObjectMeta:
        # Return a V1ObjectMeta object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_object_meta.py
        _v1_object_meta = V1ObjectMeta(
            name=self.name,
            namespace=self.namespace,
            labels=self.labels,
        )
        return _v1_object_meta

    class Config:
        arbitrary_types_allowed = True
