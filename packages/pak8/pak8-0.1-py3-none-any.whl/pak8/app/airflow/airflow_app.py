from collections import OrderedDict
from typing import Optional, List, Dict
from typing_extensions import Literal

from pak8.app import Pak8App, Pak8AppArgs
from pak8.docker.resources.container import DockerContainer
from pak8.docker.resources.docker_resource_group import (
    DockerResourceGroup,
    CreateDockerResourceGroupData,
)
from pak8.utils.log import logger


class AirflowPak8AppArgs(Pak8AppArgs):
    name: str = "airflow"
    version: str = "0.1"
    enabled: bool = True

    # Webserver Args
    ws_enabled: bool = True
    ws_image_name: str = "phidata/airflow"
    ws_image_tag: str = "0.5"
    ws_entrypoint: str = "/entrypoint.sh"
    ws_command: str = "webserver"
    ws_env: Optional[Dict[str, str]] = None
    # Set as True to init the airflow db before running the webserver
    ws_init_airflow_db: bool = False
    # Set as True to wait for the airflow db to be available before running the webserver
    ws_wait_for_db: bool = False
    # Set as True to wait for redis to be available before running the webserver
    ws_wait_for_redis: bool = False
    # Webserver Docker Args
    ws_container_name: str = "airflow-ws"
    ws_container_port: str = "8080"
    ws_container_host_port: int = 8080
    # Webserver K8s Args
    # ws_rg_name: str = "airflow-webserver"
    # ws_svc_name: str = "airflow-webserver-svc"
    # ws_deploy_name: str = "airflow-webserver-deploy"
    # ws_replicas: int = 1
    # ws_port_name: str = "http"
    # ws_port_number: int = 8080

    # Scheduler Args
    scheduler_enabled: bool = True
    scheduler_image_name: str = "phidata/airflow"
    scheduler_image_tag: str = "0.1"
    scheduler_entrypoint: str = "/entrypoint.sh"
    scheduler_command: str = "scheduler"
    scheduler_env: Optional[Dict[str, str]] = None
    scheduler_init_airflow_db: bool = False
    scheduler_wait_for_db: bool = False
    scheduler_wait_for_redis: bool = False
    scheduler_container_name: str = "airflow-scheduler"

    # Worker Args
    worker_enabled: bool = True
    worker_image_name: str = "phidata/airflow"
    worker_image_tag: str = "0.1"
    worker_entrypoint: str = "/entrypoint.sh"
    worker_command: str = "worker"
    worker_env: Optional[Dict[str, str]] = None
    worker_container_name: str = "airflow-worker"

    # Flower Args
    flower_enabled: bool = True
    flower_image_name: str = "phidata/airflow"
    flower_image_tag: str = "0.1"
    flower_entrypoint: str = "/entrypoint.sh"
    flower_command: str = "flower"
    flower_env: Optional[Dict[str, str]] = None
    flower_container_name: str = "airflow-flower"
    flower_container_port: str = "5555"
    flower_container_host_port: int = 5555

    # DB Args
    db_enabled: bool = True
    db_type: Literal["postgres", "mysql"] = "postgres"
    # Postgres as DB args
    pg_image_name: str = "postgres"
    pg_image_tag: str = "13"
    pg_driver: str = "postgresql"
    pg_env: Optional[Dict[str, str]] = None
    pg_user: str = "airflow"
    pg_password: str = "airflow"
    pg_schema: str = "airflow"
    pg_extras: str = ""
    pg_data_path: str = "/var/lib/postgresql/data/"
    # Postgres Docker Args
    pg_container_name: str = "airflow-pg"
    pg_container_port: str = "5432"
    pg_container_host_port: int = 5432
    # We currently let docker manage the storage of our database data
    pg_volume_name: str = "airflow_pg_data"
    # The directory on the users (host) machine containing the postgres data files
    # pg_data_host_path: Optional[str] = None
    # K8s Args
    # pg_rg_name: str = "airflow-pg"
    # pg_svc_name: str = "airflow-pg-svc"
    # pg_deploy_name: str = "airflow-pg-deploy"
    # pg_replicas: int = 1
    # pg_pvc_name: str = "airflow-pg-pvc"
    # pg_cm_name: str = "airflow-pg-cm"

    # Redis Args
    redis_enabled: bool = True
    redis_image_name: str = "redis"
    redis_image_tag: str = "latest"
    redis_driver: str = "redis"
    redis_user: str = "airflow"
    redis_pass: str = "airflow"
    redis_schema: str = "1"
    # Redis Docker Args
    redis_container_name: str = "airflow-redis"
    redis_container_port: str = "6379"
    redis_container_host_port: int = 6379
    # K8s Args
    # redis_svc_name: str = "airflow-redis-svc"
    # redis_deploy_name: str = "airflow-redis-deploy"

    # Common Args
    # The directory on the users (host) machine containing the airflow DAG files, starting from the workspace_dir_path.
    airflow_dags_host_dir_path: str = "/projects"
    # The path on the users (host) machine for the dir of airflow.cfg file, starting from the workspace_dir_path.
    airflow_conf_host_dir_path: str = "/workspace/airflow"
    # The directory in the container containing the airflow pipelines
    airflow__core__dags_folder: str = "/usr/local/airflow/dags"
    # The path in the container for the airflow.cfg file
    airflow__core__conf_dir: str = "/usr/local/airflow"

    # Common K8s Args
    # cm_name: str = "airflow-cm"
    # Storage Classes
    # ssd_rg_name: str = "airflow-ssd"
    # ssd_storage_class_name: str = "airflow-ssd"


class AirflowPak8App(Pak8App):
    """The AirflowPak8App deploys Apache Airflow to a docker client or K8s Cluster.
    Please refer to the README for more details.
    """

    def __init__(self, pak8_app_args: AirflowPak8AppArgs) -> None:
        logger.debug("Creating AirflowPak8App")
        if pak8_app_args is None or not isinstance(pak8_app_args, AirflowPak8AppArgs):
            raise TypeError(
                "pak8_app_args not of type AirflowPak8AppArgs: {}".format(
                    type(pak8_app_args)
                )
            )
        super().__init__(pak8_app_args=pak8_app_args)

        # Read Args
        self.args: AirflowPak8AppArgs = pak8_app_args
        logger.debug(f"Args type: {type(self.args)}")
        # logger.debug(f"Args: {self.args.json(indent=2)}")

    def get_postgres_docker_rg(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Postgres DockerResourceGroup")
        _postgres_container_env = {
            "POSTGRES_USER": self.args.pg_user,
            "POSTGRES_PASSWORD": self.args.pg_password,
            "POSTGRES_DB": self.args.pg_schema,
            "PGDATA": self.args.pg_data_path,
        }
        if self.args.pg_env is not None and isinstance(self.args.pg_env, dict):
            _postgres_container_env.update(self.args.pg_env)

        _postgres_container = DockerContainer(
            name=self.args.pg_container_name,
            image="{}:{}".format(self.args.pg_image_name, self.args.pg_image_tag),
            detach=True,
            auto_remove=True,
            remove=True,
            network=create_docker_rg_data.network,
            ports={
                self.args.pg_container_port: self.args.pg_container_host_port,
            },
            volumes={
                self.args.pg_volume_name: {
                    "bind": self.args.pg_data_path,
                    "mode": "rw",
                },
            },
        )

        _postgres_rg = DockerResourceGroup(
            name=self.args.pg_container_name,
            enabled=self.args.db_enabled,
            weight=101,
            containers=[_postgres_container],
        )
        # logger.debug("postgres rg:\n{}".format(_postgres_rg.json(indent=2)))
        return _postgres_rg

    def get_redis_docker_rg(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Redis DockerResourceGroup")
        _redis_container = DockerContainer(
            name=self.args.redis_container_name,
            image="{}:{}".format(self.args.redis_image_name, self.args.redis_image_tag),
            detach=True,
            auto_remove=True,
            remove=True,
            network=create_docker_rg_data.network,
            ports={
                self.args.redis_container_port: self.args.redis_container_host_port,
            },
        )

        _redis_rg = DockerResourceGroup(
            name=self.args.redis_container_name,
            enabled=self.args.redis_enabled,
            weight=101,
            containers=[_redis_container],
        )
        # logger.debug("redis rg:\n{}".format(_redis_rg.json(indent=2)))
        return _redis_rg

    def get_scheduler_docker_rg(
        self,
        create_docker_rg_data: CreateDockerResourceGroupData,
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Scheduler DockerResourceGroup")

        _airflow_dags_host_dir_path_str = (
            str(self.args.workspace_dir_path) + self.args.airflow_dags_host_dir_path
        )
        _airflow_conf_host_dir_path = (
            str(self.args.workspace_dir_path) + self.args.airflow_conf_host_dir_path
        )
        _scheduler_container_env = {
            "INIT_AIRFLOW_DB": self.args.scheduler_init_airflow_db,
            "WAIT_FOR_DB": self.args.scheduler_wait_for_db,
            "WAIT_FOR_REDIS": self.args.scheduler_wait_for_redis,
            "AIRFLOW_DB_CONN_URL": self.args.pg_container_name,
            "AIRFLOW_DB_CONN_PORT": self.args.pg_container_port,
            "AIRFLOW_DB_USER": self.args.pg_user,
            "AIRFLOW_DB_PASSWORD": self.args.pg_password,
            "AIRFLOW_SCHEMA": self.args.pg_schema,
            "AIRFLOW_REDIS_CONN_URL": self.args.redis_container_name,
            "AIRFLOW_REDIS_CONN_PORT": self.args.redis_container_port,
            "AIRFLOW_REDIS_USER": self.args.redis_user,
            "AIRFLOW_REDIS_PASSWORD": self.args.redis_pass,
            "AIRFLOW_REDIS_SCHEMA": self.args.redis_schema,
            "AIRFLOW__CORE__EXECUTOR": "CeleryExecutor",
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": f"{self.args.pg_driver}+psycopg2://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
            "AIRFLOW__CORE__LOAD_EXAMPLES": "True",
        }
        if self.args.scheduler_env is not None and isinstance(
            self.args.scheduler_env, dict
        ):
            _scheduler_container_env.update(self.args.scheduler_env)

        _scheduler_container = DockerContainer(
            name=self.args.scheduler_container_name,
            image="{}:{}".format(
                self.args.scheduler_image_name, self.args.scheduler_image_tag
            ),
            command=self.args.scheduler_command,
            # auto_remove=True,
            detach=True,
            entrypoint=self.args.scheduler_entrypoint,
            environment=_scheduler_container_env,
            # remove=True,
            network=create_docker_rg_data.network,
            volumes={
                _airflow_dags_host_dir_path_str: {
                    "bind": self.args.airflow__core__dags_folder,
                    "mode": "rw",
                },
                _airflow_conf_host_dir_path: {
                    "bind": self.args.airflow__core__conf_dir,
                    "mode": "rw",
                },
            },
        )

        _scheduler_rg = DockerResourceGroup(
            name=self.args.scheduler_container_name,
            enabled=self.args.scheduler_enabled,
            weight=102,
            containers=[_scheduler_container],
        )
        # logger.debug("scheduler rg:\n{}".format(_scheduler_rg.json(indent=2)))
        return _scheduler_rg

    def get_webserver_docker_rg(
        self,
        create_docker_rg_data: CreateDockerResourceGroupData,
    ) -> Optional[DockerResourceGroup]:
        logger.debug(f"Init Webserver DockerResourceGroup")

        _airflow_dags_host_dir_path_str = (
            str(self.args.workspace_dir_path) + self.args.airflow_dags_host_dir_path
        )
        _airflow_conf_host_dir_path = (
            str(self.args.workspace_dir_path) + self.args.airflow_conf_host_dir_path
        )
        _webserver_container_env = {
            "INIT_AIRFLOW_DB": self.args.ws_init_airflow_db,
            "WAIT_FOR_DB": self.args.ws_wait_for_db,
            "WAIT_FOR_REDIS": self.args.ws_wait_for_redis,
            "AIRFLOW_DB_CONN_URL": self.args.pg_container_name,
            "AIRFLOW_DB_CONN_PORT": self.args.pg_container_port,
            "AIRFLOW_DB_USER": self.args.pg_user,
            "AIRFLOW_DB_PASSWORD": self.args.pg_password,
            "AIRFLOW_SCHEMA": self.args.pg_schema,
            "AIRFLOW_REDIS_CONN_URL": self.args.redis_container_name,
            "AIRFLOW_REDIS_CONN_PORT": self.args.redis_container_port,
            "AIRFLOW_REDIS_USER": self.args.redis_user,
            "AIRFLOW_REDIS_PASSWORD": self.args.redis_pass,
            "AIRFLOW_REDIS_SCHEMA": self.args.redis_schema,
            "AIRFLOW__CORE__EXECUTOR": "CeleryExecutor",
            "AIRFLOW__CORE__SQL_ALCHEMY_CONN": f"{self.args.pg_driver}+psycopg2://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__RESULT_BACKEND": f"db+{self.args.pg_driver}://{self.args.pg_user}:{self.args.pg_password}@{self.args.pg_container_name}:{self.args.pg_container_port}/{self.args.pg_schema}{self.args.pg_extras}",
            "AIRFLOW__CELERY__BROKER_URL": f"{self.args.redis_driver}://{self.args.redis_pass}@{self.args.redis_container_name}/{self.args.redis_schema}",
            "AIRFLOW__CORE__FERNET_KEY": "FpErWX7ZxRBGxuAq2JDfle3A7k7Xxi5hY0wh_u0X0Go=",
            "AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION": "True",
            "AIRFLOW__CORE__LOAD_EXAMPLES": "True",
        }
        if self.args.ws_env is not None and isinstance(self.args.ws_env, dict):
            _webserver_container_env.update(self.args.ws_env)

        _webserver_container = DockerContainer(
            name=self.args.ws_container_name,
            image="{}:{}".format(self.args.ws_image_name, self.args.ws_image_tag),
            command=self.args.ws_command,
            # auto_remove=True,
            detach=True,
            entrypoint=self.args.ws_entrypoint,
            environment=_webserver_container_env,
            # remove=True,
            network=create_docker_rg_data.network,
            ports={
                self.args.ws_container_port: self.args.ws_container_host_port,
            },
            volumes={
                _airflow_dags_host_dir_path_str: {
                    "bind": self.args.airflow__core__dags_folder,
                    "mode": "rw",
                },
                _airflow_conf_host_dir_path: {
                    "bind": self.args.airflow__core__conf_dir,
                    "mode": "rw",
                },
            },
        )

        _webserver_rg = DockerResourceGroup(
            name=self.args.ws_container_name,
            enabled=self.args.ws_enabled,
            weight=103,
            containers=[_webserver_container],
        )
        # logger.debug("webserver rg:\n{}".format(_webserver_rg.json(indent=2)))
        return _webserver_rg

    def get_airflow_docker_rgs(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> Optional[List[DockerResourceGroup]]:
        logger.debug(f"Init AirflowPak8App DockerResourceGroups")

        airflow_docker_rgs: List[DockerResourceGroup] = []

        # Airflow Database DockerResourceGroup
        if self.args.db_enabled:
            if self.args.db_type == "postgres":
                _pg_docker_rg = self.get_postgres_docker_rg(create_docker_rg_data)
                if _pg_docker_rg is not None:
                    airflow_docker_rgs.append(_pg_docker_rg)

        # Airflow Redis DockerResourceGroup
        if self.args.redis_enabled:
            _redis_docker_rg = self.get_redis_docker_rg(create_docker_rg_data)
            if _redis_docker_rg is not None:
                airflow_docker_rgs.append(_redis_docker_rg)

        # Airflow Scheduler DockerResourceGroup
        if self.args.scheduler_enabled:
            _scheduler_docker_rg = self.get_scheduler_docker_rg(create_docker_rg_data)
            if _scheduler_docker_rg is not None:
                airflow_docker_rgs.append(_scheduler_docker_rg)

        # Airflow Webserver DockerResourceGroup
        if self.args.ws_enabled:
            _webserver_docker_rg = self.get_webserver_docker_rg(create_docker_rg_data)
            if _webserver_docker_rg is not None:
                airflow_docker_rgs.append(_webserver_docker_rg)

        return airflow_docker_rgs

    def init_docker_resource_groups(
        self, create_docker_rg_data: CreateDockerResourceGroupData
    ) -> None:
        _airflow_rgs: Optional[List[DockerResourceGroup]] = self.get_airflow_docker_rgs(
            create_docker_rg_data
        )
        if _airflow_rgs is not None:
            if self.docker_resource_groups is None:
                self.docker_resource_groups = OrderedDict()
            for _rg in _airflow_rgs:
                self.docker_resource_groups[_rg.name] = _rg

    # def get_airflow_k8s_resource_group(
    #     self,
    #     args: AirflowPak8AppArgs,
    #     common_k8s_rg_data: CommonK8sResourceGroupData,
    # ) -> k8s_resources.K8sResourceGroup:
    #
    #     airflow_k8s_resource_group: k8s_resources.K8sResourceGroup = (
    #         k8s_resources.K8sResourceGroup(
    #             name=self.name,
    #             enabled=True,
    #             secret=[],
    #             cm=[],
    #             storage_class=[],
    #             pvc=[],
    #             svc=[],
    #             deploy=[],
    #         )
    #     )
    #
    #     ######################################################
    #     ## Define common secrets and config maps
    #     ######################################################
    #
    #     # Airflow Config-Map contains all environment variables which are not secret.
    #     # The keys of this configmap will become env variables in all containers
    #     cm_data = CreateConfigMapData(
    #         name=args.CM_NAME,
    #         data={
    #             "POSTGRES_SERVICE": args.PG_SVC_NAME,
    #             "POSTGRES_PORT": f"{args.PG_PORT_NUMBER}",
    #             "POSTGRES_USER": args.PG_USER,
    #             "POSTGRES_PASSWORD": args.PG_PASS,
    #             "POSTGRES_DB": args.PG_DB,
    #             "REDIS_SERVICE": args.REDIS_SVC_NAME,
    #             "REDIS_PORT": f"{args.REDIS_PORT_NUMBER}",
    #             "AIRFLOW__CORE__EXECUTOR": "LocalExecutor",
    #             "AIRFLOW__CELERY__BROKER_URL": f"redis://{args.REDIS_SVC_NAME}:{args.REDIS_PORT_NUMBER}/{args.REDIS_DB}",
    #             "AIRFLOW__CELERY__RESULT_BACKEND": f"db+postgresql://{args.PG_USER}:{args.PG_PASS}@{args.PG_SVC_NAME}:{args.PG_PORT_NUMBER}/{args.PG_DB}",
    #             "AIRFLOW__CORE__FERNET_KEY": "46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho=",
    #             "AIRFLOW__CORE__SQL_ALCHEMY_CONN": f"postgresql+psycopg2://{args.PG_USER}:{args.PG_PASS}@{args.PG_SVC_NAME}:{args.PG_PORT_NUMBER}/{args.PG_DB}",
    #             "AIRFLOW__WEBSERVER__BASE_URL": "http://localhost/airflow",
    #         },
    #     )
    #     cm_resource: Optional[k8s_resources.ConfigMap] = create_configmap_resource(
    #         group_name=self.name,
    #         namespace=common_k8s_rg_data.namespace,
    #         create_cm_data=cm_data,
    #         create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #     )
    #     if cm_resource:
    #         airflow_k8s_resource_group.cm.append(cm_resource)  # type: ignore
    #
    #     # Create a resource group for storage class and add it to self._k8s_resource_groups
    #     # this will create the storage classes used by any postgres deployments
    #     ssd_storage_class: Optional[
    #         k8s_resources.StorageClass
    #     ] = create_storage_class_resource(
    #         group_name=self.name,
    #         namespace=common_k8s_rg_data.namespace,
    #         storage_class=CreateStorageClassData(
    #             name=args.SSD_STORAGE_CLASS_NAME,
    #             storage_class_type=enums.StorageClassType.GCE_SSD,
    #         ),
    #         create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #     )
    #     if ssd_storage_class:
    #         airflow_k8s_resource_group.storage_class.append(ssd_storage_class)  # type: ignore
    #
    #     # Create the Airflow Webserver Resource Group if needed
    #     ws_suffix: str = "webserver"
    #     if args.WS_ENABLED:
    #
    #         ws_port = CreatePortData(
    #             name=args.WS_PORT_NAME,
    #             container_port=args.WS_PORT_NUMBER,
    #         )
    #         ws_containers: List[CreateContainer] = [
    #             CreateContainer(
    #                 name=args.WS_DEPLOY_NAME,
    #                 repo=args.REPO,
    #                 tag=self.version,
    #                 args=["webserver"],
    #                 envs_from_configmap=[args.CM_NAME],
    #             )
    #         ]
    #
    #         ws_deploy_data: CreateDeploymentData = CreateDeploymentData(
    #             containers=ws_containers,
    #             name=args.WS_DEPLOY_NAME,
    #             replicas=args.WS_REPLICAS,
    #         )
    #         ws_deploy_resource: Optional[
    #             k8s_resources.Deployment
    #         ] = create_deployment_resource(
    #             group_name=f"{self.name}-{ws_suffix}",
    #             namespace=common_k8s_rg_data.namespace,
    #             deploy=ws_deploy_data,
    #             ports=[ws_port],
    #             service_account_name=common_k8s_rg_data.service_account_name,
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if ws_deploy_resource is not None:
    #             airflow_k8s_resource_group.deploy.append(ws_deploy_resource)  # type: ignore
    #
    #         ws_svc_data: CreateServiceData = CreateServiceData(
    #             name=args.WS_SVC_NAME,
    #             service_type=enums.ServiceType.NODEPORT,
    #         )
    #         ws_svc_resource: Optional[k8s_resources.Service] = create_service_resource(
    #             group_name=f"{self.name}-{ws_suffix}",
    #             namespace=common_k8s_rg_data.namespace,
    #             svc=ws_svc_data,
    #             ports=[ws_port],
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if ws_svc_resource is not None:
    #             airflow_k8s_resource_group.svc.append(ws_svc_resource)  # type: ignore
    #
    #     # Create the Airflow Postgres Resource Group if needed
    #     pg_key: str = "postgres"
    #     if args.PG_ENABLED:
    #
    #         pg_cm_data = CreateConfigMapData(
    #             name=args.PG_CM_NAME,
    #             data={
    #                 "POSTGRES_USER": args.PG_USER,
    #                 "POSTGRES_PASSWORD": args.PG_PASS,
    #                 "POSTGRES_DB": args.PG_DB,
    #                 "PGDATA": "/var/lib/postgresql/data/pgdata",
    #             },
    #         )
    #         pg_cm_resource: Optional[k8s_resources.ConfigMap] = create_configmap_resource(
    #             group_name=f"{self.name}-{pg_key}",
    #             namespace=common_k8s_rg_data.namespace,
    #             create_cm_data=pg_cm_data,
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if pg_cm_resource:
    #             airflow_k8s_resource_group.cm.append(pg_cm_resource)  # type: ignore
    #
    #         pg_pvc_data = CreatePVCData(
    #             name=args.PG_PVC_NAME,
    #             request_storage="1Gi",
    #             storage_class_name=args.SSD_STORAGE_CLASS_NAME,
    #         )
    #         pg_pvc_resource: Optional[
    #             k8s_resources.PersistentVolumeClaim
    #         ] = create_pvc_resource(
    #             group_name=f"{self.name}-{pg_key}",
    #             namespace=common_k8s_rg_data.namespace,
    #             pvc=pg_pvc_data,
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if pg_pvc_resource:
    #             airflow_k8s_resource_group.pvc.append(pg_pvc_resource)  # type: ignore
    #
    #         # pg_volume_data = CreateVolumeData(
    #         #     name=args.PG_PVC_NAME,
    #         #     mount_path="/var/lib/postgresql/data",
    #         #     volume_type=enums.VolumeType.PERSISTENT_VOLUME_CLAIM,
    #         #     pvc_name=args.PG_PVC_NAME,
    #         # )
    #         # pg_volume: Optional[k8s_resources.Volume] = create_volume_resource(
    #         #     group_name=f"{self.name}-{pg_key}",
    #         #     volume=pg_volume_data,
    #         # )
    #
    #         pg_port = CreatePortData(
    #             name=args.PG_PORT_NAME,
    #             container_port=args.PG_PORT_NUMBER,
    #         )
    #         pg_container = CreateContainer(
    #             repo="postgres",
    #             tag="11.2-alpine",
    #             envs_from_configmap=[args.PG_CM_NAME],
    #         )
    #         pg_deploy_data: CreateDeploymentData = CreateDeploymentData(
    #             containers=[pg_container],
    #             name=args.PG_DEPLOY_NAME,
    #             replicas=args.PG_REPLICAS,
    #         )
    #         pg_deploy_resource: Optional[
    #             k8s_resources.Deployment
    #         ] = create_deployment_resource(
    #             group_name=f"{self.name}-{pg_key}",
    #             namespace=common_k8s_rg_data.namespace,
    #             deploy=pg_deploy_data,
    #             ports=[pg_port],
    #             service_account_name=common_k8s_rg_data.service_account_name,
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if pg_deploy_resource is not None:
    #             airflow_k8s_resource_group.deploy.append(pg_deploy_resource)  # type: ignore
    #
    #         pg_svc_data = CreateServiceData(
    #             name=args.PG_SVC_NAME, service_type=enums.ServiceType.CLUSTERIP
    #         )
    #         pg_svc_resource: Optional[k8s_resources.Service] = create_service_resource(
    #             group_name=f"{self.name}-{pg_key}",
    #             namespace=common_k8s_rg_data.namespace,
    #             svc=pg_svc_data,
    #             ports=[pg_port],
    #             create_common_labels_dict=common_k8s_rg_data.create_common_labels_dict,
    #         )
    #         if pg_svc_resource is not None:
    #             airflow_k8s_resource_group.svc.append(pg_svc_resource)  # type: ignore
    #
    #     return airflow_k8s_resource_group
