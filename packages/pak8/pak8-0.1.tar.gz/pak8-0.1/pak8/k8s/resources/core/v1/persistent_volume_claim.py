from typing import List, Optional

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_persistent_volume_claim import V1PersistentVolumeClaim
from kubernetes.client.models.v1_persistent_volume_claim_list import (
    V1PersistentVolumeClaimList,
)
from kubernetes.client.models.v1_status import V1Status

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.core.v1.persistent_volume_claim_spec import (
    PersistentVolumeClaimSpec,
)
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class PersistentVolumeClaim(K8sResourceBase):
    """Pak8 representation of a K8s PersistentVolumeClaim
    A PersistentVolumeClaim (PVC) is a request for storage by a user.
    It is similar to a Pod. Pods consume node resources and PVCs consume PV resources.
    A PersistentVolume (PV) is a piece of storage in the cluster that has been provisioned
    by an administrator or dynamically provisioned using Storage Classes.
    With Pak8, we prefer to use Storage Classes, read more about Dynamic provisioning here: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#dynamic

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#persistentvolumeclaim-v1-core
            https://kubernetes.io/docs/concepts/storage/persistent-volumes/
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim.py
    """

    spec: PersistentVolumeClaimSpec

    # V1PersistentVolumeClaim object received as the output after creating the pvc
    v1_persistent_volume_claim: Optional[V1PersistentVolumeClaim] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["spec"]

    def get_k8s_object(self) -> V1PersistentVolumeClaim:
        """Creates a body for this PVC"""

        # Return a V1PersistentVolumeClaim object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim.py
        _v1_persistent_volume_claim = V1PersistentVolumeClaim(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            spec=self.spec.get_k8s_object(),
        )
        return _v1_persistent_volume_claim

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1PersistentVolumeClaim]:
        """Returns the "Active" PVC from the cluster"""

        _active_pvc: Optional[V1PersistentVolumeClaim] = None
        _active_pvcs: Optional[List[V1PersistentVolumeClaim]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_pvcs: {_active_pvcs}")
        if _active_pvcs is None:
            return None

        _active_pvcs_dict = {_pvc.metadata.name: _pvc for _pvc in _active_pvcs}

        _pvc_name = self.get_resource_name()
        if _pvc_name in _active_pvcs_dict:
            _active_pvc = _active_pvcs_dict[_pvc_name]
            self.__setattr__("v1_persistent_volume_claim", _active_pvc)
            # logger.debug(f"Found {_pvc_name}")
        return _active_pvc

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1PersistentVolumeClaim]]:
        """Reads PVCs from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        pvc_list: Optional[V1PersistentVolumeClaimList] = None
        if namespace:
            # logger.debug(f"Getting PVCs for ns: {namespace}")
            pvc_list = k8s_core_v1_api.list_namespaced_persistent_volume_claim(
                namespace=namespace
            )
        else:
            # logger.debug("Getting PVCs for all namespaces")
            pvc_list = k8s_core_v1_api.list_persistent_volume_claim_for_all_namespaces()

        pvcs: Optional[List[V1PersistentVolumeClaim]] = None
        if pvc_list:
            pvcs = pvc_list.items
        # logger.debug(f"pvcs: {pvcs}")
        # logger.debug(f"pvcs type: {type(pvcs)}")

        return pvcs

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1PersistentVolumeClaim = self.get_k8s_object()
        v1_persistent_volume_claim: V1PersistentVolumeClaim = (
            k8s_core_v1_api.create_namespaced_persistent_volume_claim(
                namespace=namespace, body=_k8s_object
            )
        )
        # logger.debug("Created:\n{}".format(pformat(v1_persistent_volume_claim.to_dict(), indent=2)))
        if v1_persistent_volume_claim.metadata.creation_timestamp is not None:
            logger.debug("PVC Created")
            self.__setattr__("v1_persistent_volume_claim", v1_persistent_volume_claim)
            return True
        logger.error("PVC could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _pvc_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_pvc_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = (
            k8s_core_v1_api.delete_namespaced_persistent_volume_claim(
                name=_pvc_name, namespace=namespace
            )
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("PVC Deleted")
            self.__setattr__("v1_persistent_volume_claim", None)
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
        _pvc_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_pvc_name))

        _k8s_object: V1PersistentVolumeClaim = self.get_k8s_object()
        v1_persistent_volume_claim: V1PersistentVolumeClaim = (
            k8s_core_v1_api.patch_namespaced_persistent_volume_claim(
                name=_pvc_name, namespace=namespace, body=_k8s_object
            )
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_persistent_volume_claim.to_dict(), indent=2)))
        if v1_persistent_volume_claim.metadata.creation_timestamp is not None:
            logger.debug("PVC Updated")
            self.__setattr__("v1_persistent_volume_claim", v1_persistent_volume_claim)
            return True
        logger.error("PVC could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_pvc: Optional[V1PersistentVolumeClaim] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_pvc:
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
                f"PVC {self.get_resource_name()} is already active, skipping create"
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
        logger.debug(f"PVC {self.get_resource_name()} does not exist, skipping delete")
        return True

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._update(k8s_api, namespace)
        logger.debug(f"PVC {self.get_resource_name()} does not exist, skipping update")
        return True
