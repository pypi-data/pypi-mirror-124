from pprint import pformat
from typing import List, Optional

from kubernetes.client import ApiextensionsV1beta1Api
from kubernetes.client.models.v1_status import V1Status
from kubernetes.client.models.v1beta1_custom_resource_definition import (
    V1beta1CustomResourceDefinition,
)
from kubernetes.client.models.v1beta1_custom_resource_definition_list import (
    V1beta1CustomResourceDefinitionList,
)

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition_spec import (
    CustomResourceDefinitionSpec,
)
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class CustomResourceDefinition(K8sResourceBase):
    """Pak8 representation of a K8s CustomResourceDefinition

    References:
        * Doc: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#storageclass-v1-storage-k8s-io
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition.py
    """

    spec: CustomResourceDefinitionSpec

    # V1beta1CustomResourceDefinition object received as the output after creating the crd
    v1beta1_custom_resource_definition: Optional[V1beta1CustomResourceDefinition] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["spec"]

    def get_k8s_object(self) -> V1beta1CustomResourceDefinition:
        """Creates a body for this CustomResourceDefinition"""

        # Return a V1beta1CustomResourceDefinition object to create a CustomResourceDefinition
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition.py
        _v1beta1_custom_resource_definition = V1beta1CustomResourceDefinition(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            spec=self.spec.get_k8s_object(),
        )
        return _v1beta1_custom_resource_definition

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1beta1CustomResourceDefinition]:
        """Returns the "Active" CustomResourceDefinition from the cluster"""

        _active_crd: Optional[V1beta1CustomResourceDefinition] = None
        _active_crds: Optional[
            List[V1beta1CustomResourceDefinition]
        ] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_crds: {_active_crds}")
        if _active_crds is None:
            return None

        _active_crds_dict = {_crd.metadata.name: _crd for _crd in _active_crds}

        _crd_name = self.get_resource_name()
        if _crd_name in _active_crds_dict:
            _active_crd = _active_crds_dict[_crd_name]
            self.__setattr__("v1beta1_custom_resource_definition", _active_crd)
            # logger.debug(f"Found {_crd_name}")
        return _active_crd

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1beta1CustomResourceDefinition]]:
        """Reads CRDs from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_apiextensions_v1beta1_api: ApiextensionsV1beta1Api = (
            k8s_api.k8s_apiextensions_v1beta1_api
        )
        crd_list: Optional[
            V1beta1CustomResourceDefinitionList
        ] = k8s_apiextensions_v1beta1_api.list_custom_resource_definition()
        crds: Optional[List[V1beta1CustomResourceDefinition]] = None
        if crd_list:
            crds = crd_list.items
            # logger.debug(f"crds: {crds}")
            # logger.debug(f"crds type: {type(crds)}")
        return crds

    def _create(self, k8s_api: K8sApi) -> bool:
        """Creates a CRD

        Known Issues:
            * https://github.com/kubernetes-client/python/issues/415
        """

        k8s_apiextensions_v1beta1_api: ApiextensionsV1beta1Api = (
            k8s_api.k8s_apiextensions_v1beta1_api
        )
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1beta1CustomResourceDefinition = self.get_k8s_object()
        try:
            v1beta1_custom_resource_definition: V1beta1CustomResourceDefinition = (
                k8s_apiextensions_v1beta1_api.create_custom_resource_definition(
                    body=_k8s_object
                )
            )
            logger.debug(
                "Created:\n{}".format(
                    pformat(v1beta1_custom_resource_definition.to_dict(), indent=2)
                )
            )
        except ValueError as e:
            # This is a K8s bug. Ref: https://github.com/kubernetes-client/python/issues/1022
            logger.info("Encountered known K8s bug. Exception: {}".format(e))

        # TODO: Update when K8s bug is fixed
        return True

    def _delete(
        self,
        k8s_api: K8sApi,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_apiextensions_v1beta1_api: ApiextensionsV1beta1Api = (
            k8s_api.k8s_apiextensions_v1beta1_api
        )
        # TODO: Implement wait_for_termination
        _crd_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_crd_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = (
            k8s_apiextensions_v1beta1_api.delete_custom_resource_definition(
                name=_crd_name
            )
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("CRD Deleted")
            self.__setattr__("v1beta1_custom_resource_definition", None)
            return True
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_crd: Optional[
            V1beta1CustomResourceDefinition
        ] = self.get_active_k8s_object(k8s_api, namespace)
        if _active_crd:
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
                f"CRD {self.get_resource_name()} is already active, skipping create"
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
        logger.debug(f"CRD {self.get_resource_name()} does not exist, skipping delete")
        return True
