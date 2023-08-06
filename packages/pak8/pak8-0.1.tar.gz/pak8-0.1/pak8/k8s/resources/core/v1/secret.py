from typing import Any, Dict, List, Optional

from kubernetes.client import CoreV1Api
from kubernetes.client.models.v1_secret import V1Secret
from kubernetes.client.models.v1_secret_list import V1SecretList
from kubernetes.client.models.v1_status import V1Status
from pydantic import Field

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class Secret(K8sResourceBase):
    """Pak8 representation of a K8s Secret

    References:
        * Doc: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#secret-v1-core
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_secret.py
    """

    type: str
    data: Optional[Dict[str, Any]] = None
    string_data: Optional[Dict[str, Any]] = Field(None, alias="stringData")
    # V1Secret object received as the output after creating the cm
    v1_secret: Optional[V1Secret] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["type", "data", "string_data"]

    def get_k8s_object(self) -> V1Secret:
        """Creates a body for this Secret"""

        # Return a V1Secret object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_secret.py
        _v1_secret = V1Secret(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            data=self.data,
            string_data=self.string_data,
            type=self.type,
        )
        return _v1_secret

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1Secret]:
        """Returns the "Active" Secret from the cluster"""

        _active_secret: Optional[V1Secret] = None
        _active_secrets: Optional[List[V1Secret]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_secrets: {_active_secrets}")
        if _active_secrets is None:
            return None

        _active_secrets_dict = {
            _secret.metadata.name: _secret for _secret in _active_secrets
        }

        _secret_name = self.get_resource_name()
        if _secret_name in _active_secrets_dict:
            _active_secret = _active_secrets_dict[_secret_name]
            self.__setattr__("v1_secret", _active_secret)
            # logger.debug(f"Found {_secret_name}")
        return _active_secret

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1Secret]]:
        """Reads Secrets from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        secret_list: Optional[V1SecretList] = None
        if namespace:
            # logger.debug(f"Getting Secrets for ns: {namespace}")
            secret_list = k8s_core_v1_api.list_namespaced_secret(namespace=namespace)
        else:
            # logger.debug("Getting Secrets for all namespaces")
            secret_list = k8s_core_v1_api.list_secret_for_all_namespaces()

        secrets: Optional[List[V1Secret]] = None
        if secret_list:
            secrets = secret_list.items
        # logger.debug(f"secrets: {secrets}")
        # logger.debug(f"secrets type: {type(secrets)}")

        return secrets

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1Secret = self.get_k8s_object()
        v1_secret: V1Secret = k8s_core_v1_api.create_namespaced_secret(
            namespace=namespace, body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_secret.to_dict(), indent=2)))
        if v1_secret.metadata.creation_timestamp is not None:
            logger.debug("Secret Created")
            self.__setattr__("v1_secret", v1_secret)
            return True
        logger.error("Secret could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_core_v1_api: CoreV1Api = k8s_api.k8s_core_v1_api
        # TODO: Implement wait_for_termination
        _secret_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_secret_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_core_v1_api.delete_namespaced_secret(
            name=_secret_name, namespace=namespace
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("Secret Deleted")
            self.__setattr__("v1_secret", None)
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
        _secret_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_secret_name))

        _k8s_object: V1Secret = self.get_k8s_object()
        v1_secret: V1Secret = k8s_core_v1_api.patch_namespaced_secret(
            name=_secret_name, namespace=namespace, body=_k8s_object
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_secret.to_dict(), indent=2)))
        if v1_secret.metadata.creation_timestamp is not None:
            logger.debug("Secret Updated")
            self.__setattr__("v1_secret", v1_secret)
            return True
        logger.error("Secret could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_secret: Optional[V1Secret] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_secret:
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
                f"Secret {self.get_resource_name()} is already active, skipping create"
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
            f"Secret {self.get_resource_name()} does not exist, skipping delete"
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
            f"Secret {self.get_resource_name()} does not exist, skipping update"
        )
        return True
