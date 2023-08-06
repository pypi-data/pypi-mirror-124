from time import sleep
from typing import Optional, Any, Dict, List

from docker.client import DockerClient
from docker.models.images import Image
from docker.errors import BuildError, APIError, ImageNotFound, NotFound

from pak8.docker.resources.docker_resource_base import DockerResourceBase
from pak8.utils.log import logger


class DockerImage(DockerResourceBase):
    resource_type: str = "Image"

    # Path to the directory containing the Dockerfile
    path: Optional[str] = None
    # A file object to use as the Dockerfile. (Or a file-like object)
    fileobj: Optional[Any] = None
    # A tag to add to the final image
    tag: Optional[str] = None
    # Whether to return the status
    quiet: Optional[bool] = None
    # Don’t use the cache when set to True
    nocache: Optional[bool] = None
    # Remove intermediate containers.
    # The docker build command defaults to --rm=true,
    # The docker api kept the old default of False to preserve backward compatibility
    rm: Optional[bool] = None
    # HTTP timeout
    timeout: Optional[int] = None
    # Optional if using fileobj
    custom_context: Optional[bool] = None
    # The encoding for a stream. Set to gzip for compressing
    encoding: Optional[str] = None
    # Downloads any updates to the FROM image in Dockerfiles
    pull: Optional[bool] = None
    # Always remove intermediate containers, even after unsuccessful builds
    forcerm: Optional[bool] = None
    # path within the build context to the Dockerfile
    dockerfile: Optional[str] = None
    # A dictionary of build arguments
    buildargs: Optional[Dict[str, Any]] = None
    # A dictionary of limits applied to each container created by the build process. Valid keys:
    # memory (int): set memory limit for build
    # memswap (int): Total memory (memory + swap), -1 to disable swap
    # cpushares (int): CPU shares (relative weight)
    # cpusetcpus (str): CPUs in which to allow execution, e.g. "0-3", "0,1"
    container_limits: Optional[Dict[str, Any]] = None
    # Size of /dev/shm in bytes. The size must be greater than 0. If omitted the system uses 64MB
    shmsize: Optional[int] = None
    # A dictionary of labels to set on the image
    labels: Optional[Dict[str, Any]] = None
    # A list of images used for build cache resolution
    cache_from: Optional[List[Any]] = None
    # Name of the build-stage to build in a multi-stage Dockerfile
    target: Optional[str] = None
    # networking mode for the run commands during build
    network_mode: Optional[str] = None
    # Squash the resulting images layers into a single layer.
    squash: Optional[bool] = None
    # Extra hosts to add to /etc/hosts in building containers, as a mapping of hostname to IP address.
    extra_hosts: Optional[Dict[str, Any]] = None
    # Platform in the format os[/arch[/variant]].
    platform: Optional[str] = None
    # Isolation technology used during build. Default: None.
    isolation: Optional[str] = None
    # If True, and if the docker client configuration file (~/.docker/config.json by default)
    # contains a proxy configuration, the corresponding environment variables
    # will be set in the container being built.
    use_config_proxy: Optional[bool] = None

    # Image object after it is built.
    image_object: Optional[Image] = None
    image_build_id: Optional[str] = None
    # print the build log
    print_build_log: bool = False

    def get_active_resource(self, docker_client: DockerClient) -> Any:
        """Returns an Image object if available"""

        self.verbose_log("DockerImage.get_active_resource")
        try:
            _image: Optional[List[Image]] = docker_client.images.get(self.tag)
            if _image is not None and isinstance(_image, Image):
                self.verbose_log("Image found: {}".format(_image))
                self.image_object = _image
                return _image
        except (NotFound, ImageNotFound) as not_found_err:
            self.verbose_log("Image {} not found".format(self.tag))

        return None

    def build_image(
        self,
        docker_client: DockerClient,
    ) -> Optional[Image]:

        self.verbose_log("Building image: {}".format(self.tag))
        self.verbose_log(
            "Args: {}".format(
                self.json(indent=2, exclude_unset=True, exclude_none=True)
            )
        )
        try:
            (_image, _build_log_stream) = docker_client.images.build(
                path=self.path,
                fileobj=self.fileobj,
                tag=self.tag,
                quiet=self.quiet,
                nocache=self.nocache,
                rm=self.rm,
                timeout=self.timeout,
                custom_context=self.custom_context,
                encoding=self.encoding,
                pull=self.pull,
                forcerm=self.forcerm,
                dockerfile=self.dockerfile,
                buildargs=self.buildargs,
                container_limits=self.container_limits,
                shmsize=self.shmsize,
                labels=self.labels,
                cache_from=self.cache_from,
                target=self.target,
                network_mode=self.network_mode,
                squash=self.squash,
                extra_hosts=self.extra_hosts,
                platform=self.platform,
                isolation=self.isolation,
                use_config_proxy=self.use_config_proxy,
            )
            if self.print_build_log:
                for _build_log in _build_log_stream:
                    _stream = _build_log.get("stream", None)
                    if _stream is None or _stream == "\\n":
                        continue
                    if "Step" in _stream:
                        logger.info(_stream)
                    if _build_log.get("aux", None) is not None:
                        logger.debug("_build_log['aux'] :{}".format(_build_log["aux"]))
                        self.image_build_id = _build_log.get("aux", {}).get("ID")
            return _image
        except TypeError as type_error:
            logger.exception(type_error)
            # logger.error("TypeError: {}".format(type_error))
        except BuildError as build_error:
            logger.exception(build_error)
            # logger.error("BuildError: {}".format(build_error))
        except APIError as api_err:
            logger.exception(api_err)
            # logger.error("ApiError: {}".format(api_err))

        return None

    def create(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Creates the image

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerImage.create")

        _image: Optional[Image] = None
        # Get the active image from the docker_client if skip_if_exists = True
        if self.use_cache:
            _image = self.get_active_resource(docker_client)

        # If Image does not exist, create one
        if _image is None:
            try:
                _image = self.build_image(docker_client)
                if _image is not None and isinstance(_image, Image):
                    self.verbose_log("Image built: {}".format(_image))
                    self.image_object = _image
                    return True
                else:
                    self.verbose_log("Image {} could not be built".format(self.tag))
            except Exception as e:
                logger.exception(e)
                logger.error("Error while creating image: {}".format(e))
                raise

        return True

    def delete(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Deletes the Image

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerImage.delete")

        image_object: Optional[Image] = self.get_active_resource(docker_client)
        # Return True if there is no image to delete
        if image_object is None:
            self.verbose_log("No image to delete")
            return True

        # Delete Container
        try:
            self.verbose_log("Deleting image: {}".format(self.tag))
            docker_client.images.remove(image=self.tag, force=True)
            return True
        except Exception as e:
            logger.exception("Error while deleting image: {}".format(e))
        return False
