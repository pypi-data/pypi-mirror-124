from collections import OrderedDict
from typing import Optional, Dict

from pak8.app import Pak8App, Pak8AppArgs
from pak8.docker.resources.network import DockerNetwork
from pak8.docker.resources.container import DockerContainer
from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.utils.log import logger


class PostgresPak8AppArgs(Pak8AppArgs):
    name: str = "postgres"
    version: str = "0.1"
    enabled: bool = True

    # Image Args
    image_name: str = "postgres"
    image_tag: str = "14"
    postgres_db: Optional[str] = None
    postgres_user: Optional[str] = None
    postgres_password: str = "postgres"
    postgres_initdb_args: Optional[str] = None
    postgres_initdb_waldir: Optional[str] = None
    postgres_host_auth_method: Optional[str] = None
    pgdata: Optional[str] = "/var/lib/postgresql/data/pgdata"
    postgres_password_file: Optional[str] = None
    postgres_user_file: Optional[str] = None
    postgres_db_file: Optional[str] = None
    postgres_initdb_args_file: Optional[str] = None

    # Docker Args
    container_name: Optional[str] = None
    container_port: int = 5432
    container_host_port: int = 5432
    container_env: Optional[Dict[str, str]] = None
    docker_volume_name: Optional[str] = "postgres_data"
    docker_volume_bind_path: Optional[str] = "/var/lib/postgresql/data/"


class PostgresPak8App(Pak8App):
    """The PostgresPak8App deploys postgres to a docker client or K8s Cluster.
    Please refer to the README for more details.
    """

    def __init__(self, pak8_app_args: PostgresPak8AppArgs) -> None:
        logger.debug("Creating PostgresPak8App")
        if pak8_app_args is None or not isinstance(pak8_app_args, PostgresPak8AppArgs):
            raise TypeError(
                "pak8_app_args not of type PostgresPak8AppArgs: {}".format(
                    type(pak8_app_args)
                )
            )
        super().__init__(pak8_app_args=pak8_app_args)

        # Read Args
        self.args: PostgresPak8AppArgs = pak8_app_args
        # logger.debug(f"Args type: {type(self.args)}")
        # logger.debug(f"Args: {self.args.json(indent=2)}")

    def get_postgres_docker_rg(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Postgres DockerResourceGroup")

        # Container env
        _postgres_container_env = {
            "POSTGRES_USER": self.args.postgres_user,
            "POSTGRES_PASSWORD": self.args.postgres_password,
            "POSTGRES_DB": self.args.postgres_db,
            "PGDATA": self.args.pgdata,
        }
        if self.args.container_env is not None and isinstance(
            self.args.container_env, dict
        ):
            _postgres_container_env.update(self.args.container_env)

        # Container volumes
        _docker_volume_name = self.args.docker_volume_name or "{}_{}".format(
            self.args.name, "volume"
        )

        _postgres_container = DockerContainer(
            name=self.args.container_name or self.args.name,
            image="{}:{}".format(self.args.image_name, self.args.image_tag),
            detach=True,
            auto_remove=True,
            remove=True,
            environment=_postgres_container_env,
            network=create_docker_rg_data.network,
            ports={
                self.args.container_port: self.args.container_host_port,
            },
            volumes={
                _docker_volume_name: {
                    "bind": self.args.docker_volume_bind_path,
                    "mode": "rw",
                },
            },
        )

        _postgres_rg = DockerResourceGroup(
            name=self.args.name,
            enabled=self.args.enabled,
            network=DockerNetwork(name=create_docker_rg_data.network),
            containers=[_postgres_container],
        )
        # logger.debug("postgres rg:\n{}".format(_postgres_rg.json(indent=2)))
        return _postgres_rg

    def init_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> None:
        _postgres_rg: Optional[DockerResourceGroup] = self.get_postgres_docker_rg(
            create_docker_rg_data
        )
        if _postgres_rg is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            self.docker_resource_groups[_postgres_rg.name] = _postgres_rg
