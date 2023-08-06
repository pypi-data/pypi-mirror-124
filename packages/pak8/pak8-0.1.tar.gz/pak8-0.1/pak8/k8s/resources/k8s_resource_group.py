from typing import List, Optional, Dict

from pydantic import BaseModel

from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_object import CustomObject
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
    CustomResourceDefinition,
)
from pak8.k8s.resources.apps.v1.deployment import Deployment
from pak8.k8s.resources.core.v1.config_map import ConfigMap
from pak8.k8s.resources.core.v1.namespace import Namespace
from pak8.k8s.resources.core.v1.persistent_volume_claim import PersistentVolumeClaim
from pak8.k8s.resources.core.v1.secret import Secret
from pak8.k8s.resources.core.v1.service import Service
from pak8.k8s.resources.core.v1.service_account import ServiceAccount
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluste_role_binding import (
    ClusterRoleBinding,
)
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluster_role import ClusterRole
from pak8.k8s.resources.storage_k8s_io.v1.storage_class import StorageClass


class K8sResourceGroup(BaseModel):
    """This Class contains all the instructions on how to deploy K8s resources."""

    name: str
    enabled: bool

    # The weight variable controls how this is resource group is deployed to a cluster
    # relative to other resource groups.

    # Within each resource group, different types of resources are
    # deployed in a predefined order (eg: ns first, then sa and so on..)
    # but we can also add an order to how to deploy different resource groups.
    # (Eg if we want to deploy a resource group with just storage_class (s) before all other resources)

    # Weights 1-10 are reserved
    # Weight 100 is default.
    # ResourceGroups with weight 100 are the default resources.
    # Choose weight 11-99 to deploy a resource group before all the default resources.
    # Choose weight 101+ to deploy a resource group after all the default resources
    weight: int = 100
    crd: Optional[List[CustomResourceDefinition]] = None
    ns: Optional[Namespace] = None
    sa: Optional[ServiceAccount] = None
    cr: Optional[ClusterRole] = None
    crb: Optional[ClusterRoleBinding] = None
    secret: Optional[List[Secret]] = None
    cm: Optional[List[ConfigMap]] = None
    storage_class: Optional[List[StorageClass]] = None
    pvc: Optional[List[PersistentVolumeClaim]] = None
    svc: Optional[List[Service]] = None
    deploy: Optional[List[Deployment]] = None
    custom_object: Optional[List[CustomObject]] = None


class CreateK8sResourceGroupData(BaseModel):
    namespace: str
    service_account_name: Optional[str] = None
    common_labels: Optional[Dict[str, str]] = None
