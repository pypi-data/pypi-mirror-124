from typing import List, Optional

from kubernetes.client.models.v1beta1_custom_resource_definition_names import (
    V1beta1CustomResourceDefinitionNames,
)
from kubernetes.client.models.v1beta1_custom_resource_definition_spec import (
    V1beta1CustomResourceDefinitionSpec,
)
from pydantic import BaseModel


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition_names.py
class CustomResourceDefinitionNames(BaseModel):
    kind: str
    plural: str
    singular: str

    def get_k8s_object(
        self,
    ) -> V1beta1CustomResourceDefinitionNames:

        # Return a V1beta1CustomResourceDefinitionNames object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition_names.py
        _v1beta1_custom_resource_definition_names = (
            V1beta1CustomResourceDefinitionNames(
                kind=self.kind,
                plural=self.plural,
                singular=self.singular,
            )
        )
        return _v1beta1_custom_resource_definition_names

    class Config:
        arbitrary_types_allowed = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition_spec.py
class CustomResourceDefinitionSpec(BaseModel):
    group: str
    names: CustomResourceDefinitionNames
    scope: str
    version: str

    v1beta1_custom_resource_definition_spec: Optional[
        V1beta1CustomResourceDefinitionSpec
    ] = None

    def get_k8s_object(
        self,
    ) -> V1beta1CustomResourceDefinitionSpec:

        # Return a V1beta1CustomResourceDefinitionSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1beta1_custom_resource_definition_spec.py
        _v1beta1_custom_resource_definition_spec = V1beta1CustomResourceDefinitionSpec(
            group=self.group,
            names=self.names.get_k8s_object(),
            scope=self.scope,
            version=self.version,
        )
        return _v1beta1_custom_resource_definition_spec

    class Config:
        arbitrary_types_allowed = True
