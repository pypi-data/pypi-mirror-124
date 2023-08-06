from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.common.port import CreatePortData
from pak8.k8s.api.core.v1.volume import CreateVolumeData, create_volume_resource
from pak8.k8s.api.core.v1.container import (
    CreateContainer,
    create_container_resource,
)
from pak8.k8s.k8s_utils import get_default_deploy_name, get_default_pod_name
from pak8.k8s.resources.apps.v1.deployment import (
    Deployment,
    DeploymentSpec,
    LabelSelector,
    PodTemplateSpec,
)
from pak8.k8s.resources.core.v1.container import Container
from pak8.k8s.resources.core.v1.volume import Volume
from pak8.k8s.resources.core.v1.pod_spec import PodSpec
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateDeploymentData(BaseModel):
    containers: List[CreateContainer]
    name: Optional[str] = None
    pod_name: Optional[str] = None
    replicas: Optional[int] = 1
    restart_policy: Optional[k8s_enums.RestartPolicy] = k8s_enums.RestartPolicy.ALWAYS
    termination_grace_period_seconds: Optional[int] = None


def create_deployment_resource(
    group_name: str,
    namespace: str,
    deploy: CreateDeploymentData,
    ports: Optional[List[CreatePortData]] = None,
    volumes: Optional[List[CreateVolumeData]] = None,
    service_account_name: Optional[str] = None,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[Deployment]:
    """Creates a deployment resource.

    TODO:
        * Add doc
        * Add Error Handling
    """
    # logger.debug(f"Creating Deployment Resource: {group_name}")

    if deploy is None:
        return None

    deploy_name = deploy.name if deploy.name else get_default_deploy_name(group_name)
    deploy_labels = create_component_labels_dict(
        component_name=deploy_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    pod_name = deploy.pod_name if deploy.pod_name else get_default_pod_name(group_name)
    pod_labels = create_component_labels_dict(
        component_name=pod_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    create_containers = deploy.containers
    containers: List[Container] = []
    for cc in create_containers:
        container = create_container_resource(
            group_name=group_name,
            container=cc,
            ports=ports,
            volumes=volumes,
        )
        if container:
            containers.append(container)

    _volumes: Optional[List[Volume]] = None
    if volumes:
        _volumes = []
        for _volume in volumes:
            _vol = create_volume_resource(group_name=group_name, volume=_volume)
            if _vol:
                _volumes.append(_vol)

    deployment = Deployment(
        api_version=k8s_enums.ApiVersion.APPS_V1,
        kind=k8s_enums.Kind.DEPLOYMENT,
        metadata=ObjectMeta(
            name=deploy_name,
            namespace=namespace,
            labels=deploy_labels,
        ),
        spec=DeploymentSpec(
            replicas=deploy.replicas,
            selector=LabelSelector(match_labels=pod_labels),
            template=PodTemplateSpec(
                # TODO: fix this
                metadata=ObjectMeta(
                    name=pod_name,
                    namespace=namespace,
                    labels=pod_labels,
                ),
                spec=PodSpec(
                    service_account_name=service_account_name,
                    restart_policy=deploy.restart_policy,
                    containers=containers,
                    termination_grace_period_seconds=deploy.termination_grace_period_seconds,
                    volumes=_volumes,
                ),
            ),
        ),
    )

    # logger.info(
    #     f"Deployment {deploy_name}:\n{deployment.json(exclude_defaults=True, indent=2)}"
    # )
    return deployment
