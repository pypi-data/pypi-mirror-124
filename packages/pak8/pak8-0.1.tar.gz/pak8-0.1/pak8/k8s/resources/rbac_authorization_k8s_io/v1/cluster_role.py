from typing import List, Optional

from kubernetes.client import RbacAuthorizationV1Api
from kubernetes.client.models.v1_cluster_role import V1ClusterRole
from kubernetes.client.models.v1_cluster_role_list import V1ClusterRoleList
from kubernetes.client.models.v1_status import V1Status

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.policy_rule import PolicyRule
from pak8.utils.log import logger


class ClusterRole(K8sResourceBase):
    """Pak8 representation of a K8s ClusterRole

    References:
        * Doc: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#clusterrole-v1-rbac-authorization-k8s-io
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role.py
    """

    rules: Optional[List[PolicyRule]] = None
    # V1ClusterRole object received as the output after creating the cr
    v1_cluster_role: Optional[V1ClusterRole] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["rules"]

    def get_k8s_object(self) -> V1ClusterRole:
        """Creates a body for this ClusterRole"""

        # Return a V1ClusterRole object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role.py
        rules_list = None
        if self.rules:
            rules_list = []
            for rules in self.rules:
                rules_list.append(rules.get_k8s_object())

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role.py
        _v1_cluster_role = V1ClusterRole(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            rules=rules_list,
        )

        return _v1_cluster_role

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1ClusterRole]:
        """Returns the "Active" ClusterRole from the cluster"""

        _active_cr: Optional[V1ClusterRole] = None
        _active_crs: Optional[List[V1ClusterRole]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_crs: {_active_crs}")
        if _active_crs is None:
            return None

        _active_crs_dict = {_cr.metadata.name: _cr for _cr in _active_crs}

        _cr_name = self.get_resource_name()
        if _cr_name in _active_crs_dict:
            _active_cr = _active_crs_dict[_cr_name]
            self.__setattr__("v1_cluster_role", _active_cr)
            # logger.debug(f"Found {_cr_name}")
        return _active_cr

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1ClusterRole]]:
        """Reads CRs from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        cr_list: Optional[V1ClusterRoleList] = k8s_rbac_auth_v1_api.list_cluster_role()
        crs: Optional[List[V1ClusterRole]] = None
        if cr_list:
            crs = cr_list.items
            # logger.debug(f"crs: {crs}")
            # logger.debug(f"crs type: {type(crs)}")
        return crs

    def _create(self, k8s_api: K8sApi) -> bool:

        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1ClusterRole = self.get_k8s_object()
        v1_cluster_role: V1ClusterRole = k8s_rbac_auth_v1_api.create_cluster_role(
            body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_cluster_role.to_dict(), indent=2)))
        if v1_cluster_role.metadata.creation_timestamp is not None:
            logger.debug("CR Created")
            self.__setattr__("v1_cluster_role", v1_cluster_role)
            return True
        logger.error("CR could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        # TODO: Implement wait_for_termination
        _cr_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_cr_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_rbac_auth_v1_api.delete_cluster_role(
            name=_cr_name
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("CR Deleted")
            self.__setattr__("v1_cluster_role", None)
            return True
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_cr: Optional[V1ClusterRole] = self.get_active_k8s_object(
            k8s_api, namespace
        )
        if _active_cr:
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
                f"CR {self.get_resource_name()} is already active, skipping create"
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
        logger.debug(f"CR {self.get_resource_name()} does not exist, skipping delete")
        return True
