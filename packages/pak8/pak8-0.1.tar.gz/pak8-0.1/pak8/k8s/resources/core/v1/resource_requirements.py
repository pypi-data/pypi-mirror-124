from typing import Dict, Optional

from kubernetes.client.models.v1_resource_requirements import V1ResourceRequirements
from pydantic import BaseModel


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#resourcerequirements-v1-core
class ResourceRequirements(BaseModel):
    limits: Optional[Dict[str, str]] = None
    requests: Optional[Dict[str, str]] = None

    def get_k8s_object(self) -> V1ResourceRequirements:

        # Return a V1ResourceRequirements object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_resource_requirements.py

        _v1_resource_requirements = V1ResourceRequirements(
            limits=self.limits,
            requests=self.requests,
        )
        return _v1_resource_requirements

    class Config:
        arbitrary_types_allowed = True
