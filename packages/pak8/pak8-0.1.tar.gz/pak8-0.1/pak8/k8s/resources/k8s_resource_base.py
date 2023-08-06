import itertools
import json
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta
from pak8.utils.log import logger


class K8sResourceBase(BaseModel):
    """Base class for all K8s Resources. All Models in the pak8.k8s.resources module are
    expected to be subclasses of this Model.
    """

    # Shared attributes for all K8s Resources
    api_version: k8s_enums.ApiVersion = Field(..., alias="apiVersion")
    kind: k8s_enums.Kind
    metadata: ObjectMeta

    # List of attributes to include from the K8sResourceBase class when generating the
    # K8s manifest. Subclasses must define the attributes_for_k8s_manifest list
    base_attributes_for_k8s_manifest: List[str] = [
        "api_version",
        "apiVersion",
        "kind",
        "metadata",
    ]
    # List of attributes to include from Subclasses
    # This should be defined by the Subclass
    attributes_for_k8s_manifest: List[str] = []

    def get_resource_name(self) -> str:
        return self.metadata.name

    def get_label_selector(self) -> str:
        labels = self.metadata.labels
        label_str = ",".join([f"{k}={v}" for k, v in labels.items()])
        return label_str

    def get_k8s_object(self) -> Any:
        """Creates a K8sObject for this resource.
        Eg:
            * For a Deployment resource, it will return the V1Deployment object.
        """
        logger.error("@get_k8s_object method not defined")

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Any:
        """Returns the "Active" K8sObject from the cluster.
        Eg:
            * For a Deployment resource, it will return the V1Deployment object
            currently running on the cluster.
        """
        logger.error("@get_active_k8s_object method not defined")

    def get_k8s_manifest_dict(self) -> Optional[Dict[str, Any]]:
        """Returns the K8s Manifest for this Object as a dict"""

        _k8s_manifest: Dict[str, Any] = {}
        _all_attributes: Dict[str, Any] = self.dict(
            exclude_defaults=True, by_alias=True
        )
        # logger.debug("All Attributes: {}".format(_all_attributes))
        for _attr_name in itertools.chain(
            self.base_attributes_for_k8s_manifest, self.attributes_for_k8s_manifest
        ):
            if _attr_name in _all_attributes:
                _k8s_manifest[_attr_name] = _all_attributes[_attr_name]
        # logger.debug(f"k8s_manifest:\n{_k8s_manifest}")
        return _k8s_manifest

    def get_k8s_manifest_yaml(self) -> Optional[str]:
        """Returns the K8s Manifest for this Object as a yaml"""
        _dict = self.get_k8s_manifest_dict()
        if _dict:
            return yaml.safe_dump(_dict)
        return None

    def get_k8s_manifest_json(self, **kwargs) -> Optional[str]:
        """Returns the K8s Manifest for this Object as a json"""
        _dict = self.get_k8s_manifest_dict()
        if _dict:
            return json.dumps(_dict, **kwargs)
        return None

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs
    ) -> Any:
        logger.error("@get_from_cluster method not defined")

    def debug(self) -> None:
        logger.error("@debug method not defined")

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:
        """Returns True if the resource is active on the K8s Cluster"""
        logger.error("@is_active_on_cluster method not defined")
        return False

    def create_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        only_if_not_active: Optional[bool] = True,
    ) -> bool:
        """Applies the resource to the K8s Cluster

        Args:
            k8s_api: An instance of K8sApi which connects to the active K8s Cluster
            namespace: Apply this resource under this namespace
            only_if_not_active: If True, apply only if an existing Active resource with the same name does not exists
        """
        logger.error("@create_if method not defined")
        return False

    def delete_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:
        """Deletes the resource from the K8s Cluster"""
        logger.error("@delete_if method not defined")
        return False

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:
        """Updates the resource on the K8s Cluster"""
        logger.error("@update_if method not defined")
        return False

    class Config:
        # https://pydantic-docs.helpmanual.io/usage/model_config/
        # If we need to use an alias for fields of subclasses, eg: Kubeconfig
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True

        # @classmethod
        # def alias_generator(cls, field_name: str) -> str:
        #     return field_name
