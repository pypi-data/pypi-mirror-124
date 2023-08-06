from typing import Any, List, Optional

from kubernetes.client.models.v1_config_map_env_source import V1ConfigMapEnvSource
from kubernetes.client.models.v1_config_map_key_selector import V1ConfigMapKeySelector
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_container_port import V1ContainerPort
from kubernetes.client.models.v1_env_from_source import V1EnvFromSource
from kubernetes.client.models.v1_env_var import V1EnvVar
from kubernetes.client.models.v1_env_var_source import V1EnvVarSource
from kubernetes.client.models.v1_object_field_selector import V1ObjectFieldSelector
from kubernetes.client.models.v1_probe import V1Probe
from kubernetes.client.models.v1_resource_field_selector import V1ResourceFieldSelector
from kubernetes.client.models.v1_secret_env_source import V1SecretEnvSource
from kubernetes.client.models.v1_secret_key_selector import V1SecretKeySelector
from kubernetes.client.models.v1_volume_mount import V1VolumeMount
from pydantic import BaseModel, Field

import pak8.k8s.enums as k8s_enums
from pak8.k8s.resources.core.v1.resource_requirements import ResourceRequirements


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#resourcefieldselector-v1-core
class ResourceFieldSelector(BaseModel):
    container_name: str = Field(..., alias="containerName")
    divisor: str
    resource: str

    def get_k8s_object(self) -> V1ResourceFieldSelector:

        # Return a V1ResourceFieldSelector object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_resource_field_selector.py
        _v1_resource_field_selector = V1ResourceFieldSelector(
            container_name=self.container_name,
            divisor=self.divisor,
            resource=self.resource,
        )
        return _v1_resource_field_selector

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#objectfieldselector-v1-core
class ObjectFieldSelector(BaseModel):
    api_version: str = Field(..., alias="apiVersion")
    field_path: str

    def get_k8s_object(self) -> V1ObjectFieldSelector:

        # Return a V1ObjectFieldSelector object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_object_field_selector.py
        _v1_object_field_selector = V1ObjectFieldSelector(
            api_version=self.api_version,
            field_path=self.field_path,
        )
        return _v1_object_field_selector

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#secretkeyselector-v1-core
class SecretKeySelector(BaseModel):
    key: str
    name: str
    optional: Optional[bool] = None

    def get_k8s_object(self) -> V1SecretKeySelector:

        # Return a V1SecretKeySelector object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_secret_key_selector.py
        _v1_secret_key_selector = V1SecretKeySelector(
            key=self.key,
            name=self.name,
            optional=self.optional,
        )
        return _v1_secret_key_selector

    class Config:
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#configmapkeyselector-v1-core
class ConfigMapKeySelector(BaseModel):
    key: str
    name: str
    optional: Optional[bool] = None

    def get_k8s_object(self) -> V1ConfigMapKeySelector:

        # Return a V1ConfigMapKeySelector object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_config_map_key_selector.py
        _v1_config_map_key_selector = V1ConfigMapKeySelector(
            key=self.key,
            name=self.name,
            optional=self.optional,
        )
        return _v1_config_map_key_selector

    class Config:
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#envvarsource-v1-core
class EnvVarSource(BaseModel):
    config_map_key_ref: Optional[ConfigMapKeySelector] = Field(
        None, alias="configMapKeyRef"
    )
    field_ref: Optional[ObjectFieldSelector] = Field(None, alias="fieldRef")
    resource_field_ref: Optional[ResourceFieldSelector] = Field(
        None, alias="resourceFieldRef"
    )
    secret_key_ref: Optional[SecretKeySelector] = Field(None, alias="secretKeyRef")

    def get_k8s_object(self) -> V1EnvVarSource:

        # Return a V1EnvVarSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_env_var_source.py
        _v1_env_var_source = V1EnvVarSource(
            config_map_key_ref=self.config_map_key_ref.get_k8s_object()
            if self.config_map_key_ref
            else None,
            field_ref=self.field_ref.get_k8s_object() if self.field_ref else None,
            resource_field_ref=self.resource_field_ref.get_k8s_object()
            if self.resource_field_ref
            else None,
            secret_key_ref=self.secret_key_ref.get_k8s_object()
            if self.secret_key_ref
            else None,
        )
        return _v1_env_var_source

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#envvar-v1-core
class EnvVar(BaseModel):
    name: str
    value: Optional[str] = None
    value_from: Optional[EnvVarSource] = Field(None, alias="valueFrom")

    def get_k8s_object(self) -> V1EnvVar:

        # Return a V1EnvVar object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_env_var.py
        _v1_env_var = V1EnvVar(
            name=self.name,
            value=self.value,
            value_from=self.value_from.get_k8s_object() if self.value_from else None,
        )
        return _v1_env_var

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#configmapenvsource-v1-core
class ConfigMapEnvSource(BaseModel):
    name: str
    optional: Optional[bool] = None


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#secretenvsource-v1-core
class SecretEnvSource(BaseModel):
    name: str
    optional: Optional[bool] = None


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#envfromsource-v1-core
class EnvFromSource(BaseModel):
    config_map_ref: Optional[ConfigMapEnvSource] = Field(None, alias="configMapRef")
    prefix: Optional[str] = None
    secret_ref: Optional[SecretEnvSource] = Field(None, alias="secretRef")

    def get_k8s_object(self) -> V1EnvFromSource:

        # Return a V1EnvFromSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_env_from_source.py
        _config_map_ref = (
            V1ConfigMapEnvSource(
                name=self.config_map_ref.name,
                optional=self.config_map_ref.optional,
            )
            if self.config_map_ref
            else None
        )
        _prefix = self.prefix if self.prefix else None
        _secret_ref = (
            V1SecretEnvSource(
                name=self.secret_ref.name,
                optional=self.secret_ref.optional,
            )
            if self.secret_ref
            else None
        )
        _v1_env_from_source = V1EnvFromSource(
            config_map_ref=_config_map_ref,
            prefix=_prefix,
            secret_ref=_secret_ref,
        )
        return _v1_env_from_source

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#containerport-v1-core
class ContainerPort(BaseModel):
    name: str
    container_port: int = Field(..., alias="containerPort")
    protocol: Optional[k8s_enums.Protocol] = None

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#volumemount-v1-core
class VolumeMount(BaseModel):
    name: str
    mount_path: str = Field(..., alias="mountPath")
    read_only: Optional[bool] = Field(None, alias="readOnly")
    mount_propagation: Optional[str] = Field(None, alias="mountPropagation")
    sub_path: Optional[str] = Field(None, alias="subPath")
    sub_path_expr: Optional[str] = Field(None, alias="subPathExpr")

    class Config:
        allow_population_by_field_name = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#container-v1-core
class Container(BaseModel):
    args: Optional[List[str]] = None
    command: Optional[List[str]] = None
    env_from: Optional[List[EnvFromSource]] = Field(None, alias="envFrom")
    env: Optional[List[EnvVar]] = None
    image_pull_policy: Optional[k8s_enums.ImagePullPolicy] = Field(
        None, alias="imagePullPolicy"
    )
    image: str
    name: str
    ports: Optional[List[ContainerPort]] = None
    readiness_probe: Optional[Any] = Field(None, alias="readinessProbe")
    resources: Optional[ResourceRequirements] = None
    volume_mounts: Optional[List[VolumeMount]] = Field(None, alias="volumeMounts")

    def get_k8s_object(self) -> V1Container:

        # Return a V1Container object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_container.py
        _ports: Optional[List[V1ContainerPort]] = None
        if self.ports:
            _ports = []
            for _port in self.ports:
                _ports.append(
                    V1ContainerPort(
                        container_port=_port.container_port,
                        name=_port.name if _port.name else None,
                        protocol=_port.protocol if _port.protocol else None,
                    )
                )

        _env: Optional[List[V1EnvVar]] = None
        if self.env:
            _env = []
            for _env_var in self.env:
                _env.append(_env_var.get_k8s_object())

        _env_from: Optional[List[V1EnvFromSource]] = None
        if self.env_from:
            _env_from = []
            for _env_from_var in self.env_from:
                _env_from.append(_env_from_var.get_k8s_object())

        _readiness_probe = (
            V1Probe(
                failure_threshold=self.readiness_probe.get("failure_threshold", None),
                http_get=self.readiness_probe.get("http_get", None),
                initial_delay_seconds=self.readiness_probe.get(
                    "initial_delay_seconds", None
                ),
                period_seconds=self.readiness_probe.get("period_seconds", None),
                success_threshold=self.readiness_probe.get("success_threshold", None),
                tcp_socket=self.readiness_probe.get("tcp_socket", None),
                timeout_seconds=self.readiness_probe.get("timeout_seconds", None),
            )
            if self.readiness_probe
            else None
        )

        _resources = self.resources.get_k8s_object() if self.resources else None

        _volume_mounts: Optional[List[V1VolumeMount]] = None
        if self.volume_mounts:
            _volume_mounts = []
            for _volume_mount in self.volume_mounts:
                _volume_mounts.append(
                    V1VolumeMount(
                        mount_path=_volume_mount.mount_path,
                        mount_propagation=_volume_mount.mount_propagation,
                        name=_volume_mount.name,
                        read_only=_volume_mount.read_only,
                        sub_path=_volume_mount.sub_path,
                        sub_path_expr=_volume_mount.sub_path_expr,
                    )
                )

        _v1_container = V1Container(
            args=self.args,
            command=self.command,
            env=_env,
            env_from=_env_from,
            image=self.image,
            image_pull_policy=self.image_pull_policy,
            name=self.name,
            ports=_ports,
            readiness_probe=_readiness_probe,
            resources=_resources,
            volume_mounts=_volume_mounts,
        )
        return _v1_container

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
