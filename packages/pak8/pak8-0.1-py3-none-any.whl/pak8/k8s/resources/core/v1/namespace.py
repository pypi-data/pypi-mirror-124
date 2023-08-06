from typing import List, Optional

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_namespace import V1Namespace
from kubernetes.client.models.v1_namespace_list import V1NamespaceList
from kubernetes.client.models.v1_status import V1Status

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class Namespace(K8sResourceBase):
    """Pak8 representation of a K8s Namespace.
    Kubernetes supports multiple virtual clusters backed by the same physical cluster.
    These virtual clusters are called namespaces.

    We always prefer to create a namespace for deploying a Pak8,
    so we can keep the Pak8 operations independent.

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#namespace-v1-core
            https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_namespace.py
    """

    # V1Namespace object received as the output after creating the ns
    v1_namespace: Optional[V1Namespace] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = []

    def get_k8s_object(self) -> V1Namespace:
        """Creates a body for this Namespace"""

        # Return a V1Namespace object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_namespace.py
        _v1_namespace = V1Namespace(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
        )
        return _v1_namespace

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1Namespace]:
        """Returns the "Active" Namespace from the cluster"""

        _active_ns: Optional[V1Namespace] = None
        _active_nss: Optional[List[V1Namespace]] = self.read_from_cluster(
            k8s_api=k8s_api,
        )
        # logger.debug(f"_active_nss: {_active_nss}")
        if _active_nss is None:
            return None

        _active_nss_dict = {_ns.metadata.name: _ns for _ns in _active_nss}

        _ns_name = self.get_resource_name()
        if _ns_name in _active_nss_dict:
            _active_ns = _active_nss_dict[_ns_name]
            self.__setattr__("v1_namespace", _active_ns)
            # logger.debug(f"Found {_ns_name}")
        return _active_ns

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1Namespace]]:
        """Reads Namespaces from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # logger.debug("Getting all Namespaces")
        ns_list: Optional[V1NamespaceList] = k8s_core_v1_api.list_namespace()

        namespaces: Optional[List[V1Namespace]] = None
        if ns_list:
            namespaces = [ns for ns in ns_list.items if ns.status.phase == "Active"]
        # logger.debug(f"namespaces: {namespaces}")
        # logger.debug(f"namespaces type: {type(namespaces)}")

        return namespaces

    def _create(self, k8s_api: K8sApi) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1Namespace = self.get_k8s_object()
        v1_namespace: V1Namespace = k8s_core_v1_api.create_namespace(body=_k8s_object)
        # logger.debug("Created:\n{}".format(pformat(v1_namespace.to_dict(), indent=2)))
        if v1_namespace.status.phase == "Active":
            logger.debug("Namespace Created")
            self.__setattr__("v1_namespace", v1_namespace)
            return True
        logger.error("Namespace could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _ns_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_ns_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_core_v1_api.delete_namespace(name=_ns_name)
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("Namespace Deleted")
            self.__setattr__("v1_namespace", None)
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
        _ns_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_ns_name))

        _k8s_object: V1Namespace = self.get_k8s_object()
        v1_namespace: V1Namespace = k8s_core_v1_api.patch_namespace(
            name=_ns_name, body=_k8s_object
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_namespace.to_dict(), indent=2)))
        if v1_namespace.metadata.creation_timestamp is not None:
            logger.debug("Namespace Updated")
            self.__setattr__("v1_namespace", v1_namespace)
            return True
        logger.error("Namespace could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        # logger.info(f"Checking if {self.get_resource_name()} is active")
        _active_ns: Optional[V1Namespace] = self.get_active_k8s_object(
            k8s_api=k8s_api,
        )
        if _active_ns:
            return True
        return False

    def create_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        only_if_not_active: Optional[bool] = True,
    ) -> bool:

        if only_if_not_active and self.is_active_on_cluster(k8s_api):
            logger.debug(
                f"Namespace {self.get_resource_name()} is already active, skipping create"
            )
            return True
        return self._create(k8s_api)

    def delete_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._delete(k8s_api)
        logger.debug(
            f"Namespace {self.get_resource_name()} does not exist, skipping delete"
        )
        return True

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._update(k8s_api)
        logger.debug(
            f"Namespace {self.get_resource_name()} does not exist, skipping update"
        )
        return True
