from typing import Dict, List, Optional

from kubernetes.client import StorageV1Api
from kubernetes.client.models.v1_status import V1Status
from kubernetes.client.models.v1_storage_class import V1StorageClass
from kubernetes.client.models.v1_storage_class_list import V1StorageClassList

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class StorageClass(K8sResourceBase):
    """Pak8 representation of a K8s StorageClass

    References:
        * Doc: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#storageclass-v1-storage-k8s-io
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_storage_class.py
    """

    provisioner: str
    parameters: Dict[str, str]
    # V1StorageClass object received as the output after creating the storage_class
    v1_storage_class: Optional[V1StorageClass] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["provisioner", "parameters"]

    def get_k8s_object(self) -> V1StorageClass:
        """Creates a body for this StorageClass"""

        # Return a V1StorageClass object to create a StorageClass
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_storage_class.py
        _v1_storage_class = V1StorageClass(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            provisioner=self.provisioner,
            parameters=self.parameters,
        )

        return _v1_storage_class

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1StorageClass]:
        """Returns the "Active" StorageClass from the cluster"""

        _active_sc: Optional[V1StorageClass] = None
        _active_scs: Optional[List[V1StorageClass]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_scs: {_active_scs}")
        if _active_scs is None:
            return None

        _active_scs_dict = {_sc.metadata.name: _sc for _sc in _active_scs}

        _sc_name = self.get_resource_name()
        if _sc_name in _active_scs_dict:
            _active_sc = _active_scs_dict[_sc_name]
            self.__setattr__("v1_storage_class", _active_sc)
            # logger.debug(f"Found {_sc_name}")
        return _active_sc

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1StorageClass]]:
        """Reads SCs from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_storage_v1_api: StorageV1Api = k8s_api.k8s_storage_v1_api
        sc_list: Optional[V1StorageClassList] = k8s_storage_v1_api.list_storage_class()
        scs: Optional[List[V1StorageClass]] = None
        if sc_list:
            scs = sc_list.items
            # logger.debug(f"scs: {scs}")
            # logger.debug(f"scs type: {type(scs)}")
        return scs

    def _create(self, k8s_api: K8sApi) -> bool:

        k8s_storage_v1_api: StorageV1Api = k8s_api.k8s_storage_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1StorageClass = self.get_k8s_object()
        v1_storage_class: V1StorageClass = k8s_storage_v1_api.create_storage_class(
            body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_storage_class.to_dict(), indent=2)))
        if v1_storage_class.metadata.creation_timestamp is not None:
            logger.debug("SC Created")
            self.__setattr__("v1_storage_class", v1_storage_class)
            return True
        logger.error("SC could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_storage_v1_api: StorageV1Api = k8s_api.k8s_storage_v1_api
        # TODO: Implement wait_for_termination
        _sc_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_sc_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_storage_v1_api.delete_storage_class(
            name=_sc_name
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("SC Deleted")
            self.__setattr__("v1_storage_class", None)
            return True
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_sc: Optional[V1StorageClass] = self.get_active_k8s_object(
            k8s_api, namespace
        )
        if _active_sc:
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
                f"SC {self.get_resource_name()} is already active, skipping create"
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
        logger.debug(f"SC {self.get_resource_name()} does not exist, skipping delete")
        return True
