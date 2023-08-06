from typing import Optional, List, Dict, Tuple

from typing_extensions import Literal

from pak8.docker.resources.docker_resource_group import DockerResourceGroup
from pak8.docker.resources.docker_resource_base import DockerResourceBase
from pak8.docker.resources.docker_resource_types import (
    DockerResourceInstallOrder,
    DockerResourceType,
)
from pak8.utils.log import logger


def get_install_weight_for_docker_resource(
    docker_resource_type: DockerResourceType, resource_group_weight: int = 100
) -> int:
    """Function which takes a DockerResource and resource_group_weight and returns the install
    weight for that resource.

    Understanding install weights for DockerResources:

    - Each DockerResource in a Pak8 gets an install weight, which determines the order for installing that particular resource.
    - By default, DockerResources are installed in the order determined by the DockerResourceInstallOrder dict.
        The DockerResourceInstallOrder dict ensures volumes are created before containers
    - We can also provide a weight to the DockerResourceGroup, that weight determines the install order for resources of
        that resource group as compared to other resource groups.
    - We achieve this by multiplying the DockerResourceGroup.weight with the value from DockerResourceInstallOrder
        and by default using a weight of 100. So
        * Weights 1-10 are reserved
        * Choose weight 11-99 to deploy a resource group before all the "default" resources
        * Choose weight 101+ to deploy a resource group after all the "default" resources
        * Choosing weight 100 has no effect because that is the default install weight
    """
    resource_type_class_name = docker_resource_type.__class__.__name__
    if resource_type_class_name in DockerResourceInstallOrder.keys():
        # logger.debug(
        #     "Resource type: {} | RG Weight: {} | Install weight: {}".format(
        #         resource_type_class_name,
        #         resource_group_weight,
        #         resource_group_weight
        #         * DockerResourceInstallOrder[resource_type_class_name],
        #     )
        # )
        return (
            resource_group_weight * DockerResourceInstallOrder[resource_type_class_name]
        )

    return 5000


def get_docker_resources_from_group(
    docker_resource_group: DockerResourceGroup,
    name_filters: Optional[List[str]] = None,
) -> Optional[List[DockerResourceType]]:
    """Parses the DockerResourceGroup and returns an array of DockerResources
    after applying the filters (if any). This function also flattens any
    List[DockerResourceType] attributes. Eg: we will flatten container resources

    Args:
        docker_resource_group:
        name_filters:
            List of names to filter by

    Returns:
        List[DockerResourceType]: List of filtered and flattened DockerResources
    """

    # List of resources to return, we use the Union type: DockerResourceType
    # to hold all DockerResources
    docker_resources: List[DockerResourceType] = []
    # logger.debug(f"Flattening {docker_resource_group.name}")

    # Now we populate the docker_resources list with the resources
    # we also flatten any list resources
    # This will loop over each key of the DockerResourceGroup model
    # resource = key
    # resource_data = value in the current DockerResourceGroup object
    for resource, resource_data in docker_resource_group.__dict__.items():
        # logger.debug("resource: {}".format(resource))
        # logger.debug("resource_data: {}".format(resource_data))

        # When we check for isinstance(resource_data, DockerResourceBase)
        # we filter out all keys which are not a subclass of the resource_data
        # thereby leaving out only DockerResource types

        # Check if the resource is a single DockerResourceType or a List[DockerResourceType]
        # If it is a List[DockerResourceType], flatten the resources, verify each element
        # of the list is a subclass of DockerResourceBase and add to the _resources list
        if isinstance(resource_data, list):
            for _r in resource_data:
                if isinstance(_r, DockerResourceBase):
                    docker_resources.append(_r)  # type: ignore
        # If its a single resource, verify that the resource is a subclass of
        # DockerResourceBase and add it to the docker_resources list
        elif isinstance(resource_data, DockerResourceBase):
            docker_resources.append(resource_data)  # type: ignore

    return docker_resources


def filter_and_flatten_docker_resource_groups(
    docker_resource_groups: Dict[str, DockerResourceGroup],
    name_filters: Optional[List[str]] = None,
    sort_order: Literal["create", "delete"] = "create",
) -> Optional[List[DockerResourceType]]:
    """This function parses the docker_resource_groups dict and returns a filtered array of
    DockerResources sorted in the order requested. create == install order, delete == reverse
    Desc:
        1. Iterate through each DockerResourceGroup
        2. If group is enabled, get the DockerResources from that group
        3. Return a list of all DockerResources from 2.

    Args:
        docker_resource_groups: Dict[str, DockerResourceGroup]
            Dict of {resource_group_name : DockerResourceGroup}
        name_filters: Filter resource groups by name
        sort_order:

    Returns:
        List[DockerResourceType]: List of filtered DockerResources

    TODO:
        * Implement sorting docker_resource_groups by weight
    """

    # The list of DockerResourceType that will be returned
    filtered_docker_resources: List[DockerResourceType] = []

    # Step 1: Create _docker_resource_list_with_weight
    # A List of Tuples where each tuple is a (DockerResource, Resource Group Weight)
    # This list helps us sort the DockerResources
    # based on their resource group weight using get_install_weight_for_docker_resource
    _docker_resource_list_with_weight: List[Tuple[DockerResourceType, int]] = []
    if docker_resource_groups:
        # Iterate through docker_resource_groups
        for docker_rg_name, docker_rg in docker_resource_groups.items():
            # logger.debug("docker_rg_name: {}".format(docker_rg_name))
            # logger.debug("docker_rg: {}".format(docker_rg))
            # Skip if name matches name_filters
            if name_filters is not None and docker_rg_name in name_filters:
                logger.debug("{} filtered out".format(docker_rg_name))
                continue
            # Only process enabled DockerResourceGroup
            if docker_rg.enabled:
                # Get filtered resources
                # logger.debug("{} is enabled".format(docker_rg_name))
                _docker_resources = get_docker_resources_from_group(
                    docker_rg, name_filters
                )
                # logger.debug(f"_docker_resources: {_docker_resources}")
                if _docker_resources:
                    for _docker_rsrc in _docker_resources:
                        _docker_resource_list_with_weight.append(
                            (_docker_rsrc, docker_rg.weight)
                        )
                    filtered_docker_resources.extend(_docker_resources)

    # Sort the resources in install order
    if sort_order == "delete":
        _docker_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_docker_resource(x[0], x[1]),
            reverse=True,
        )
    else:
        # logger.debug("Sorting _docker_resource_list_with_weight")
        _docker_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_docker_resource(x[0], x[1])
        )

    filtered_docker_resources = [x[0] for x in _docker_resource_list_with_weight]
    # logger.debug("filtered_docker_resources: {}".format(filtered_docker_resources))
    return filtered_docker_resources
