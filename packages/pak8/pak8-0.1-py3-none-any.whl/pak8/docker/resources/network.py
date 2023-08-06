from typing import Optional, Any, List, Dict

from docker.client import DockerClient
from docker.models.networks import Network
from docker.errors import NotFound

from pak8.docker.resources.docker_resource_base import DockerResourceBase
from pak8.utils.log import logger


class DockerNetwork(DockerResourceBase):
    resource_type: str = "Network"

    # driver (str) – Name of the driver used to create the network
    driver: Optional[str] = None
    # options (dict) – Driver options as a key-value dictionary
    options: Optional[Dict[str, Any]] = None
    # check_duplicate (bool) – Request daemon to check for networks with same name. Default: None.
    auto_remove: Optional[bool] = None
    # internal (bool) – Restrict external access to the network. Default False.
    internal: Optional[bool] = None
    # labels (dict) – Map of labels to set on the network. Default None.
    labels: Optional[Dict[str, Any]] = None
    # enable_ipv6 (bool) – Enable IPv6 on the network. Default False.
    enable_ipv6: Optional[bool] = None
    # attachable (bool) – If enabled, and the network is in the global scope
    # non-service containers on worker nodes will be able to connect to the network.
    attachable: Optional[bool] = None
    # scope (str) – Specify the network’s scope (local, global or swarm)
    scope: Optional[str] = None
    # ingress (bool) – If set, create an ingress network which provides the routing-mesh in swarm mode.
    ingress: Optional[bool] = None

    def get_active_resource(self, docker_client: DockerClient) -> Any:
        """Returns a Network object if the network is active on the docker_client"""

        # self.verbose_log("DockerNetwork.get_active_resource")
        # Get active networks from the docker_client
        _network_name: Optional[str] = self.name
        # self.verbose_log(f"Checking if network {_network_name} exists")
        _network_list: Optional[List[Network]] = docker_client.networks.list()
        # self.verbose_log("_network_list: {}".format(_network_list))
        if _network_list is not None:
            for _network in _network_list:
                if _network.name == _network_name:
                    self.verbose_log(f"Network {_network_name} exists")
                    return _network
        return None

    def create(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Creates the Network on docker

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerNetwork.create")

        _network_name: Optional[str] = self.name
        network_object: Optional[Network] = None
        # Get the active network from the docker_client if skip_if_exists = True
        if self.use_cache:
            network_object = self.get_active_resource(docker_client)

        # If a Network does not exist, create one
        if network_object is None:
            try:
                # self.verbose_log("Creating Network: {}".format(_network_name))
                _network = docker_client.networks.create(_network_name)
                self.verbose_log("Network created: {}".format(_network.name))
                # self.verbose_log("Network {}".format(_network.attrs))
                network_object = _network
            except Exception as e:
                logger.exception("Error while creating network: {}".format(e))

        # By this step the network should be created
        # Validate that the network is created
        # self.verbose_log("Validating network is created")
        if network_object is not None:
            # TODO: validate that the network actually started
            return True
        return False

    def delete(
        self,
        docker_client: DockerClient,
    ) -> bool:
        """Deletes the Network on docker

        Args:
            docker_client: The docker_client for the current env
        """
        self.verbose_log("DockerNetwork.delete")

        _network_name: Optional[str] = self.name
        network_object: Optional[Network] = self.get_active_resource(docker_client)
        # Return True if there is no Network to delete
        if network_object is None:
            return True

        # Delete Network
        try:
            network_object.remove()
        except Exception as e:
            logger.exception("Error while deleting network: {}".format(e))

        # Validate that the network is deleted
        self.verbose_log("Validating network is deleted")
        try:
            self.verbose_log("Reloading network_object: {}".format(network_object))
            network_object.reload()
        except NotFound as e:
            self.verbose_log("Got NotFound Exception, Network is deleted")
            return True

        return False
