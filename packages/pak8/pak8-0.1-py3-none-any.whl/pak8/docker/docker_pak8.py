from typing import Optional, List

from docker.client import DockerClient

from pak8.docker.clients import DockerPak8Client
from pak8.docker.conf import DockerPak8Conf
from pak8.docker.enums import DockerPak8Status
from pak8.docker.exceptions import DockerPak8ConfInvalidException, DockerClientException
from pak8.utils.log import logger


class DockerPak8:
    def __init__(self, ws_name: str, docker_pak8_conf: DockerPak8Conf):
        if ws_name is None or docker_pak8_conf is None:
            raise DockerPak8ConfInvalidException("Invalid DockerPak8Conf")

        self._ws_name: str = ws_name
        self._docker_pak8_conf: DockerPak8Conf = docker_pak8_conf
        self._pak8_status: DockerPak8Status = DockerPak8Status.INIT

        # Clients
        self._docker_pak8_client: Optional[DockerPak8Client] = None
        logger.debug(f"** DockerPak8 created")

    def init_docker_client(self, docker_client: DockerClient) -> bool:

        # logger.debug("--- DockerPak8 init start")
        if self._docker_pak8_client is None:
            if self._docker_pak8_conf is None:
                logger.debug("Invalid DockerPak8Conf")
                return False
            try:
                self._docker_pak8_client = DockerPak8Client(
                    docker_client, self._docker_pak8_conf
                )
                self._pak8_status = DockerPak8Status.CLIENT_VALID
            except DockerClientException as e:
                logger.debug("DockerClientException: {}".format(e))
                raise
            # logger.debug("--- DockerPak8 init complete")

        # TODO: update the is_valid() function to validate the pak8_docker_client
        return self._docker_pak8_client.is_valid()

    def get_pak8_status(self, refresh: bool = False) -> DockerPak8Status:
        # logger.debug("Getting Pak8 status")
        if refresh:
            self._pak8_status = DockerPak8Status.INIT
            logger.debug(
                "Refreshing DockerPak8 status: {}".format(DockerPak8Status.INIT)
            )

        if self._pak8_status == DockerPak8Status.INIT:
            if (
                self._docker_pak8_client is not None
                and self._docker_pak8_client.is_valid()
            ):
                self._pak8_status = DockerPak8Status.CLIENT_VALID

        return self._pak8_status

    def create_resources(self, name_filters: Optional[List[str]] = None) -> bool:

        pak8_status = self.get_pak8_status()
        if not pak8_status.can_create_resources():
            logger.debug("Cannot create resources")
            return False
        if self._docker_pak8_client is None:
            logger.debug("docker_client is none")
            return False

        init_success: bool = self._docker_pak8_client.init_resources()
        if not init_success:
            logger.debug("Cannot initialize resources")
            return False

        return self._docker_pak8_client.create_resources(name_filters=name_filters)

    def validate_resources_are_created(
        self, name_filters: Optional[List[str]] = None
    ) -> bool:

        logger.debug("Validating resources are created...")
        return True

    def delete_resources(self, name_filters: Optional[List[str]] = None) -> bool:

        pak8_status = self.get_pak8_status()
        if not pak8_status.can_delete_resources():
            logger.debug("Cannot delete resources")
            return False
        if self._docker_pak8_client is None:
            logger.debug("docker_client is none")
            return False

        init_success: bool = self._docker_pak8_client.init_resources()
        if not init_success:
            logger.debug("Cannot initialize resources")
            return False

        return self._docker_pak8_client.delete_resources(name_filters=name_filters)

    def validate_resources_are_deleted(
        self, name_filters: Optional[List[str]] = None
    ) -> bool:

        logger.debug("Validating resources are deleted...")
        return True
