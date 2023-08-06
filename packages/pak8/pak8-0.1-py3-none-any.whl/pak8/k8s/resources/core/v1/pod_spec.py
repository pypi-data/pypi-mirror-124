from typing import List, Optional

from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_pod_spec import V1PodSpec
from kubernetes.client.models.v1_volume import V1Volume
from pydantic import BaseModel, Field

import pak8.k8s.enums as k8s_enums
from pak8.k8s.resources.core.v1.container import Container
from pak8.k8s.resources.core.v1.local_object_reference import LocalObjectReference
from pak8.k8s.resources.core.v1.volume import Volume


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#podspec-v1-core
class PodSpec(BaseModel):
    containers: List[Container]
    image_pull_secrets: Optional[List[LocalObjectReference]] = Field(
        None, alias="imagePullSecrets"
    )
    restart_policy: Optional[k8s_enums.RestartPolicy] = Field(
        None, alias="restartPolicy"
    )
    service_account_name: Optional[str] = Field(None, alias="serviceAccountName")
    termination_grace_period_seconds: Optional[int] = Field(
        None, alias="terminationGracePeriodSeconds"
    )
    volumes: Optional[List[Volume]] = None

    def get_k8s_object(self) -> V1PodSpec:
        # Set and return a V1PodSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_pod_spec.py

        _containers: Optional[List[V1Container]] = None
        if self.containers:
            _containers = []
            for _container in self.containers:
                _containers.append(_container.get_k8s_object())

        _image_pull_secrets = None
        if self.image_pull_secrets:
            _image_pull_secrets = []
            for ips in self.image_pull_secrets:
                _image_pull_secrets.append(ips.get_k8s_object())

        _volumes: Optional[List[V1Volume]] = None
        if self.volumes:
            _volumes = []
            for _volume in self.volumes:
                _volumes.append(_volume.get_k8s_object())

        _v1_pod_spec = V1PodSpec(
            containers=_containers,
            image_pull_secrets=_image_pull_secrets,
            restart_policy=self.restart_policy,
            service_account_name=self.service_account_name,
            termination_grace_period_seconds=self.termination_grace_period_seconds,
            volumes=_volumes,
        )
        return _v1_pod_spec

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
