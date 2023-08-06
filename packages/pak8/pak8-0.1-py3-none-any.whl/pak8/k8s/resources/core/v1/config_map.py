from typing import Any, Dict, List, Optional

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_config_map import V1ConfigMap
from kubernetes.client.models.v1_config_map_list import V1ConfigMapList
from kubernetes.client.models.v1_status import V1Status

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class ConfigMap(K8sResourceBase):
    """Pak8 representation of a K8s ConfigMap
    ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable.
    In short, they store configs. For config variables which contain sensitive info, use Secrets.

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#configmap-v1-core
            https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_config_map.py
    """

    data: Dict[str, Any]

    # V1ConfigMap object received as the output after creating the cm
    v1_config_map: Optional[V1ConfigMap] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["data"]

    def get_k8s_object(self) -> V1ConfigMap:
        """Creates a body for this ConfigMap"""

        # Return a V1ConfigMap object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_config_map.py
        _v1_config_map = V1ConfigMap(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            data=self.data,
        )
        return _v1_config_map

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1ConfigMap]:
        """Returns the "Active" ConfigMap from the cluster"""

        _active_cm: Optional[V1ConfigMap] = None
        _active_cms: Optional[List[V1ConfigMap]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_cms: {_active_cms}")
        if _active_cms is None:
            return None

        _active_cms_dict = {_cm.metadata.name: _cm for _cm in _active_cms}

        _cm_name = self.get_resource_name()
        if _cm_name in _active_cms_dict:
            _active_cm = _active_cms_dict[_cm_name]
            self.__setattr__("v1_config_map", _active_cm)
            # logger.debug(f"Found {_cm_name}")
        return _active_cm

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1ConfigMap]]:
        """Reads ConfigMaps from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        cm_list: Optional[V1ConfigMapList] = None
        if namespace:
            # logger.debug(f"Getting CMs for ns: {namespace}")
            cm_list = k8s_core_v1_api.list_namespaced_config_map(namespace=namespace)
        else:
            # logger.debug("Getting CMs for all namespaces")
            cm_list = k8s_core_v1_api.list_config_map_for_all_namespaces()

        config_maps: Optional[List[V1ConfigMap]] = None
        if cm_list:
            config_maps = cm_list.items
        # logger.debug(f"config_maps: {config_maps}")
        # logger.debug(f"config_maps type: {type(config_maps)}")

        return config_maps

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1ConfigMap = self.get_k8s_object()
        v1_config_map: V1ConfigMap = k8s_core_v1_api.create_namespaced_config_map(
            namespace=namespace, body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_config_map.to_dict(), indent=2)))
        if v1_config_map.metadata.creation_timestamp is not None:
            logger.debug("ConfigMap Created")
            self.__setattr__("v1_config_map", v1_config_map)
            return True
        logger.error("ConfigMap could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _cm_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_cm_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_core_v1_api.delete_namespaced_config_map(
            name=_cm_name, namespace=namespace
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("ConfigMap Deleted")
            self.__setattr__("v1_config_map", None)
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
        _cm_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_cm_name))

        _k8s_object: V1ConfigMap = self.get_k8s_object()
        v1_config_map: V1ConfigMap = k8s_core_v1_api.patch_namespaced_config_map(
            name=_cm_name, namespace=namespace, body=_k8s_object
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_config_map.to_dict(), indent=2)))
        if v1_config_map.metadata.creation_timestamp is not None:
            logger.debug("ConfigMap Updated")
            self.__setattr__("v1_config_map", v1_config_map)
            return True
        logger.error("ConfigMap could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_cm: Optional[V1ConfigMap] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_cm:
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
                f"ConfigMap {self.get_resource_name()} is already active, skipping create"
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
            f"ConfigMap {self.get_resource_name()} does not exist, skipping delete"
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
            f"ConfigMap {self.get_resource_name()} does not exist, skipping update"
        )
        return True
