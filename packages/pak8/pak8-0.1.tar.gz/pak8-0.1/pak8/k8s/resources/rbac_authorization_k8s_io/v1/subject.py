from typing import Optional

from kubernetes.client.models.v1_subject import V1Subject
from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#subject-v1-rbac-authorization-k8s-io
class Subject(BaseModel):
    kind: k8s_enums.Kind
    name: str
    namespace: Optional[str] = None

    def get_k8s_object(self) -> V1Subject:
        # Return a V1Subject object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_subject.py
        _v1_subject = V1Subject(
            kind=self.kind, name=self.name, namespace=self.namespace
        )
        return _v1_subject

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
