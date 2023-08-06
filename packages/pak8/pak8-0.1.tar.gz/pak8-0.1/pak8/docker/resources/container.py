from time import sleep
from typing import Optional, Any, Dict, Union, List

from docker.client import DockerClient
from docker.models.containers import Container
from docker.errors import NotFound, ImageNotFound, APIError

from pak8.docker.resources.docker_resource_base import DockerResourceBase
from pak8.utils.log import logger


class DockerContainerMount(DockerResourceBase):
    resource_type: str = "ContainerMount"

    target: str
    source: str
    type: str = "volume"
    read_only: bool = False
    labels: Optional[Dict[str, Any]] = None


class DockerContainer(DockerResourceBase):
    resource_type: str = "Container"

    # image (str) – The image to run.
    image: Optional[str] = None
    # command (str or list) – The command to run in the container.
    command: Optional[Union[str, List]] = None
    # auto_remove (bool) – enable auto-removal of the container on daemon side when the container’s process exits.
    auto_remove: Optional[bool] = None
    # detach (bool) – Run container in the background and return a Container object.
    detach: Optional[bool] = None
    # entrypoint (str or list) – The entrypoint for the container.
    entrypoint: Optional[Union[str, List]] = None
    # environment (dict or list) – Environment variables to set inside the container
    environment: Optional[Union[Dict[str, Any], List]] = None
    # group_add (list) – List of additional group names and/or IDs that the container process will run as.
    group_add: Optional[List[Any]] = None
    # healthcheck (dict) – Specify a test to perform to check that the container is healthy.
    healthcheck: Optional[Dict[str, Any]] = None
    # hostname (str) – Optional hostname for the container.
    hostname: Optional[str] = None
    # labels (dict or list) – A dictionary of name-value labels
    # e.g. {"label1": "value1", "label2": "value2"})
    # or a list of names of labels to set with empty values (e.g. ["label1", "label2"])
    labels: Optional[Dict[str, Any]] = None
    # mounts (list) – Specification for mounts to be added to the container.
    # More powerful alternative to volumes.
    # Each item in the list is a DockerContainerMount object which is then converted to a docker.types.Mount object.
    mounts: Optional[List[DockerContainerMount]] = None
    # network (str) – Name of the network this container will be connected to at creation time
    network: Optional[str] = None
    # network_disabled (bool) – Disable networking.
    network_disabled: Optional[str] = None
    # network_mode (str) One of:
    # bridge - Create a new network stack for the container on on the bridge network.
    # none - No networking for this container.
    # container:<name|id> - Reuse another container’s network stack.
    # host - Use the host network stack. This mode is incompatible with ports.
    # network_mode is incompatible with network.
    network_mode: Optional[str] = None
    # ports (dict) – Ports to bind inside the container.
    ports: Optional[Dict[str, Any]] = None
    # remove (bool) – Remove the container when it has finished running. Default: False.
    remove: Optional[bool] = None
    # Restart the container when it exits. Configured as a dictionary with keys:
    # Name: One of on-failure, or always.
    # MaximumRetryCount: Number of times to restart the container on failure.
    # For example: {"Name": "on-failure", "MaximumRetryCount": 5}
    restart_policy: Optional[Dict[str, Any]] = None
    # user (str or int) – Username or UID to run commands as inside the container.
    user: Optional[Union[str, int]] = None
    # volumes (dict or list) –
    # A dictionary to configure volumes mounted inside the container.
    # The key is either the host path or a volume name, and the value is a dictionary with the keys:
    # bind - The path to mount the volume inside the container
    # mode - Either rw to mount the volume read/write, or ro to mount it read-only.
    # For example:
    # {
    #   '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'},
    #   '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}
    # }
    volumes: Optional[Union[Dict[str, Any], List]] = None
    # working_dir (str) – Path to the working directory.
    working_dir: Optional[str] = None

    # Data provided by the resource running on the docker client
    status: Optional[str] = None

    def get_active_resource(self, docker_client: DockerClient) -> Any:
        """Returns a Container object if the container is active on the docker_client"""

        # self.verbose_log("DockerContainer.get_active_resource")
        # Get active containers from the docker_client
        _container_name: Optional[str] = self.name
        # self.verbose_log(f"Checking if container {_container_name} exists")
        _container_list: Optional[List[Container]] = docker_client.containers.list(
            all=True
        )
        # self.verbose_log("_container_list: {}".format(_container_list))
        if _container_list is not None:
            for _container in _container_list:
                if _container.name == _container_name:
                    self.verbose_log(f"Container {_container_name} exists")
                    return _container
        return None

    def run_container(
        self,
        docker_client: DockerClient,
    ) -> Optional[Container]:

        self.verbose_log("Running container: {}".format(self.image))
        self.verbose_log(
            "Args: {}".format(
                self.json(indent=2, exclude_unset=True, exclude_none=True)
            )
        )
        try:
            _container = docker_client.containers.run(
                name=self.name,
                image=self.image,
                command=self.command,
                auto_remove=self.auto_remove,
                detach=self.detach,
                entrypoint=self.entrypoint,
                environment=self.environment,
                group_add=self.group_add,
                healthcheck=self.healthcheck,
                hostname=self.hostname,
                labels=self.labels,
                mounts=self.mounts,
                network=self.network,
                network_disabled=self.network_disabled,
                network_mode=self.network_mode,
                ports=self.ports,
                remove=self.remove,
                restart_policy=self.restart_policy,
                user=self.user,
                volumes=self.volumes,
                working_dir=self.working_dir,
            )
            return _container
        except AttributeError as attr_error:
            logger.error(f"AttributeError: {attr_error}")
        except ImageNotFound as img_error:
            logger.error(f"Image {self.image} not found")
        except NotFound as not_found_error:
            logger.error(not_found_error.explanation)
        except APIError as api_err:
            logger.exception(api_err)
            # logger.error("ApiError: {}".format(api_err))

        return None

    def create(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Creates the Container on docker

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerContainer.create")

        _container_name: Optional[str] = self.name
        container_object: Optional[Container] = self.get_active_resource(docker_client)
        # container_object is not None => container exists
        # not self.use_cache => not use the cache container
        # => delete the existing container and set to None
        if container_object is not None and not self.use_cache:
            logger.debug(
                "Removing container {} because use_cache = {}".format(
                    _container_name, self.use_cache
                )
            )
            _container_deleted = self.delete(docker_client)
            if _container_deleted:
                container_object = None

        # If a Container does not exist, create one
        if container_object is None:
            try:
                # self.verbose_log("Running Container: {}".format(_container_name))
                container_object = self.run_container(docker_client)
                if container_object is not None:
                    self.verbose_log(
                        "Container Created: {}".format(container_object.name)
                    )
                else:
                    self.verbose_log("Container could not be created")
                # self.verbose_log("Container {}".format(_container.attrs))
            except Exception as e:
                logger.exception("Error while creating container: {}".format(e))
                raise

        # By this step the container should be created
        # Validate that the container is running
        self.verbose_log("Validating container is created")
        if container_object is not None:
            container_object.reload()
            _status: str = container_object.status
            # self.verbose_log("status type: {}".format(type(_status)))
            self.verbose_log("Container Status: {}".format(_status))
            self.status = _status
            wait_for_start = False
            if _status == "created":
                self.verbose_log(
                    f"Container {_container_name} is created but not yet running"
                )
                self.verbose_log(
                    "Waiting for 30 seconds for the container to start running"
                )
                sleep(30)
                container_object.reload()
                _status = container_object.status
                if _status == "created":
                    self.verbose_log(
                        f"Stopping and removing container {_container_name}"
                    )
                    container_object.stop()
                    container_object.remove()
                    container_object = self.run_container(docker_client)
                wait_for_start = True
            if _status == "exited":
                self.verbose_log(f"Starting container {_container_name}")
                container_object.remove()
                container_object = self.run_container(docker_client)
                wait_for_start = True

            if wait_for_start:
                self.verbose_log("Waiting for 30 seconds for the container to start")
                sleep(30)
                _status = container_object.status
                while _status != "created":
                    self.verbose_log(
                        "--> status: {}, trying again in 30 seconds".format(_status)
                    )
                    sleep(30)
                    _status = container_object.status
                self.verbose_log("--> status: {}".format(_status))

            # TODO IMPORTANT: validate that the container is running
            if _status == "running" or "created":
                return True

        self.verbose_log("Container not found :(")
        return False

    def delete(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Deletes the Container on docker

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerContainer.delete")

        _container_name: Optional[str] = self.name
        container_object: Optional[Container] = self.get_active_resource(docker_client)
        # Return True if there is no Container to delete
        if container_object is None:
            return True

        # Delete Container
        try:
            self.verbose_log("Deleting Container: {}".format(_container_name))
            _status: str = container_object.status
            self.status = _status
            self.verbose_log("Container Status: {}".format(_status))
            self.verbose_log("Stopping Container: {}".format(_container_name))
            container_object.stop()
            self.verbose_log("Waiting 10 seconds for the container to stop")
            sleep(10)
            # If self.remove is set, then the container would be auto removed after being stopped
            # If self.remove is not set, we need to manually remove the container
            if not self.remove:
                self.verbose_log("Removing Container: {}".format(_container_name))
                container_object.remove()
        except Exception as e:
            logger.exception("Error while deleting container: {}".format(e))

        # Validate that the Container is deleted
        self.verbose_log("Validating Container is deleted")
        try:
            self.verbose_log("Reloading container_object: {}".format(container_object))
            container_object.reload()
        except NotFound as e:
            self.verbose_log("Got NotFound Exception, Container is deleted")
            return True

        return False
