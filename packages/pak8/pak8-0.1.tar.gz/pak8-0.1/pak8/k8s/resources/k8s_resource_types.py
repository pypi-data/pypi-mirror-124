from collections import OrderedDict
from typing import Dict, List, Type, Union

from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_object import CustomObject
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
    CustomResourceDefinition,
)
from pak8.k8s.resources.apps.v1.deployment import Deployment
from pak8.k8s.resources.core.v1.config_map import ConfigMap
from pak8.k8s.resources.core.v1.namespace import Namespace
from pak8.k8s.resources.core.v1.persistent_volume_claim import PersistentVolumeClaim
from pak8.k8s.resources.core.v1.pod import Pod
from pak8.k8s.resources.core.v1.secret import Secret
from pak8.k8s.resources.core.v1.service import Service
from pak8.k8s.resources.core.v1.service_account import ServiceAccount
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluste_role_binding import (
    ClusterRoleBinding,
)
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluster_role import ClusterRole
from pak8.k8s.resources.storage_k8s_io.v1.storage_class import StorageClass

# Use this as a type for an object which can hold any K8s Resource
# See get_k8s_resources_from_group() function for an example
K8sResourceType = Union[
    CustomResourceDefinition,
    Namespace,
    Secret,
    ConfigMap,
    StorageClass,
    # PersistentVolume,
    PersistentVolumeClaim,
    ServiceAccount,
    ClusterRole,
    ClusterRoleBinding,
    # Role,
    # RoleBinding,
    Service,
    Pod,
    Deployment,
    # Ingress,
    CustomObject,
]

# Use this as an ordered list to iterate over all K8s Resource Classes
# This list is the order in which resources should be installed as well.
# Copied from https://github.com/helm/helm/blob/release-2.10/pkg/tiller/kind_sorter.go#L29
K8sResourceTypeList: List[Type[K8sResourceBase]] = [
    CustomResourceDefinition,
    Namespace,
    ServiceAccount,
    StorageClass,
    Secret,
    ConfigMap,
    # PersistentVolume,
    PersistentVolumeClaim,
    ClusterRoleBinding,
    ClusterRole,
    # Role,
    # RoleBinding,
    Service,
    Pod,
    Deployment,
    # Ingress,
    CustomObject,
]

# Map K8s resource alias' to their type
_k8s_resource_type_names: Dict[str, Type[K8sResourceBase]] = {
    k8s_type.__name__.lower(): k8s_type for k8s_type in K8sResourceTypeList
}
_k8s_resource_type_aliases: Dict[str, Type[K8sResourceBase]] = {
    "crd": CustomResourceDefinition,
    "ns": Namespace,
    "cm": ConfigMap,
    "sc": StorageClass,
    "pvc": PersistentVolumeClaim,
    "sa": ServiceAccount,
    "cr": ClusterRole,
    "crb": ClusterRoleBinding,
    "svc": Service,
    "deploy": Deployment,
}

K8sResourceAliasToTypeMap: Dict[str, Type[K8sResourceBase]] = dict(
    **_k8s_resource_type_names, **_k8s_resource_type_aliases
)

# Maps each K8sResource to an install weight
# lower weight K8sResource(s) get installed first
# i.e. Namespace is installed first, then Secret... and so on
K8sResourceInstallOrder: Dict[str, int] = OrderedDict(
    {
        resource_type.__name__: idx
        for idx, resource_type in enumerate(K8sResourceTypeList, start=1)
    }
)
