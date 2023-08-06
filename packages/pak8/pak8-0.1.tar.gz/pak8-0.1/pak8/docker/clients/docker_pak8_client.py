from collections import OrderedDict
from typing import Optional, List, Dict

from docker.client import DockerClient

from pak8.docker.conf.docker_pak8_conf import DockerPak8Conf
from pak8.app import Pak8App
from pak8.docker.resources.network import DockerNetwork
from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.docker.resources.docker_resource_types import DockerResourceType
from pak8.docker.docker_utils import filter_and_flatten_docker_resource_groups
from pak8.docker.exceptions import DockerClientException
from pak8.utils.log import logger


class DockerPak8Client:
    def __init__(
        self, docker_client: DockerClient, docker_pak8_conf: DockerPak8Conf
    ) -> None:
        if docker_client is None or not isinstance(docker_client, DockerClient):
            raise DockerClientException(
                "docker_client invalid: {}".format(docker_client)
            )
        if docker_pak8_conf is None or not isinstance(docker_pak8_conf, DockerPak8Conf):
            raise DockerClientException(
                "docker_pak8_conf invalid: {}".format(docker_pak8_conf)
            )

        self.docker_client: DockerClient = docker_client
        self.docker_pak8_conf: DockerPak8Conf = docker_pak8_conf

        self.docker_network: Optional[DockerNetwork] = None
        self.docker_apps: Optional[List[Pak8App]] = None
        self.docker_resource_groups: Optional[Dict[str, DockerResourceGroup]] = None

    def is_valid(self) -> bool:
        # TODO: add more checks
        return True

    ######################################################
    ## Init Docker Apps
    ######################################################

    def init_resources(self) -> bool:
        """
        This function initializes the docker resources managed by this DockerPak8Client.
            - Step 1: Create a Pak8App instance for each Pak8AppConf in the docker_pak8_conf.app
                Add these Pak8App objects to the self.docker_apps dict using the app_name as the key
            - Step 2: For each Pak8App, get the DockerResourceGroups.
            - Step 3: Add all DockerResourceGroups to the self.docker_resource_groups dict
        Returns:
            True if the resources were initialized successfully
        """
        logger.debug("-*- Initializing Docker Resources")
        # logger.debug("DockerPak8Conf: {}".format(self.docker_pak8_conf.json(indent=2)))
        if self.docker_pak8_conf.apps is None:
            logger.debug("No app to init")
            return True
        # tracking the total number of docker app to create for validation
        docker_apps_to_init = len(self.docker_pak8_conf.apps)

        # Step 1: Create a Pak8App instance for each Pak8AppConf in the docker_pak8_conf.app
        if self.docker_apps is None:
            self.docker_apps = []
        for _app in self.docker_pak8_conf.apps:
            if _app is not None:
                self.docker_apps.append(_app)
        docker_apps_inited = len(self.docker_apps)

        # Step 2: For each Pak8App, get the DockerResourceGroups.
        for _app in self.docker_apps:
            _app_rgs: Optional[
                Dict[str, DockerResourceGroup]
            ] = _app.get_docker_resource_groups(
                create_docker_rg_data=CreateDockerResourceGroupData(
                    network=self.docker_pak8_conf.network
                )
            )
            # Step 3: Add all DockerResourceGroups to the self.docker_resource_groups dict
            if _app_rgs is not None:
                if self.docker_resource_groups is None:
                    self.docker_resource_groups = OrderedDict()
                self.docker_resource_groups.update(_app_rgs)

        # logger.debug(f"Docker Apps to init: {docker_apps_to_init}")
        # logger.debug(f"Docker Apps initialized: {docker_apps_inited}")
        if docker_apps_to_init == docker_apps_inited:
            return True
        return False

    ######################################################
    ## Create Resources
    ######################################################

    def create_resources(self, name_filters: Optional[List[str]] = None) -> bool:

        if self.docker_resource_groups is None:
            logger.debug("No resources to create")
            return True

        if self.docker_client is None:
            logger.debug("docker_client unavailable")
            return False

        logger.debug("-*- Creating Docker Resources")
        _filtered_docker_resources: Optional[
            List[DockerResourceType]
        ] = filter_and_flatten_docker_resource_groups(
            docker_resource_groups=self.docker_resource_groups,
            name_filters=name_filters,
            sort_order="create",
        )

        if _filtered_docker_resources is not None:
            _num_resources_needed: int = len(_filtered_docker_resources)
            _num_resources_created: int = 0
            for resource in _filtered_docker_resources:
                logger.debug(
                    f"-==+==- Creating {resource.resource_type}: {resource.name}"
                )
                if resource:
                    try:
                        _resource_created = resource.create(
                            docker_client=self.docker_client
                        )
                        if _resource_created:
                            _num_resources_created += 1
                    except Exception as e:
                        logger.error("Error while creating resource: {}".format(e))

            logger.debug(f"# of resources needed:  {_num_resources_needed}")
            logger.debug(f"# of resources created: {_num_resources_created}")
            if _num_resources_created == _num_resources_needed:
                return True
            else:
                logger.debug(
                    f"# of resources created ({_num_resources_created}) do not match # of resources needed ({_num_resources_needed})"
                )

        return False

    ######################################################
    ## Delete Resources
    ######################################################

    def delete_resources(self, name_filters: Optional[List[str]] = None) -> bool:

        if self.docker_resource_groups is None:
            logger.debug("No resources to delete")
            return False

        if self.docker_client is None:
            logger.debug("docker_client unavailable")
            return False

        logger.debug("-*- Deleting Docker Resources")
        _filtered_docker_resources: Optional[
            List[DockerResourceType]
        ] = filter_and_flatten_docker_resource_groups(
            docker_resource_groups=self.docker_resource_groups,
            name_filters=name_filters,
            sort_order="delete",
        )

        if _filtered_docker_resources is not None:
            _num_resources_to_delete: int = len(_filtered_docker_resources)
            _num_resources_deleted: int = 0
            for resource in _filtered_docker_resources:
                logger.debug(
                    f"-==+==- Deleting: {resource.name}: {resource.resource_type}"
                )
                if resource:
                    _resource_delete = resource.delete(docker_client=self.docker_client)
                    if _resource_delete:
                        _num_resources_deleted += 1

            logger.debug(f"# of resources to delete {_num_resources_to_delete}")
            logger.debug(f"# of resources deleted: {_num_resources_deleted}")
            if _num_resources_deleted == _num_resources_to_delete:
                return True
            else:
                logger.debug(
                    f"# of resources deleted ({_num_resources_deleted}) do not match # of resources to delete ({_num_resources_to_delete})"
                )

        return False
