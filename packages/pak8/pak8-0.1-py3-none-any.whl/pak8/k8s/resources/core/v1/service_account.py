from typing import List, Optional

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_service_account import V1ServiceAccount
from kubernetes.client.models.v1_service_account_list import V1ServiceAccountList
from kubernetes.client.models.v1_status import V1Status
from pydantic import Field

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.core.v1.local_object_reference import LocalObjectReference
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class ServiceAccount(K8sResourceBase):
    """Pak8 representation of a K8s Service Account.
    A service account provides an identity for processes that run in a Pod.
    When you create a pod, if you do not specify a service account, it is automatically assigned the default service account in the same namespace.

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#serviceaccount-v1-core
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service_account.py
    """

    image_pull_secrets: Optional[List[LocalObjectReference]] = Field(
        None, alias="imagePullSecrets"
    )
    # V1ServiceAccount object received as the output after creating the sa
    v1_service_account: Optional[V1ServiceAccount] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["image_pull_secrets"]

    def get_k8s_object(self) -> V1ServiceAccount:
        """Creates a body for this ServiceAccount"""

        # Return a V1ServiceAccount object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_service_account.py
        _image_pull_secrets = None
        if self.image_pull_secrets:
            _image_pull_secrets = []
            for ips in self.image_pull_secrets:
                _image_pull_secrets.append(ips.get_k8s_object())

        _v1_service_account = V1ServiceAccount(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            image_pull_secrets=_image_pull_secrets,
        )
        return _v1_service_account

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1ServiceAccount]:
        """Returns the "Active" ServiceAccount from the cluster"""

        _active_sa: Optional[V1ServiceAccount] = None
        _active_sas: Optional[List[V1ServiceAccount]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_sas: {_active_sas}")
        if _active_sas is None:
            return None

        _active_sas_dict = {_sa.metadata.name: _sa for _sa in _active_sas}

        _sa_name = self.get_resource_name()
        if _sa_name in _active_sas_dict:
            _active_sa = _active_sas_dict[_sa_name]
            self.__setattr__("v1_service_account", _active_sa)
            # logger.debug(f"Found {_sa_name}")
        return _active_sa

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1ServiceAccount]]:
        """Reads ServiceAccounts from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        sa_list: Optional[V1ServiceAccountList] = None
        if namespace:
            # logger.debug(f"Getting SAs for ns: {namespace}")
            sa_list = k8s_core_v1_api.list_namespaced_service_account(
                namespace=namespace
            )
        else:
            # logger.debug("Getting SAs for all namespaces")
            sa_list = k8s_core_v1_api.list_service_account_for_all_namespaces()

        sas: Optional[List[V1ServiceAccount]] = None
        if sa_list:
            sas = sa_list.items
        # logger.debug(f"sas: {sas}")
        # logger.debug(f"sas type: {type(sas)}")

        return sas

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1ServiceAccount = self.get_k8s_object()
        v1_service_account: V1ServiceAccount = (
            k8s_core_v1_api.create_namespaced_service_account(
                namespace=namespace, body=_k8s_object
            )
        )
        # logger.debug("Created:\n{}".format(pformat(v1_service_account.to_dict(), indent=2)))
        if v1_service_account.metadata.creation_timestamp is not None:
            logger.debug("ServiceAccount Created")
            self.__setattr__("v1_service_account", v1_service_account)
            return True
        logger.error("ServiceAccount could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _sa_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_sa_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_core_v1_api.delete_namespaced_service_account(
            name=_sa_name, namespace=namespace
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("ServiceAccount Deleted")
            self.__setattr__("v1_service_account", None)
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
        _sa_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_sa_name))

        _k8s_object: V1ServiceAccount = self.get_k8s_object()
        v1_service_account: V1ServiceAccount = (
            k8s_core_v1_api.patch_namespaced_service_account(
                name=_sa_name, namespace=namespace, body=_k8s_object
            )
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_service_account.to_dict(), indent=2)))
        if v1_service_account.metadata.creation_timestamp is not None:
            logger.debug("ServiceAccount Updated")
            self.__setattr__("v1_service_account", v1_service_account)
            return True
        logger.error("ServiceAccount could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_sa: Optional[V1ServiceAccount] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_sa:
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
                f"ServiceAccount {self.get_resource_name()} is already active, skipping create"
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
            f"ServiceAccount {self.get_resource_name()} does not exist, skipping delete"
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
            f"ServiceAccount {self.get_resource_name()} does not exist, skipping update"
        )
        return True
