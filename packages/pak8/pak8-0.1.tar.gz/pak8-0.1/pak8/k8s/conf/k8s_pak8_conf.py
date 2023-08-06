from pathlib import Path
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, validator

from pak8.app import Pak8App
from pak8.k8s.api.apiextensions_k8s_io.v1beta1.custom_object import (
    CreateCustomObjectData,
    CreateCRDData,
)
from pak8.k8s.api.common.port import CreatePortData
from pak8.k8s.api.apps.v1.deployment import CreateDeploymentData
from pak8.k8s.api.core.v1.volume import CreateVolumeData
from pak8.k8s.api.core.v1.config_map import CreateConfigMapData
from pak8.k8s.api.core.v1.persistent_volume_claim import CreatePVCData
from pak8.k8s.api.core.v1.secret import CreateSecretData
from pak8.k8s.api.core.v1.service import CreateServiceData
from pak8.k8s.api.core.v1.service_account import CreateServiceAccountData
from pak8.k8s.api.rbac_authorization_k8s_io.v1.cluste_role_binding import (
    CreateClusterRoleBindingData,
)
from pak8.k8s.api.rbac_authorization_k8s_io.v1.cluster_role import CreateClusterRoleData
from pak8.k8s.resources.kubeconfig import Kubeconfig
from pak8.k8s.api.storage_k8s_io.v1.storage_class import CreateStorageClassData


class Pak8K8sResourceGroup(BaseModel):
    """Pak8K8sResourceGroup contains all the resources to create a microservice.
    Eg:
        Let's say our App has 1 Backend API, 1 postgres and 1 redis deployment.
        We will have 3 ResourceGroup objects. Each ResourceGroup object will
        contain how to deploy that microservice.
    """

    name: str
    enabled: bool = True
    weight: Optional[int] = 0
    crd: Optional[List[CreateCRDData]] = None
    secret: Optional[List[CreateSecretData]] = None
    config_map: Optional[List[CreateConfigMapData]] = None
    storage_class: Optional[List[CreateStorageClassData]] = None
    pvc: Optional[List[CreatePVCData]] = None
    service: Optional[List[CreateServiceData]] = None
    deployment: Optional[List[CreateDeploymentData]] = None
    port: Optional[List[CreatePortData]] = None
    volume: Optional[List[CreateVolumeData]] = None
    custom_object: Optional[List[CreateCustomObjectData]] = None


class K8sRbacConf(BaseModel):
    name: str
    enabled: Optional[bool] = True
    service_account: Optional[CreateServiceAccountData]
    cluster_role: Optional[CreateClusterRoleData]
    cluster_role_binding: Optional[CreateClusterRoleBindingData]


class Pak8K8sConf(BaseModel):
    namespace: Optional[str] = None
    context: Optional[str] = None
    # Use kubeconfig_resource when you have a saved kubeconfig resource
    # If kubeconfig_resource is available, we ignore the kubeconfig dict/path
    kubeconfig_resource: Optional[Kubeconfig] = None
    # Use kubeconfig_dict when kubeconfig is already available as a dict
    # if kubeconfig_dict is available, we ignore the kubeconfig_path
    kubeconfig_dict: Optional[Dict[str, Any]] = None
    # Use kubeconfig_path when kubeconfig needs to be stored in a file
    # Pak8 would pickle the kubeconfig and store it so a .pkl extension is recommended.
    kubeconfig_path: Optional[Path] = None
    rbac: Optional[K8sRbacConf] = None
    resource_groups: Optional[List[Pak8K8sResourceGroup]] = None
    apps: Optional[List[Any]] = None

    @validator("app")
    def apps_are_valid(cls, _app_list):
        for _app in _app_list:
            if not isinstance(_app, Pak8App):
                raise TypeError("App not of type Pak8App: {}".format(_app))
        return _app_list
