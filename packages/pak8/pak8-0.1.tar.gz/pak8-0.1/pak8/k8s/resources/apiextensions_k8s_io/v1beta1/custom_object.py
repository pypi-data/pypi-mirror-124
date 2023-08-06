from typing import Any, Dict, List, Optional

from kubernetes.client import CustomObjectsApi
from kubernetes.client.models.v1_delete_options import V1DeleteOptions

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.utils.log import logger


class CustomObject(K8sResourceBase):
    """Pak8 representation of a K8s CustomObject.
    The CustomResourceDefinition must be created before creating this object.
    When creating a CustomObject, provide the spec and generate the object body using
        get_k8s_object()

    References:
        * https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/CustomObjectsApi.md
        * https://github.com/kubernetes-client/python/blob/master/examples/custom_object.py
    """

    spec: Optional[Dict[str, Any]] = None

    # Helper Attributes for the CustomObject
    group: str
    version: str
    plural: str

    # CustomObject received as the output after creating the custom object
    custom_object: Optional[Dict[str, Any]] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["spec"]

    def get_k8s_object(self) -> Dict[str, Any]:
        """Creates a body for this CustomObject"""

        _body = {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": self.metadata.get_k8s_object().to_dict(),
            "spec": self.spec,
        }
        return _body

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Returns the "Active" CustomObject from the cluster"""

        _active_custom_object: Optional[Dict[str, Any]] = None
        _active_custom_objects: Optional[List[Dict[str, Any]]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
            group=self.group,
            version=self.version,
            plural=self.plural,
        )
        # logger.debug(f"_active_custom_objects: {_active_custom_objects}")
        if _active_custom_objects is None:
            return None

        _active_custom_objects_dict = {
            _custom_object.get("metadata", {}).get("name", None): _custom_object
            for _custom_object in _active_custom_objects
        }

        _custom_object_name = self.get_resource_name()
        if _custom_object_name in _active_custom_objects_dict:
            _active_custom_object = _active_custom_objects_dict[_custom_object_name]
            self.__setattr__("custom_object", _active_custom_object)
            # logger.debug(f"Found {_custom_object_name}")
        return _active_custom_object

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[Dict[str, Any]]]:
        """Reads CustomObject from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        if "group" not in kwargs:
            logger.error("No Group provided")
            return None
        if "version" not in kwargs:
            logger.error("No Version provided")
            return None
        if "plural" not in kwargs:
            logger.error("No Plural provided")
            return None

        group = kwargs["group"]
        version = kwargs["version"]
        plural = kwargs["plural"]

        k8s_custom_objects_api: CustomObjectsApi = k8s_api.k8s_custom_objects_api
        custom_object_list: Optional[Dict[str, Any]] = None
        if namespace:
            # logger.debug(
            #     f"Getting CustomObjects for:\n\tNS: {namespace}\n\tGroup: {group}\n\tVersion: {version}\n\tPlural: {plural}"
            # )
            custom_object_list = k8s_custom_objects_api.list_namespaced_custom_object(
                group=group,
                version=version,
                namespace=namespace,
                plural=plural,
            )
        else:
            # logger.debug(
            #     f"Getting CustomObjects for:\n\tGroup: {group}\n\tVersion: {version}\n\tPlural: {plural}"
            # )
            custom_object_list = k8s_custom_objects_api.list_cluster_custom_object(
                group=group,
                version=version,
                plural=plural,
            )
        custom_objects: Optional[List[Dict[str, Any]]] = None
        # logger.debug(f"custom_object_list: {custom_object_list}")
        # logger.debug(f"custom_object_list type: {type(custom_object_list)}")
        if custom_object_list:
            custom_objects = custom_object_list.get("items", None)
            # logger.debug(f"custom_objects: {custom_objects}")
            # logger.debug(f"custom_objects type: {type(custom_objects)}")
        return custom_objects

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_custom_objects_api: CustomObjectsApi = k8s_api.k8s_custom_objects_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: Dict[str, Any] = self.get_k8s_object()
        _custom_object: Dict[
            str, Any
        ] = k8s_custom_objects_api.create_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            body=_k8s_object,
        )
        # logger.debug("Created:\n{}".format(pformat(_custom_object, indent=2)))
        if (
            _custom_object.get("metadata", {}).get("creationTimestamp", None)
            is not None
        ):
            logger.debug("CustomObject Created")
            self.__setattr__("custom_object", _custom_object)
            return True
        logger.error("CustomObject could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_custom_objects_api: CustomObjectsApi = k8s_api.k8s_custom_objects_api
        # TODO: Implement wait_for_termination
        _custom_object_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_custom_object_name))

        _delete_options = V1DeleteOptions()
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: Dict[
            str, Any
        ] = k8s_custom_objects_api.delete_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=_custom_object_name,
            body=_delete_options,
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.get("status", None) == "Success":
            logger.debug("CustomObject Deleted")
            self.__setattr__("custom_object", None)
            return True
        return False

    def _update(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_completion: Optional[bool] = False,
    ) -> bool:

        k8s_custom_objects_api: CustomObjectsApi = k8s_api.k8s_custom_objects_api
        # TODO: Implement wait_for_completion
        _custom_object_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_custom_object_name))

        _k8s_object: Dict[str, Any] = self.get_k8s_object()
        _custom_object: Dict[
            str, Any
        ] = k8s_custom_objects_api.patch_namespaced_custom_object(
            group=self.group,
            version=self.version,
            namespace=namespace,
            plural=self.plural,
            name=_custom_object_name,
            body=_k8s_object,
        )
        # logger.debug("Updated:\n{}".format(pformat(_custom_object, indent=2)))
        if (
            _custom_object.get("metadata", {}).get("creationTimestamp", None)
            is not None
        ):
            logger.debug("CustomObject Updated")
            self.__setattr__("custom_object", _custom_object)
            return True
        logger.error("CustomObject could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_custom_object: Optional[Dict[str, Any]] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_custom_object:
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
                f"CustomObject {self.get_resource_name()} is already active, skipping create"
            )
            return True
        return self._create(k8s_api, namespace)

    def delete_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api, namespace):
            return self._delete(k8s_api, namespace)
        logger.debug(
            f"CustomObject {self.get_resource_name()} does not exist, skipping delete"
        )
        return True

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api, namespace):
            return self._update(k8s_api, namespace)
        logger.debug(
            f"CustomObject {self.get_resource_name()} does not exist, skipping update"
        )
        return True
