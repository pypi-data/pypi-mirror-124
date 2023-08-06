from typing import Dict, List, Optional, Type

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums

# from pak8.conf.pak8_conf import Pak8Conf
from pak8.k8s.conf import Pak8K8sConf
from pak8.k8s.conf.k8s_pak8_conf import Pak8K8sResourceGroup, K8sRbacConf
from pak8.utils.log import logger
from pak8.k8s.resources.k8s_resource_group import (
    K8sResourceGroup,
    CreateK8sResourceGroupData,
)
from pak8.k8s.resources.apps.v1.deployment import Deployment
from pak8.k8s.resources.core.v1.service import Service
from pak8.k8s.resources.core.v1.persistent_volume_claim import PersistentVolumeClaim
from pak8.k8s.resources.core.v1.namespace import Namespace
from pak8.k8s.resources.core.v1.secret import Secret
from pak8.k8s.resources.core.v1.config_map import ConfigMap
from pak8.k8s.resources.storage_k8s_io.v1.storage_class import StorageClass
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_object import CustomObject
from pak8.k8s.resources.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
    CustomResourceDefinition,
)
from pak8.k8s.resources.common.labels import create_common_labels_dict


# Common data used by each K8sResourceGroup
# TODO: replace with pak8.k8s.k8s_resources.k8s_resource_group.CreateK8sResourceGroupData
class CommonK8sResourceGroupData(BaseModel):
    namespace: str
    service_account_name: Optional[str] = None
    common_labels: Optional[Dict[str, str]] = None


def create_k8s_resource_group_from_pak8_resource_group(
    pak8_resource_group: Pak8K8sResourceGroup,
    common_k8s_rg_data: CommonK8sResourceGroupData,
) -> Optional[K8sResourceGroup]:
    """Creates a K8sResourceGroup using a Pak8K8sResourceGroup"""

    if pak8_resource_group is None:
        return None

    _group_name = pak8_resource_group.name
    _group_enabled = pak8_resource_group.enabled
    _group_weight = pak8_resource_group.weight

    logger.debug(f"Creating K8sResourceGroup for {_group_name}")

    k8s_resource_group: K8sResourceGroup = K8sResourceGroup(
        name=_group_name,
        enabled=_group_enabled,
        weight=_group_weight,
    )

    for resource_type, resource_data in pak8_resource_group.__dict__.items():

        if resource_data is None:
            continue
        logger.debug(f"Parsing {resource_type}")

        ######################################################
        ## Create deploy k8s_resources from Pak8 deployment
        ######################################################
        if resource_type == "deployment":
            logger.debug(f"deployment type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateDeploymentData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.apps.v1.deployment import (
                create_deployment_resource,
                CreateDeploymentData,
            )

            deploy_resources: List[Deployment] = []
            for _deployment in resource_data:
                if not isinstance(_deployment, CreateDeploymentData):
                    logger.warning(f"Invalid type for _deployment: {type(_deployment)}")
                    continue
                _deploy_resource: Optional[Deployment] = create_deployment_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    deploy=_deployment,
                    ports=pak8_resource_group.port,
                    volumes=pak8_resource_group.volume,
                    service_account_name=common_k8s_rg_data.service_account_name,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _deploy_resource:
                    deploy_resources.append(_deploy_resource)
            if len(deploy_resources) >= 0:
                k8s_resource_group.deploy = deploy_resources

        ######################################################
        ## Create svc k8s_resources from Pak8 service
        ######################################################
        elif resource_type == "service":
            logger.debug(f"service type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateServiceData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.core.v1.service import (
                CreateServiceData,
                create_service_resource,
            )

            svc_resources: List[Service] = []
            for _service in resource_data:
                if not isinstance(_service, CreateServiceData):
                    logger.warning(f"Invalid type for _service: {type(_service)}")
                    continue
                _svc_resource: Optional[Service] = create_service_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    svc=_service,
                    ports=pak8_resource_group.port,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _svc_resource:
                    svc_resources.append(_svc_resource)
            if len(svc_resources) >= 0:
                k8s_resource_group.svc = svc_resources

        ######################################################
        ## Create cm k8s_resources from Pak8 config_map
        ######################################################
        elif resource_type == "config_map":
            logger.debug(f"config_map type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateConfigMapData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.core.v1.config_map import (
                CreateConfigMapData,
                create_configmap_resource,
            )

            cm_resources: List[ConfigMap] = []
            for _config_map in resource_data:
                if not isinstance(_config_map, CreateConfigMapData):
                    logger.warning(f"Invalid type for _config_map: {type(_config_map)}")
                    continue
                _cm_resource: Optional[ConfigMap] = create_configmap_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    create_cm_data=_config_map,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _cm_resource:
                    cm_resources.append(_cm_resource)
            if len(cm_resources) >= 0:
                k8s_resource_group.cm = cm_resources

        ######################################################
        ## Create secret k8s_resources from Pak8 secret
        ######################################################
        elif resource_type == "secret":
            logger.debug(f"secret type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateSecretData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.core.v1.secret import (
                CreateSecretData,
                create_secret_resource,
            )

            secret_resources: List[Secret] = []
            for _secret in resource_data:
                if not isinstance(_secret, CreateSecretData):
                    logger.warning(f"Invalid type for _secret': {type(_secret)}")
                    continue
                _secret_resource: Optional[Secret] = create_secret_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    secret=_secret,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _secret_resource:
                    secret_resources.append(_secret_resource)
            if len(secret_resources) >= 0:
                k8s_resource_group.secret = secret_resources

        ######################################################
        ## Create pvc k8s_resources from Pak8 pvc
        ######################################################
        elif resource_type == "pvc":
            logger.debug(f"pvc type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreatePVCData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.core.v1.persistent_volume_claim import (
                CreatePVCData,
                create_pvc_resource,
            )

            pvc_resources: List[PersistentVolumeClaim] = []
            for _pvc in resource_data:
                if not isinstance(_pvc, CreatePVCData):
                    logger.warning(f"Invalid type for _pvc': {type(_pvc)}")
                    continue
                _pvc_resource: Optional[PersistentVolumeClaim] = create_pvc_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    pvc=_pvc,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _pvc_resource:
                    pvc_resources.append(_pvc_resource)
            if len(pvc_resources) >= 0:
                k8s_resource_group.pvc = pvc_resources

        ######################################################
        ## Create storage_class k8s_resources from Pak8 storage_class
        ######################################################
        elif resource_type == "storage_class":
            logger.debug(f"storage_class type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateStorageClassData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.storage_k8s_io.v1.storage_class import (
                CreateStorageClassData,
                create_storage_class_resource,
            )

            storage_class_resources: List[StorageClass] = []
            for _storage_class in resource_data:
                if not isinstance(_storage_class, CreateStorageClassData):
                    logger.warning(
                        f"Invalid type for _storage_class': {type(_storage_class)}"
                    )
                    continue
                _storage_class_resource: Optional[
                    StorageClass
                ] = create_storage_class_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    storage_class=_storage_class,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _storage_class_resource:
                    storage_class_resources.append(_storage_class_resource)
            if len(storage_class_resources) >= 0:
                k8s_resource_group.storage_class = storage_class_resources

        ######################################################
        ## Create crd k8s_resources from Pak8 crd
        ######################################################
        elif resource_type == "crd":
            logger.debug(f"crd type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateCRDData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.apiextensions_k8s_io.v1beta1.custom_resource_definition import (
                CreateCRDData,
                create_crd_resource,
            )

            crd_resources: List[CustomResourceDefinition] = []
            for _crd in resource_data:
                if not isinstance(_crd, CreateCRDData):
                    logger.warning(f"Invalid type for _crd': {type(_crd)}")
                    continue
                _crd_resource: Optional[CustomResourceDefinition] = create_crd_resource(
                    group_name=_group_name,
                    crd=_crd,
                )
                if _crd_resource:
                    crd_resources.append(_crd_resource)
            if len(crd_resources) >= 0:
                k8s_resource_group.crd = crd_resources

        ######################################################
        ## Create custom_object k8s_resources from Pak8 custom_object
        ######################################################
        elif resource_type == "custom_object":
            logger.debug(f"custom_object type: {type(resource_data)}")
            if not isinstance(resource_data, List):
                logger.error(
                    f"Expecting List[CreateCustomObjectData], received {type(resource_data)}"
                )
                continue

            # Add necessary imports here to speed up file load time
            from pak8.k8s.api.apiextensions_k8s_io.v1beta1.custom_object import (
                CreateCustomObjectData,
                create_custom_object_resource,
            )

            custom_object_resources: List[CustomObject] = []
            for _custom_object in resource_data:
                if not isinstance(_custom_object, CreateCustomObjectData):
                    logger.warning(
                        f"Invalid type for _custom_object': {type(_custom_object)}"
                    )
                    continue
                _custom_object_resource: Optional[
                    CustomObject
                ] = create_custom_object_resource(
                    group_name=_group_name,
                    namespace=common_k8s_rg_data.namespace,
                    custom_object=_custom_object,
                    common_labels=common_k8s_rg_data.common_labels,
                )
                if _custom_object_resource:
                    custom_object_resources.append(_custom_object_resource)
            if len(custom_object_resources) >= 0:
                k8s_resource_group.custom_object = custom_object_resources

    return k8s_resource_group


#
# def get_k8s_resource_groups_for_pak8_service(
#     pak8_app: Pak8AppConf,
#     common_k8s_rg_data: CommonK8sResourceGroupData,
# ) -> Optional[Dict[str, K8sResourceGroup]]:
#     """Returns the K8sResourceGroups for a Pak8AppConf"""
#
#     if (
#         pak8_app is None
#         or pak8_app.type is None
#         or not isinstance(pak8_app.type, k8s_enums.Pak8AppType)
#     ):
#         return None
#
#     from pak8.app.pak8_app_base import Pak8App
#     from pak8.app.pak8_app_provider import Pak8AppProvider
#
#     _pak8_app: Optional[Pak8App] = None
#     _pak8_app_class: Optional[Type[Pak8App]] = Pak8AppProvider.get(pak8_app.type, None)
#     if _pak8_app_class:
#         logger.debug(
#             "Creating K8sResourceGroups for: {}".format(_pak8_app_class.__name__)
#         )
#         _pak8_app = _pak8_app_class(pak8_app)
#         if _pak8_app:
#             # TODO: fix this when common_k8s_rg_data is replaced with CreateK8sResourceGroupData
#             return _pak8_app.get_k8s_resource_groups(
#                 CreateK8sResourceGroupData(
#                     namespace=common_k8s_rg_data.namespace,
#                     service_account_name=common_k8s_rg_data.service_account_name,
#                     common_labels=common_k8s_rg_data.common_labels,
#                 )
#             )
#     return None
#
#
#
# def get_k8s_resource_groups_for_pak8_conf(
#     pak8_conf: Pak8Conf, pak8_k8s_conf: Pak8K8sConf
# ) -> Dict[str, K8sResourceGroup]:
#     """Returns all K8sResourceGroups for a Pak8Conf.
#
#     Only the namespace + service account are the two k8s_resources created by default.
#     All other resource groups must either be created from a Pak8AppConf or Pak8K8sResourceGroup.
#     """
#     from collections import OrderedDict
#     from pak8.conf.constants import (
#         NAMESPACE_RESOURCE_GROUP_KEY,
#         RBAC_RESOURCE_GROUP_KEY,
#     )
#     from pak8.k8s.api.core.v1.namespace import create_namespace_resource
#     from pak8.k8s.api.core.v1.service_account import (
#         create_service_account_resource,
#         CreateServiceAccountData,
#     )
#     from pak8.k8s.api.rbac_authorization_k8s_io.v1.cluste_role_binding import (
#         create_cluster_role_binding_resource,
#     )
#     from pak8.k8s.api.rbac_authorization_k8s_io.v1.cluster_role import (
#         create_cluster_role_resource,
#     )
#     from pak8.k8s.k8s_utils import (
#         get_default_ns_name,
#         get_default_sa_name,
#         get_default_rbac_rg_name,
#     )
#
#     pak8_name: str = pak8_conf.name
#     logger.debug(f"Creating K8sResourceGroups for: {pak8_name}")
#
#     k8s_resource_groups: Dict[str, K8sResourceGroup] = OrderedDict()
#     common_labels: Dict[str, str] = create_common_labels_dict(
#         name=pak8_name,
#         version=pak8_conf.version,
#         cloud_provider=pak8_conf.cloud_provider,
#     )
#
#     # Step 1: Create the namespace resource
#     namespace_name: str = (
#         pak8_k8s_conf.namespace
#         if pak8_conf and pak8_k8s_conf and pak8_k8s_conf.namespace
#         else get_default_ns_name(pak8_name)
#     )
#     logger.debug(f"Creating Namespace: {namespace_name}")
#     namespace_resource: Namespace = create_namespace_resource(
#         name=namespace_name,
#         part_of=pak8_name,
#         common_labels=common_labels,
#     )
#     # Create a K8sResourceGroup with the namespace resource
#     k8s_resource_groups[NAMESPACE_RESOURCE_GROUP_KEY] = K8sResourceGroup(
#         name=NAMESPACE_RESOURCE_GROUP_KEY, enabled=True, weight=0, ns=namespace_resource
#     )
#
#     # Step 2: Create RBAC k8s_resources for the cluster to use
#     # Fill in default values where needed
#     rbac: Optional[K8sRbacConf] = (
#         pak8_k8s_conf.rbac
#         if pak8_conf and pak8_k8s_conf and pak8_k8s_conf.rbac
#         else None
#     )
#     # If no rbac is provided, create a default K8sRbacConf
#     if rbac is None:
#         rbac = K8sRbacConf(name=get_default_rbac_rg_name(pak8_name), enabled=True)
#     # Create default SA if needed
#     if rbac.service_account is None:
#         rbac.service_account = CreateServiceAccountData(
#             name=get_default_sa_name(pak8_name)
#         )
#     # if rbac.cluster_role is None:
#     #     rbac.cluster_role = CreateClusterRoleData(
#     #         name=get_default_cr_name(pak8_name),
#     #         rules=[
#     #             CreatePolicyRule(api_groups=["*"], k8s_resources=["*"], verbs=["*"],)
#     #         ],
#     #     )
#     # if rbac.cluster_role_binding is None:
#     #     rbac.cluster_role_binding = CreateClusterRoleBindingData(
#     #         name=get_default_crb_name(pak8_name),
#     #         cluster_role_name=rbac.cluster_role.name,
#     #         service_account_name=rbac.service_account.name,
#     #     )
#
#     # Using the K8sRbacConf, now create an Rbac K8sResourceGroup
#     rbac_resource_group = K8sResourceGroup(
#         name=rbac.name, enabled=rbac.enabled, weight=1
#     )
#     if rbac.service_account:
#         logger.debug(f"Creating SA: {rbac.service_account.name}")
#         rbac_resource_group.sa = create_service_account_resource(
#             create_service_account=rbac.service_account,
#             part_of=pak8_name,
#             namespace=namespace_name,
#             common_labels=common_labels,
#         )
#     if rbac.cluster_role:
#         logger.debug(f"Creating CR: {rbac.cluster_role.name}")
#         rbac_resource_group.cr = create_cluster_role_resource(
#             create_cluster_role=rbac.cluster_role,
#             part_of=pak8_name,
#             namespace=namespace_name,
#             common_labels=common_labels,
#         )
#     if rbac.cluster_role_binding:
#         logger.debug(f"Creating CRB: {rbac.cluster_role_binding.name}")
#         rbac_resource_group.crb = create_cluster_role_binding_resource(
#             create_cluster_role_binding=rbac.cluster_role_binding,
#             part_of=pak8_name,
#             namespace=namespace_name,
#             common_labels=common_labels,
#         )
#     k8s_resource_groups[RBAC_RESOURCE_GROUP_KEY] = rbac_resource_group
#
#     # Now that we have the base namespace and Rbac resource groups
#     # Create all other K8sResourceGroups
#     common_k8s_rg_data = CommonK8sResourceGroupData(
#         namespace=namespace_name,
#         service_account_name=rbac.service_account.name,
#         common_labels=common_labels,
#     )
#
#     # Step 3: Create K8sResourceGroups for each Pak8AppConf
#     if pak8_k8s_conf is not None and pak8_k8s_conf.app is not None:
#         for pak8_app_name, pak8_app in pak8_k8s_conf.app.items():
#             _pak8_app_k8s_resource_groups: Optional[
#                 Dict[str, K8sResourceGroup]
#             ] = get_k8s_resource_groups_for_pak8_service(pak8_app, common_k8s_rg_data)
#             if _pak8_app_k8s_resource_groups:
#                 k8s_resource_groups.update(_pak8_app_k8s_resource_groups)
#
#     # Step 4: Create K8sResourceGroups for Pak8ResourceGroups if needed
#     if pak8_k8s_conf is not None and pak8_k8s_conf.resource_groups is not None:
#         for pak8_rg in pak8_k8s_conf.resource_groups:
#             _k8s_rg = create_k8s_resource_group_from_pak8_resource_group(
#                 pak8_rg, common_k8s_rg_data
#             )
#             if _k8s_rg:
#                 k8s_resource_groups[pak8_rg.name] = _k8s_rg
#
#     return k8s_resource_groups
