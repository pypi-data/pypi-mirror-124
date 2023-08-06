from collections import OrderedDict
from typing import Optional, List, Dict, Any

from pak8.app import Pak8App, Pak8AppArgs
from pak8.docker.resources.network import DockerNetwork
from pak8.docker.resources.container import DockerContainer
from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.utils.log import logger


class DevboxPak8AppArgs(Pak8AppArgs):
    name: str = "devbox"
    version: str = "0.1"
    enabled: bool = True

    # Image args
    image_name: str = "phidata/devbox"
    image_tag: str = "0.1"
    entrypoint: str = "/entrypoint.sh"
    command: str = "chill"
    env: Optional[Dict[str, str]] = None

    # Devbox args
    # requirements.txt file path
    install_requirements: bool = True
    requirements_file_path: str = "/workspace/requirements.txt"
    container_requirements_file_path: str = "/requirements.txt"
    # projects directory path
    projects_dir_path: str = "/projects"
    container_projects_dir_path: str = "/projects"

    # Airflow args
    # True => setup this devbox to use airflow
    init_airflow: bool = False
    # True => init the airflow db locally in this devbox
    init_airflow_db: Optional[bool] = False
    wait_for_airflow_db: Optional[bool] = False
    wait_for_airflow_redis: Optional[bool] = False
    airflow_db_conn_url: Optional[str] = "airflow-pg"
    airflow_db_conn_port: Optional[str] = "5432"
    airflow_db_user: Optional[str] = "airflow"
    airflow_db_password: Optional[str] = "airflow"
    airflow_schema: Optional[str] = "airflow"
    airflow_redis_conn_url: Optional[str] = "airflow-redis"
    airflow_redis_conn_port: Optional[str] = "6379"
    airflow_redis_password: Optional[str] = None
    # The path on the users (host) machine for the airflow.cfg file
    airflow_conf_host_file_path: str = "/workspace/airflow/airflow.cfg"
    # The directory in the container containing the airflow pipelines
    airflow__core__dags_folder: str = "/usr/local/airflow/dags"
    # The path in the container for the airflow.cfg file
    airflow__core__conf_file: str = "/usr/local/airflow/airflow.cfg"

    # Temporary args
    install_phidata: bool = True
    phidata_dir_path: str = "/Users/ashpreetbedi/philab/phidata"
    container_phidata_dir_path: str = "/phidata"


class DevboxPak8App(Pak8App):
    """The DevboxPak8App deploys a data devbox i.e. a testing environment
    to a docker client or K8s Cluster.
    Please refer to the README for more details.
    """

    def __init__(self, pak8_app_args: DevboxPak8AppArgs) -> None:
        logger.debug("Creating DevboxPak8App")
        if pak8_app_args is None or not isinstance(pak8_app_args, DevboxPak8AppArgs):
            raise TypeError(
                "pak8_app_args not of type DevboxPak8AppArgs: {}".format(
                    type(pak8_app_args)
                )
            )
        super().__init__(pak8_app_args=pak8_app_args)

        # Read Args
        self.args: DevboxPak8AppArgs = pak8_app_args
        # logger.debug(f"args type: {type(self.args)}")
        # logger.debug(f"args: {self.args.json(indent=2)}")

    def get_devbox_docker_rgs(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Devbox DockerResourceGroup")

        # Create env dict
        _devbox_container_env: Dict[str, Any] = {
            "INSTALL_REQUIREMENTS": self.args.install_requirements,
            "REQUIREMENTS_FILE_PATH": self.args.container_requirements_file_path,
            "INSTALL_PHIDATA": self.args.install_phidata,
            "PHIDATA_DIR_PATH": self.args.container_phidata_dir_path,
            "INIT_AIRFLOW_DB": self.args.init_airflow_db,
            "WAIT_FOR_AIRFLOW_DB": self.args.wait_for_airflow_db,
            "WAIT_FOR_AIRFLOW_REDIS": self.args.wait_for_airflow_redis,
            "AIRFLOW_DB_CONN_URL": self.args.airflow_db_conn_url,
            "AIRFLOW_DB_CONN_PORT": self.args.airflow_db_conn_port,
            "AIRFLOW_DB_USER": self.args.airflow_db_user,
            "AIRFLOW_DB_PASSWORD": self.args.airflow_db_password,
            "AIRFLOW_SCHEMA": self.args.airflow_schema,
            "AIRFLOW_REDIS_CONN_URL": self.args.airflow_redis_conn_url,
            "AIRFLOW_REDIS_CONN_PORT": self.args.airflow_redis_conn_port,
            "AIRFLOW_REDIS_PASSWORD": self.args.airflow_redis_password,
        }
        if self.args.env is not None and isinstance(self.args.env, dict):
            _devbox_container_env.update(self.args.env)

        # Create volumes
        _projects_dir_path = (
            str(self.args.workspace_dir_path) + self.args.projects_dir_path
        )
        _requirements_file_path = (
            str(self.args.workspace_dir_path) + self.args.requirements_file_path
        )
        # mount projects on host directory to /projects directory in the container
        _devbox_container_volumes = {
            _requirements_file_path: {
                "bind": self.args.container_requirements_file_path,
                "mode": "rw",
            },
            _projects_dir_path: {
                "bind": self.args.container_projects_dir_path,
                "mode": "rw",
            },
            self.args.phidata_dir_path: {
                "bind": self.args.container_phidata_dir_path,
                "mode": "rw",
            },
        }
        if self.args.init_airflow:
            # mount projects to airflow dags folder
            # _devbox_container_volumes[_projects_dir_path] = {
            #         "bind": self.args.airflow__core__dags_folder,
            #         "mode": "rw",
            # }

            # mount airflow conf file
            _airflow_conf_host_file_path = (
                str(self.args.workspace_dir_path)
                + self.args.airflow_conf_host_file_path
            )
            _devbox_container_volumes[_airflow_conf_host_file_path] = {
                "bind": self.args.airflow__core__conf_file,
                "mode": "rw",
            }

        _devbox_container = DockerContainer(
            name=self.args.name,
            image="{}:{}".format(self.args.image_name, self.args.image_tag),
            command=self.args.command,
            auto_remove=True,
            detach=True,
            entrypoint=self.args.entrypoint,
            environment=_devbox_container_env,
            remove=True,
            network=create_docker_rg_data.network,
            volumes=_devbox_container_volumes,
        )

        _devbox_rg = DockerResourceGroup(
            name=self.args.name,
            enabled=self.args.enabled,
            network=DockerNetwork(name=create_docker_rg_data.network),
            containers=[_devbox_container],
        )
        return _devbox_rg

    def init_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> None:
        _devbox_rg: Optional[DockerResourceGroup] = self.get_devbox_docker_rgs(
            create_docker_rg_data
        )
        if _devbox_rg is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            self.docker_resource_groups[_devbox_rg.name] = _devbox_rg
