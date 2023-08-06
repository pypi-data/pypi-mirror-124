from typing import List, Optional

from kubernetes.client.models.v1_policy_rule import V1PolicyRule
from pydantic import BaseModel


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#policyrule-v1-rbac-authorization-k8s-io
class PolicyRule(BaseModel):
    api_groups: List[str]
    resources: List[str]
    verbs: List[str]

    def get_k8s_object(self) -> V1PolicyRule:
        # Return a V1PolicyRule object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_policy_rule.py
        _v1_policy_rule = V1PolicyRule(
            api_groups=self.api_groups,
            resources=self.resources,
            verbs=self.verbs,
        )
        return _v1_policy_rule

    class Config:
        arbitrary_types_allowed = True
