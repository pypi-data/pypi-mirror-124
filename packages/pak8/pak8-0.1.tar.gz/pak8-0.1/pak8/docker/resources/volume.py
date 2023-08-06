from typing import Optional, Any, Dict, Union, List

from docker.client import DockerClient
from docker.models.volumes import Volume

from pak8.docker.resources.docker_resource_base import DockerResourceBase
from pak8.utils.log import logger


class DockerVolume(DockerResourceBase):
    resource_type: str = "Volume"

    # driver (str) – Name of the driver used to create the volume
    driver: Optional[str] = None
    # driver_opts (dict) – Driver options as a key-value dictionary
    driver_opts: Optional[Dict[str, Any]] = None
    # labels (dict) – Labels to set on the volume
    labels: Optional[Dict[str, Any]] = None

    def get_active_resource(self, docker_client: DockerClient) -> Any:
        """Returns a Volume object if the volume is active on the docker_client"""

        self.verbose_log("DockerVolume.get_active_resource")
        # Get active volumes from the docker_client
        _volume_name: Optional[str] = self.name
        self.verbose_log(f"Checking if volume {_volume_name} exists")
        _volume_list: Optional[List[Volume]] = docker_client.volumes.list()
        # self.verbose_log("_volume_list: {}".format(_volume_list))
        if _volume_list is not None:
            for _volume in _volume_list:
                if _volume.name == _volume_name:
                    self.verbose_log(f"Volume {_volume_name} exists")
                    return _volume
        return None

    def create(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Creates the Volume on docker

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerVolume.create")

        _volume_name: Optional[str] = self.name
        volume_object: Optional[Volume] = None
        # Get the active volume from the docker_client if skip_if_exists = True
        if self.use_cache:
            volume_object = self.get_active_resource(docker_client)

        # If a Volume does not exist, create one
        if volume_object is None:
            try:
                self.verbose_log("Creating Volume: {}".format(_volume_name))
                _volume = docker_client.volumes.create(
                    name=_volume_name,
                    driver=self.driver,
                    driver_opts=self.driver_opts,
                    labels=self.labels,
                )
                self.verbose_log("Volume created: {}".format(_volume.name))
                self.verbose_log("Volume {}".format(_volume.attrs))
                volume_object = _volume
            except Exception as e:
                self.verbose_log("Error while creating volume: {}".format(e))

        # By this step the volume should be created
        # Get the data from the volume object
        if volume_object is not None:
            _id: str = volume_object.id
            _short_id: str = volume_object.short_id
            _name: str = volume_object.name
            _attrs: str = volume_object.attrs
            if _id:
                self.verbose_log("_id: {}".format(_id))
                self.id = _id
            if _short_id:
                self.verbose_log("_short_id: {}".format(_short_id))
                self.short_id = _short_id
            if _name:
                self.verbose_log("_name: {}".format(_name))
            if _attrs:
                self.verbose_log("_attrs: {}".format(_attrs))
                # TODO: use json_to_dict(_attrs)
                self.attrs = _attrs  # type: ignore
            # TODO: Validate that the volume object is created properly
            return True
        return False

    def delete(
        self,
        docker_client: DockerClient,
        only_if_active: Optional[bool] = True,
    ) -> bool:
        """Deletes the Volume on docker

        Args:
            docker_client: The docker_client for the current env
            only_if_active: If True, delete the volume only if an existing active
                volume with the same name exists.
        """
        self.verbose_log("DockerVolume.delete")
        return False
