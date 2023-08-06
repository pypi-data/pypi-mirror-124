from typing import Dict, List, Optional, Union

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_service import V1Service
from kubernetes.client.models.v1_service_list import V1ServiceList
from kubernetes.client.models.v1_service_port import V1ServicePort
from kubernetes.client.models.v1_service_spec import V1ServiceSpec
from kubernetes.client.models.v1_status import V1Status
from pydantic import BaseModel, Field

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#serviceport-v1-core
class ServicePort(BaseModel):
    """References:
    * Docs:
        https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#serviceport-v1-core
    * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service_port.py
    """

    name: str
    # node_port: Optional[int] = None
    port: int
    protocol: k8s_enums.Protocol
    target_port: Union[str, int] = Field(..., alias="targetPort")

    def get_k8s_object(self) -> V1ServicePort:

        # Return a V1ServicePort object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service_port.py
        _v1_service_port = V1ServicePort(
            name=self.name,
            # node_port=self.node_port,
            port=self.port,
            protocol=self.protocol,
            target_port=self.target_port,
        )
        return _v1_service_port

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#servicespec-v1-core
class ServiceSpec(BaseModel):
    type: k8s_enums.ServiceType
    # cluster_ip: Optional[str] = Field(None, alias="clusterIP")
    # external_i_ps: Optional[List[str]] = Field(None, alias="externalIPs")
    # external_name: Optional[str] = Field(None, alias="externalName")
    external_traffic_policy: Optional[str] = Field(None, alias="externalTrafficPolicy")
    # health_check_node_port: Optional[int] = Field(None, alias="healthCheckNodePort")
    load_balancer_ip: Optional[str] = Field(None, alias="loadBalancerIP")
    load_balancer_source_ranges: Optional[List[str]] = Field(
        None, alias="loadBalancerSourceRanges"
    )
    ports: List[ServicePort]
    # publish_not_ready_addresses: Optional[bool] = Field(None, alias="publishNotReadyAddresses")
    selector: Dict[str, str]
    # session_affinity: Optional[str] = Field(None, alias="sessionAffinity")
    # session_affinity_config: Optional[V1SessionAffinityConfig] = Field(None, alias="sessionAffinityConfig")

    def get_k8s_object(self) -> V1ServiceSpec:

        # Return a V1ServiceSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service_spec.py
        _ports: Optional[List[V1ServicePort]] = None
        if self.ports:
            _ports = []
            for _port in self.ports:
                _ports.append(_port.get_k8s_object())

        _v1_service_spec = V1ServiceSpec(
            external_traffic_policy=self.external_traffic_policy,
            load_balancer_ip=self.load_balancer_ip,
            load_balancer_source_ranges=self.load_balancer_source_ranges,
            ports=_ports,
            selector=self.selector,
            type=self.type,
        )
        return _v1_service_spec

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True


class Service(K8sResourceBase):
    """Pak8 representation of a K8s Service: An abstract way to expose an application running on a set of Pods as a network service.

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#service-v1-core
            https://kubernetes.io/docs/concepts/services-networking/service/
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service.py
    Notes:
        * The name of a Service object must be a valid DNS label name.
    """

    spec: ServiceSpec
    # V1Service object received as the output after creating the svc
    v1_service: Optional[V1Service] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["spec"]

    class Config:
        arbitrary_types_allowed = True

    def get_k8s_object(self) -> V1Service:
        """Creates a body for this Service"""

        # Return a V1Service object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service.py
        _v1_service = V1Service(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            spec=self.spec.get_k8s_object(),
        )
        return _v1_service

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1Service]:
        """Returns the "Active" Service from the cluster"""

        _active_svc: Optional[V1Service] = None
        _active_svcs: Optional[List[V1Service]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_svcs: {_active_svcs}")
        if _active_svcs is None:
            return None

        _active_svcs_dict = {_svc.metadata.name: _svc for _svc in _active_svcs}

        _svc_name = self.get_resource_name()
        if _svc_name in _active_svcs_dict:
            _active_svc = _active_svcs_dict[_svc_name]
            self.__setattr__("v1_service", _active_svc)
            # logger.debug(f"Found {_svc_name}")
        return _active_svc

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1Service]]:
        """Reads Services from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        svc_list: Optional[V1ServiceList] = None
        if namespace:
            # logger.debug(f"Getting SAs for ns: {namespace}")
            svc_list = k8s_core_v1_api.list_namespaced_service(namespace=namespace)
        else:
            # logger.debug("Getting SAs for all namespaces")
            svc_list = k8s_core_v1_api.list_service_for_all_namespaces()

        svcs: Optional[List[V1Service]] = None
        if svc_list:
            svcs = svc_list.items
        # logger.debug(f"svcs: {svcs}")
        # logger.debug(f"svcs type: {type(svcs)}")

        return svcs

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1Service = self.get_k8s_object()
        v1_service: V1Service = k8s_core_v1_api.create_namespaced_service(
            namespace=namespace, body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_service.to_dict(), indent=2)))
        if v1_service.metadata.creation_timestamp is not None:
            logger.debug("Service Created")
            self.__setattr__("v1_service", v1_service)
            return True
        logger.error("Service could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _svc_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_svc_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_core_v1_api.delete_namespaced_service(
            name=_svc_name, namespace=namespace
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("Service Deleted")
            self.__setattr__("v1_service", None)
            return True
        return False

    def _update(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_completion: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_completion
        _svc_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_svc_name))

        _k8s_object: V1Service = self.get_k8s_object()
        v1_service: V1Service = k8s_core_v1_api.patch_namespaced_service(
            name=_svc_name, namespace=namespace, body=_k8s_object
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_service.to_dict(), indent=2)))
        if v1_service.metadata.creation_timestamp is not None:
            logger.debug("Service Updated")
            self.__setattr__("v1_service", v1_service)
            return True
        logger.error("Service could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_svc: Optional[V1Service] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_svc:
            return True
        return False

    def create_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        only_if_not_active: Optional[bool] = True,
    ) -> bool:

        if only_if_not_active and self.is_active_on_cluster(k8s_api, namespace):
            logger.debug(
                f"Service {self.get_resource_name()} is already active, skipping create"
            )
            return True
        return self._create(k8s_api, namespace)

    def delete_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._delete(k8s_api, namespace)
        logger.debug(
            f"Service {self.get_resource_name()} does not exist, skipping delete"
        )
        return True

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._update(k8s_api, namespace)
        logger.debug(
            f"Service {self.get_resource_name()} does not exist, skipping update"
        )
        return True
