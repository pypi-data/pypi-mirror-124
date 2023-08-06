from collections import OrderedDict
from typing import Optional, List, Dict

from pak8.app import Pak8App, Pak8AppArgs
from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.utils.log import logger


class ElasticPak8AppArgs(Pak8AppArgs):
    name: str = "elastic"
    version: str = "0.1"
    enabled: bool = True
    docker_resource_groups: Optional[List[DockerResourceGroup]] = None


class ElasticPak8App(Pak8App):
    def __init__(self, pak8_app_args: ElasticPak8AppArgs) -> None:
        logger.debug("Creating ElasticPak8App")
        if pak8_app_args is None or not isinstance(pak8_app_args, ElasticPak8AppArgs):
            raise TypeError(
                "pak8_app_args not of type ElasticPak8AppArgs: {}".format(
                    type(pak8_app_args)
                )
            )
        super().__init__(pak8_app_args=pak8_app_args)

        self.args: ElasticPak8AppArgs = pak8_app_args
        # logger.debug(f"Args type: {type(self.args)}")
        # logger.debug(f"Args: {self.args.json(indent=2)}")

    def init_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> None:
        if self.args.docker_resource_groups is not None:
            self.docker_resource_groups = OrderedDict()
            for drg in self.args.docker_resource_groups:
                if drg is not None and isinstance(drg, DockerResourceGroup):
                    self.docker_resource_groups[drg.name] = drg
                else:
                    logger.error("+------+ DockerResourceGroup invalid")
