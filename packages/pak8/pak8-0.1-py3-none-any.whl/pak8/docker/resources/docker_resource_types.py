from collections import OrderedDict
from typing import Dict, List, Type, Union

from pak8.docker.resources.network import DockerNetwork
from pak8.docker.resources.image import DockerImage
from pak8.docker.resources.container import DockerContainer
from pak8.docker.resources.volume import DockerVolume
from pak8.docker.resources.docker_resource_base import DockerResourceBase

# Use this as a type for an object which can hold any DockerResource
DockerResourceType = Union[
    DockerNetwork,
    DockerImage,
    DockerVolume,
    DockerContainer,
]

# Use this as an ordered list to iterate over all DockerResource Classes
# This list is the order in which resources are installed as well.
DockerResourceTypeList: List[Type[DockerResourceBase]] = [
    DockerNetwork,
    DockerImage,
    DockerVolume,
    DockerContainer,
]

# Maps each DockerResource to an install weight
# lower weight DockerResource(s) get installed first
# i.e. networks are installed first, then volumes ... and so on
DockerResourceInstallOrder: Dict[str, int] = OrderedDict(
    {
        resource_type.__name__: idx
        for idx, resource_type in enumerate(DockerResourceTypeList, start=1)
    }
)
