from typing import Any, Optional, Dict

from pydantic import BaseModel
from docker.client import DockerClient

from pak8.utils.log import logger


class DockerResourceBase(BaseModel):
    """Base class for all Docker Resources.
    All Models in the pak8.docker.resources module are expected to be subclasses of this Model.
    The rationale for using a pydantic model here is that the data which populates this
    model comes from the docker api, which can return anything so we need to validate
    the data were ingesting.
    """

    # is defined in each subclass
    resource_type: Optional[str] = None
    # name is used to identify objects of a subclass
    name: Optional[str] = None
    # If True, create the resource only if an existing active
    # resource with the same name does not exist.
    use_cache: bool = True
    # If True, logs extra debug messages
    use_verbose_logs: bool = False

    # Data provided by the resource running on the docker client
    id: Optional[str] = None
    short_id: Optional[str] = None
    attrs: Optional[Dict[str, Any]] = None

    def get_active_resource(self, docker_client: DockerClient) -> Optional[Any]:
        """Returns the resource object if it is active on the docker_client
        Eg:
            * For a Network resource, it will return the DockerNetwork object
            currently running on docker.
        """
        logger.error("@get_active_resource method not defined")
        return None

    def create(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Creates the resource on docker

        Args:
            docker_client: The docker_client for the current env
        """
        logger.error("@create method not defined")
        return False

    def delete(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Deletes the resource on docker

        Args:
            docker_client: The docker_client for the current env
        """
        logger.error("@delete method not defined")
        return False

    def verbose_log(self, msg: Any) -> None:
        if self.use_verbose_logs:
            logger.debug(msg)

    class Config:
        # https://pydantic-docs.helpmanual.io/usage/model_config/
        # If we need to use an alias for fields of subclasses, eg: Kubeconfig
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        use_enum_values = True
