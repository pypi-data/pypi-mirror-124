from typing import Optional

from kubernetes.client.models.v1_role_ref import V1RoleRef
from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#roleref-v1-rbac-authorization-k8s-io
class RoleRef(BaseModel):
    api_group: k8s_enums.ApiGroup
    kind: k8s_enums.Kind
    name: str

    def get_k8s_object(self) -> V1RoleRef:
        # Return a V1RoleRef object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_role_ref.py
        _v1_role_ref = V1RoleRef(
            api_group=self.api_group,
            kind=self.kind,
            name=self.name,
        )
        return _v1_role_ref

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
