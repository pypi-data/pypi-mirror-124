from typing import List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.common.port import CreatePortData
from pak8.k8s.api.core.v1.volume import CreateVolumeData
from pak8.utils.container import image_str
from pak8.k8s.k8s_utils import get_default_container_name
from pak8.k8s.resources.core.v1.container import (
    Container,
    ContainerPort,
    EnvFromSource,
    VolumeMount,
    ConfigMapEnvSource,
    SecretEnvSource,
    EnvVar,
    EnvVarSource,
    ConfigMapKeySelector,
    SecretKeySelector,
)


class CreateEnvVarFromConfigMap(BaseModel):
    env_var_name: str
    configmap_name: str
    configmap_key: Optional[str] = None


class CreateEnvVarFromSecret(BaseModel):
    env_var_name: str
    secret_name: str
    secret_key: Optional[str] = None


class CreateContainer(BaseModel):
    name: Optional[str] = None
    repo: str
    tag: str
    args: Optional[List[str]] = None
    command: Optional[List[str]] = None
    image_pull_policy: Optional[
        k8s_enums.ImagePullPolicy
    ] = k8s_enums.ImagePullPolicy.IF_NOT_PRESENT
    envs_from_configmap: Optional[List[str]] = None
    envs_from_secret: Optional[List[str]] = None
    env_vars_from_secret: Optional[List[CreateEnvVarFromSecret]] = None
    env_vars_from_configmap: Optional[List[CreateEnvVarFromConfigMap]] = None


def create_container_resource(
    group_name: str,
    container: CreateContainer,
    ports: Optional[List[CreatePortData]],
    volumes: Optional[List[CreateVolumeData]] = None,
) -> Container:
    # logger.debug(f"Creating Container Resource: {name}")

    if container is None:
        return None

    container_name = (
        container.name if container.name else get_default_container_name(group_name)
    )

    _container_ports: Optional[List[ContainerPort]] = None
    if ports:
        _container_ports = []
        for _port in ports:
            _container_ports.append(
                ContainerPort(
                    name=_port.name,
                    container_port=_port.container_port,
                    protocol=_port.protocol,
                )
            )

    _env_from: Optional[List[EnvFromSource]] = None
    if container.envs_from_configmap:
        if _env_from is None:
            _env_from = []
        for _cm_envs in container.envs_from_configmap:
            _env_from.append(
                EnvFromSource(config_map_ref=ConfigMapEnvSource(name=_cm_envs))
            )
    if container.envs_from_secret:
        if _env_from is None:
            _env_from = []
        for _secret_envs in container.envs_from_secret:
            _env_from.append(
                EnvFromSource(secret_ref=SecretEnvSource(name=_secret_envs))
            )

    _env: Optional[List[EnvVar]] = None
    if container.env_vars_from_configmap:
        if _env is None:
            _env = []
        for _cm_env_var in container.env_vars_from_configmap:
            _env.append(
                EnvVar(
                    name=_cm_env_var.env_var_name,
                    value_from=EnvVarSource(
                        config_map_key_ref=ConfigMapKeySelector(
                            key=_cm_env_var.configmap_key
                            if _cm_env_var.configmap_key
                            else _cm_env_var.env_var_name,
                            name=_cm_env_var.configmap_name,
                        )
                    ),
                )
            )
    if container.env_vars_from_secret:
        if _env is None:
            _env = []
        for _secret_env_var in container.env_vars_from_secret:
            _env.append(
                EnvVar(
                    name=_secret_env_var.env_var_name,
                    value_from=EnvVarSource(
                        secret_key_ref=SecretKeySelector(
                            key=_secret_env_var.secret_key
                            if _secret_env_var.secret_key
                            else _secret_env_var.env_var_name,
                            name=_secret_env_var.secret_name,
                        )
                    ),
                )
            )

    _volume_mounts: Optional[List[VolumeMount]] = None
    if volumes:
        _volume_mounts = []
        for _volume in volumes:
            _volume_mounts.append(
                VolumeMount(
                    name=_volume.name,
                    mount_path=_volume.mount_path,
                    read_only=_volume.read_only,
                )
            )

    container_resource = Container(
        name=container_name,
        image=image_str(container.repo, container.tag),
        image_pull_policy=container.image_pull_policy,
        args=container.args,
        command=container.command,
        ports=_container_ports,
        env_from=_env_from,
        env=_env,
        volume_mounts=_volume_mounts,
    )
    return container_resource
