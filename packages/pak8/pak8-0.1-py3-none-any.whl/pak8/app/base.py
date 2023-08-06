from pathlib import Path
from typing import Optional, Dict, Any

from pydantic import BaseModel

from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.k8s.resources.k8s_resource_group import (
    K8sResourceGroup,
    CreateK8sResourceGroupData,
)
from pak8.utils.log import logger


class Pak8AppArgs(BaseModel):
    name: str
    version: str
    enabled: bool

    # path for the workspace directory
    workspace_dir_path: Optional[Path] = None
    # path for the workspace config file
    workspace_config_file_path: Optional[Path] = None


class Pak8App:
    """Base Class for all Pak8 Apps.

    Each Pak8App inherits from this base class,
    """

    def __init__(self, pak8_app_args: Any) -> None:

        # The following block must be implemented by each sublass
        # logger.debug("Creating Pak8App. Pak8AppArgs: {}".format(pak8_app_args))
        # if pak8_app_args is None or not isinstance(pak8_app_args, Pak8AppArgs):
        #     raise TypeError("pak8_app_args not of type DevboxPak8AppArgs: {}".format(type(pak8_app_args)))
        # super().__init__(pak8_app_args=pak8_app_args)

        self.pak8_app_args: Pak8AppArgs = pak8_app_args
        self.docker_resource_groups: Optional[Dict[str, DockerResourceGroup]] = None
        self.k8s_resource_groups: Optional[Dict[str, K8sResourceGroup]] = None

    def init_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> None:
        logger.debug(
            f"@init_docker_resource_groups not defined for {self.__class__.__name__}"
        )

    def get_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[Dict[str, DockerResourceGroup]]:
        if self.docker_resource_groups is None:
            self.init_docker_resource_groups(create_docker_rg_data)
        # Uncomment when debugging
        # if self.docker_resource_groups:
        #     logger.debug("DockerResourceGroups:")
        #     for rg_name, rg in self.docker_resource_groups.items():
        #         logger.debug(
        #             "{}: {}".format(rg_name, rg.json(exclude_none=True, indent=2))
        #         )
        return self.docker_resource_groups

    def init_k8s_resource_groups(
        self, create_k8s_rg_data: CreateK8sResourceGroupData
    ) -> None:
        logger.debug(
            f"@init_k8s_resource_groups not defined for {self.__class__.__name__}"
        )

    def get_k8s_resource_groups(
        self, create_k8s_rg_data: CreateK8sResourceGroupData
    ) -> Optional[Dict[str, K8sResourceGroup]]:
        if self.k8s_resource_groups is None:
            self.init_k8s_resource_groups(create_k8s_rg_data)
        # Uncomment when debugging
        # if self.k8s_resource_groups:
        #     logger.debug(
        #         "K8sResourceGroups :\n{}".format(
        #             self.k8s_resource_groups.items()
        #             if self.k8s_resource_groups is not None
        #             else "None"
        #         )
        #     )
        return self.k8s_resource_groups

    # def get_k8s_resource_groups_as_dicts(
    #     self,
    #     kind_filters: Optional[List[str]] = None,
    #     name_filters: Optional[List[str]] = None,
    # ) -> Optional[Dict[str, List[Dict[str, Any]]]]:
    #
    #     logger.debug(
    #         "Getting K8sResourceGroups for Pak8AppConf :\n{}".format(
    #             self.k8s_resource_groups
    #         )
    #     )
    #     k8s_rgs = self.k8s_resource_groups
    #     if k8s_rgs is None:
    #         logger.debug("No K8sResourceGroups available")
    #         return None
    #
    #     k8s_rg_dict: Dict[str, List[Dict[str, Any]]] = OrderedDict()
    #     for rg_name, k8s_rg in k8s_rgs.items():
    #         if not k8s_rg.enabled:
    #             continue
    #         _k8s_resources_for_rg: Optional[
    #             List[K8sResourceType]
    #         ] = get_k8s_resources_from_group(
    #             k8s_resource_group=k8s_rg,
    #             kind_filters=kind_filters,
    #             name_filters=name_filters,
    #         )
    #         if _k8s_resources_for_rg is None:
    #             continue
    #
    #         _k8s_resource_dicts: List[Dict[str, Any]] = []
    #         for resource in _k8s_resources_for_rg:
    #             _dict = resource.get_k8s_manifest_dict()
    #             if _dict:
    #                 _k8s_resource_dicts.append(_dict)
    #
    #         if len(_k8s_resource_dicts) > 0:
    #             k8s_rg_dict[rg_name] = _k8s_resource_dicts
    #
    #     logger.debug("K8sResourceGroups:\n{}".format(k8s_rg_dict))
    #     return k8s_rg_dict
    #
    # def create_resources(
    #     self,
    #     k8s_api: K8sApi,
    #     namespace: Optional[str] = None,
    #     kind_filters: Optional[List[str]] = None,
    #     name_filters: Optional[List[str]] = None,
    #     only_if_not_active: Optional[bool] = True,
    # ) -> bool:
    #     if self.k8s_resource_groups is None:
    #         logger.debug("No K8sResourceGroups available")
    #         return False
    #
    #     logger.debug(f"Creating Resource for {self.name}")
    #     _filtered_k8s_resources: Optional[
    #         List[K8sResourceType]
    #     ] = filter_and_flatten_k8s_resource_groups(
    #         k8s_resource_groups=self.k8s_resource_groups,
    #         kind_filters=kind_filters,
    #         name_filters=name_filters,
    #         sort_order="create",
    #     )
    #     if _filtered_k8s_resources:
    #         for resource in _filtered_k8s_resources:
    #             logger.debug(f"Creating: {resource.metadata.name} | NS: {namespace}")
    #             if resource and k8s_api:
    #                 resource.create_if(
    #                     k8s_api=k8s_api,
    #                     namespace=namespace,
    #                     only_if_not_active=only_if_not_active,
    #                 )
    #     # TODO: Add validation before returning True
    #     return True
    #
    # def get_active_resource_classes(
    #     self,
    #     kind_filters: Optional[List[str]] = None,
    #     name_filters: Optional[List[str]] = None,
    # ) -> Optional[Set[Type[K8sResourceBase]]]:
    #
    #     if self.k8s_resource_groups is None:
    #         logger.debug("No K8sResourceGroups available")
    #         return None
    #
    #     _filtered_k8s_resources: Optional[
    #         List[K8sResourceType]
    #     ] = filter_and_flatten_k8s_resource_groups(
    #         k8s_resource_groups=self.k8s_resource_groups,
    #         kind_filters=kind_filters,
    #         name_filters=name_filters,
    #         sort_order="create",
    #     )
    #     return dedup_resource_types(_filtered_k8s_resources)
    #
    # def get_active_resources(
    #     self,
    #     k8s_api: K8sApi,
    #     namespace: Optional[str] = None,
    #     kind_filters: Optional[List[str]] = None,
    #     name_filters: Optional[List[str]] = None,
    # ) -> Optional[Dict[str, List[Any]]]:
    #
    #     from kubernetes.client.rest import ApiException
    #
    #     active_resource_classes: Optional[
    #         Set[Type[K8sResourceBase]]
    #     ] = self.get_active_resource_classes(kind_filters, name_filters)
    #
    #     if active_resource_classes is None:
    #         return None
    #
    #     active_k8s_resources: Dict[str, List[Any]] = defaultdict(list)
    #     for resource_class in active_resource_classes:
    #         resource_type: str = resource_class.__name__
    #         logger.debug(f"Resource Type: {resource_type}")
    #         try:
    #             _active_objects: Optional[List[Any]] = resource_class.read_from_cluster(
    #                 k8s_api=k8s_api, namespace=namespace
    #             )
    #             if _active_objects is not None and isinstance(_active_objects, list):
    #                 active_k8s_resources[resource_type] = _active_objects
    #         except ApiException as e:
    #             logger.debug(
    #                 f"ApiException while getting {resource_type}, reason: {e.reason}"
    #             )
    #
    #     return active_k8s_resources
