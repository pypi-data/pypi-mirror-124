from kubernetes.client.models.v1_pod_template_spec import V1PodTemplateSpec
from pydantic import BaseModel

from pak8.k8s.resources.core.v1.pod_spec import PodSpec
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#podtemplatespec-v1-core
class PodTemplateSpec(BaseModel):
    metadata: ObjectMeta
    spec: PodSpec

    def get_k8s_object(self) -> V1PodTemplateSpec:

        # Set and return a V1PodTemplateSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_pod_template_spec.py
        _v1_pod_template_spec = V1PodTemplateSpec(
            metadata=self.metadata.get_k8s_object(),
            spec=self.spec.get_k8s_object(),
        )
        return _v1_pod_template_spec

    class Config:
        arbitrary_types_allowed = True
