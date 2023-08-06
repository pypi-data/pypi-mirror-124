from typing import List, Optional

from kubernetes.client import RbacAuthorizationV1Api
from kubernetes.client.models.v1_cluster_role_binding import V1ClusterRoleBinding
from kubernetes.client.models.v1_cluster_role_binding_list import (
    V1ClusterRoleBindingList,
)
from kubernetes.client.models.v1_status import V1Status
from pydantic import Field

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.role_ref import RoleRef
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.subject import Subject
from pak8.utils.log import logger


class ClusterRoleBinding(K8sResourceBase):
    """Pak8 representation of a K8s ClusterRoleBinding

    References:
        * Doc: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#clusterrolebinding-v1-rbac-authorization-k8s-io
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role_binding_binding.py
    """

    role_ref: RoleRef = Field(..., alias="roleRef")
    subjects: List[Subject]
    # V1ClusterRoleBinding object received as the output after creating the crb
    v1_cluster_role_binding: Optional[V1ClusterRoleBinding] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["role_ref", "subjects"]

    def get_k8s_object(self) -> V1ClusterRoleBinding:
        """Creates a body for this ClusterRoleBinding"""

        # Return a V1ClusterRoleBinding object to create a ClusterRoleBinding
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role_binding.py
        subjects_list = None
        if self.subjects:
            subjects_list = []
            for subject in self.subjects:
                subjects_list.append(subject.get_k8s_object())

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_cluster_role_binding.py
        _v1_cluster_role_binding = V1ClusterRoleBinding(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            role_ref=self.role_ref.get_k8s_object(),
            subjects=subjects_list,
        )
        return _v1_cluster_role_binding

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1ClusterRoleBinding]:
        """Returns the "Active" ClusterRoleBinding from the cluster"""

        _active_crb: Optional[V1ClusterRoleBinding] = None
        _active_crbs: Optional[List[V1ClusterRoleBinding]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_crbs: {_active_crbs}")
        if _active_crbs is None:
            return None

        _active_crbs_dict = {_crb.metadata.name: _crb for _crb in _active_crbs}

        _crb_name = self.get_resource_name()
        if _crb_name in _active_crbs_dict:
            _active_crb = _active_crbs_dict[_crb_name]
            self.__setattr__("v1_cluster_role_binding", _active_crb)
            # logger.debug(f"Found {_crb_name}")
        return _active_crb

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1ClusterRoleBinding]]:
        """Reads CRBs from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        crb_list: Optional[
            V1ClusterRoleBindingList
        ] = k8s_rbac_auth_v1_api.list_cluster_role_binding()
        crbs: Optional[List[V1ClusterRoleBinding]] = None
        if crb_list:
            crbs = crb_list.items
            # logger.debug(f"crbs: {crbs}")
            # logger.debug(f"crbs type: {type(crbs)}")
        return crbs

    def _create(self, k8s_api: K8sApi) -> bool:

        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1ClusterRoleBinding = self.get_k8s_object()
        v1_cluster_role_binding: V1ClusterRoleBinding = (
            k8s_rbac_auth_v1_api.create_cluster_role_binding(body=_k8s_object)
        )
        # logger.debug("Created:\n{}".format(pformat(v1_cluster_role_binding.to_dict(), indent=2)))
        if v1_cluster_role_binding.metadata.creation_timestamp is not None:
            logger.debug("CRB Created")
            self.__setattr__("v1_cluster_role_binding", v1_cluster_role_binding)
            return True
        logger.error("CRB could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_rbac_auth_v1_api: RbacAuthorizationV1Api = k8s_api.k8s_rbac_auth_v1_api
        # TODO: Implement wait_for_termination
        _crb_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_crb_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_rbac_auth_v1_api.delete_cluster_role_binding(
            name=_crb_name
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("CRB Deleted")
            self.__setattr__("v1_cluster_role_binding", None)
            return True
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_crb: Optional[V1ClusterRoleBinding] = self.get_active_k8s_object(
            k8s_api, namespace
        )
        if _active_crb:
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
                f"CRB {self.get_resource_name()} is already active, skipping create"
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
        logger.debug(f"CRB {self.get_resource_name()} does not exist, skipping delete")
        return True
