from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.apps.v1.deployment import CreateDeploymentData
from pak8.k8s.api.common.port import CreatePortData
from pak8.k8s.k8s_utils import get_default_pod_name, get_default_svc_name
from pak8.k8s.resources.core.v1.service import Service, ServicePort, ServiceSpec
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateServiceData(BaseModel):
    name: Optional[str] = None
    service_type: k8s_enums.ServiceType = k8s_enums.ServiceType.CLUSTERIP
    external_traffic_policy: Optional[str] = None
    load_balancer_ip: Optional[str] = None
    load_balancer_source_ranges: Optional[List[str]] = None
    target_deploy: Optional[CreateDeploymentData] = None
    target_deploy_group: Optional[str] = None


def create_service_resource(
    group_name: str,
    namespace: str,
    svc: CreateServiceData,
    ports: Optional[List[CreatePortData]] = None,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[Service]:
    """Creates a service resource.

    TODO:
        * Add doc
        * Add Error Handling
    """
    # logger.debug(f"Creating Service Resource: {group_name}")

    if svc is None:
        return None

    svc_name = svc.name if svc.name else get_default_svc_name(group_name)
    svc_labels = create_component_labels_dict(
        component_name=svc_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    target_deploy_group = (
        svc.target_deploy_group if svc.target_deploy_group else group_name
    )
    target_pod_name = (
        svc.target_deploy.pod_name
        if svc.target_deploy and svc.target_deploy.pod_name
        else get_default_pod_name(target_deploy_group)
    )
    target_pod_labels = create_component_labels_dict(
        component_name=target_pod_name,
        part_of=target_deploy_group,
        common_labels=common_labels,
    )

    _service_ports: Optional[List[ServicePort]] = None
    if ports:
        _service_ports = []
        for _port in ports:
            # logger.debug(f"Creating ServicePort for {_port}")
            _service_ports.append(
                ServicePort(
                    name=_port.name,
                    port=_port.svc_port if _port.svc_port else _port.container_port,
                    protocol=_port.protocol,
                    target_port=_port.name,
                )
            )

    service = Service(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.SERVICE,
        metadata=ObjectMeta(
            name=svc_name,
            namespace=namespace,
            labels=svc_labels,
        ),
        spec=ServiceSpec(
            external_traffic_policy=svc.external_traffic_policy,
            load_balancer_ip=svc.load_balancer_ip,
            load_balancer_source_ranges=svc.load_balancer_source_ranges,
            ports=_service_ports,
            selector=target_pod_labels,
            type=svc.service_type,
        ),
    )

    # logger.info(f"Service {svc_name}:\n{service.json(exclude_defaults=True, indent=2)}")
    return service
