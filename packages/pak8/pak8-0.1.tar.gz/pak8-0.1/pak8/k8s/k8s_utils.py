from typing import Dict, List, Optional, Type, Tuple, Set

from typing_extensions import Literal

from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.k8s_resource_group import K8sResourceGroup
from pak8.k8s.resources.k8s_resource_types import (
    K8sResourceAliasToTypeMap,
    K8sResourceInstallOrder,
    K8sResourceType,
)
from pak8.utils.common import isinstanceany
from pak8.utils.log import logger


def get_default_ns_name(pak8_name: str) -> str:
    return "{}-ns".format(pak8_name)


def get_default_ctx_name(pak8_name: str) -> str:
    return "{}-ctx".format(pak8_name)


def get_default_sa_name(pak8_name: str) -> str:
    return "{}-sa".format(pak8_name)


def get_default_cr_name(pak8_name: str) -> str:
    return "{}-cr".format(pak8_name)


def get_default_crb_name(pak8_name: str) -> str:
    return "{}-crb".format(pak8_name)


def get_default_pod_name(group_name: str) -> str:
    return "{}-pod".format(group_name)


def get_default_container_name(group_name: str) -> str:
    return "{}-container".format(group_name)


def get_default_svc_name(group_name: str) -> str:
    return "{}-svc".format(group_name)


def get_default_deploy_name(group_name: str) -> str:
    return "{}-deploy".format(group_name)


def get_default_configmap_name(group_name: str) -> str:
    return "{}-cm".format(group_name)


def get_default_secret_name(group_name: str) -> str:
    return "{}-secret".format(group_name)


# def get_default_volume_name(group_name: str) -> str:
#     return "{}-volume".format(group_name)


# def get_default_pvc_name(group_name: str) -> str:
#     return "{}-pvc".format(group_name)


def get_default_rbac_rg_name(pak8_name: str) -> str:
    return "{}-rbac".format(pak8_name)


def dedup_resource_types(
    k8s_resources: Optional[List[K8sResourceType]] = None,
) -> Optional[Set[Type[K8sResourceBase]]]:
    """Takes a list of K8sResources and returns a Set of K8sResource classes.
    Each K8sResource classes is represented by the Type[resources.K8sResourceBase] type.
    From python docs:
        A variable annotated with Type[K8sResourceBase] may accept values that are classes.
        Acceptable classes are the K8sResourceBase class + subclasses.
    """
    if k8s_resources:
        active_resource_types: Set[Type[K8sResourceBase]] = set()
        for resource in k8s_resources:
            active_resource_types.add(resource.__class__)
            # logger.debug(f"Gathering: {resource.get_resource_name()}")
            # logger.debug(f"Resource Type: {resource_type}")
        logger.debug("Active Resource Types: {}".format(active_resource_types))
        return active_resource_types
    return None


def get_k8s_resources_from_group(
    k8s_resource_group: K8sResourceGroup,
    kind_filters: Optional[List[str]] = None,
    name_filters: Optional[List[str]] = None,
) -> Optional[List[K8sResourceType]]:
    """Parses the K8sResourceGroup and returns an array of K8s Resources
    after applying the filters (if any). This function also flattens any
    List[K8sResourceType] attributes. Eg: we will flatten pvc, cm, secret and
    storage_class resources.

    Args:
        k8s_resource_group:
        kind_filters:
            List of kind str values to filter by, check K8sResourceAliasToTypeMap.
        name_filters:
            List of K8sResourceGroup names to filter by. Useful when only wanting
            "ns", "rbac", "zeus" resources

    Returns:
        List[K8sResourceType]: List of filtered and flattened K8s Resources
    """

    # List of resources to return, we use the Union type: K8sResourceType
    # to hold all K8s Resources
    k8s_resources: List[K8sResourceType] = []

    ## APPLY FILTERS

    # Name filters are simple, if the K8sResourceGroup name does not match
    # the filter, we stop processing.
    if name_filters:
        if k8s_resource_group.name not in name_filters:
            return k8s_resources

    # logger.info(f"Found {k8s_resource_group.name}")
    # When filtering by kind, for each resource in the K8sResourceGroup we check if the
    # Resource is an instance of one of the Types in _kind_filter
    # This makes filtering more deterministic. On the flipside, it also ensures that
    # we control what "kind" str maps to which Resource Type. Eg: ns maps to resources.Namespace
    # This mapping is available at: K8sResourceAliasToTypeMap
    _kind_filter: List[Type[K8sResourceBase]] = []
    if kind_filters:
        for k in kind_filters:
            _kind_str_to_type = K8sResourceAliasToTypeMap.get(k.lower(), None)
            if _kind_str_to_type:
                _kind_filter.append(_kind_str_to_type)

    # logger.info(f"_kind_filter: {_kind_filter}")
    # logger.info(f"name_filters: {name_filters}")

    # Apply filters and flatten any resources which are accepted as a list
    for resource, resource_data in k8s_resource_group.__dict__.items():
        # First check if the resource_data is active for this K8sResourceGroup
        if resource_data is not None:
            # Check if the resource is a single K8sResourceType or a List[K8sResourceType]
            _resources: List[K8sResourceType] = []
            # If its a single resource, verify that the resource is a subclass of
            # K8sResourceBase and add it to the _resources list
            if isinstance(resource_data, K8sResourceBase):
                _resources.append(resource_data)  # type: ignore
            # If its a List[K8sResourceType], flatten the resources, verify each element
            # of the list is a subclass of K8sResourceBase and add to the _resources list
            elif isinstance(resource_data, list):
                for _r in resource_data:
                    if isinstance(_r, K8sResourceBase):
                        _resources.append(_r)  # type: ignore

            # Filter elements of _resources and add to k8s_resources if they match the filter
            for _resource in _resources:
                # Apply _kind_filter, if the _resource is not an instance of one of the
                # _kind_filter resources - do not add to the k8s_resources list.
                if _kind_filter and not isinstanceany(_resource, _kind_filter):
                    continue
                k8s_resources.append(_resource)
    return k8s_resources


def get_install_weight_for_k8s_resource(
    k8s_resource_type: K8sResourceType, resource_group_weight: int = 100
) -> int:
    """Function which takes a K8sResource and resource_group_weight and returns the install
    weight for that resource.

    Understanding install weights for K8s Resources:

    - Each K8s Resource in a Pak8 gets an install weight, which determines the order for installing that particular resource.
    - By default, K8s resources are installed in the order determined by the K8sResourceInstallOrder dict.
        The K8sResourceInstallOrder dict ensures namespaces/service accounts are applied before deployments
    - We can also provide a weight to the K8sResourceGroup, that weight determines the install order for all resources within
        that resource group as compared to other resource groups.
    - We achieve this by multiplying the K8sResourceGroup.weight with the value from K8sResourceInstallOrder
        and by default using a weight of 100. So
        * Weights 1-10 are reserved
        * Choose weight 11-99 to deploy a resource group before all the "default" resources
        * Choose weight 101+ to deploy a resource group after all the "default" resources
        * Choosing weight 100 has no effect because that is the default install weight
    """
    resource_type_name = k8s_resource_type.__class__.__name__
    if resource_type_name in K8sResourceInstallOrder.keys():
        logger.info(
            "Resource type: {} | RG Weight: {} | Install weight: {}".format(
                resource_type_name,
                resource_group_weight,
                resource_group_weight * K8sResourceInstallOrder[resource_type_name],
            )
        )
        return resource_group_weight * K8sResourceInstallOrder[resource_type_name]

    return 5000


def filter_and_flatten_k8s_resource_groups(
    k8s_resource_groups: Dict[str, K8sResourceGroup],
    kind_filters: Optional[List[str]] = None,
    name_filters: Optional[List[str]] = None,
    sort_order: Literal["create", "delete"] = "create",
) -> Optional[List[K8sResourceType]]:
    """This function parses the k8s_resource_groups dict and returns a filtered array of
    K8s Resources sorted in the order requested. create == install order, delete == reverse
    Desc:
        1. Iterate through each K8sResourceGroup
        2. If enabled, get the K8s Resources from that group which match the filters
        2. Return a list of all K8s Resources from 2.

    Args:
        sort_order:
        k8s_resource_groups: Dict[str, resources.K8sResourceGroup]
            Dict of {resource_group_name : K8sResourceGroup}
        kind_filters: Optional[List[str]]
            List of kind str values to filter by, check K8sResourceAliasToTypeMap.
        name_filters: Optional[List[str]]
            List of K8sResourceGroup names to filter by. Useful when only wanting
            "ns", "rbac", "zeus" resources

    Returns:
        List[K8sResourceType]: List of filtered K8s Resources

    TODO:
        * Implement sorting k8s_resource_groups by weight
    """

    # _k8s_resource_list_with_weight: A List of Tuples where each tuple is a
    # (K8s Resource, Resource Group Weight)
    # The reason for creating this list is so that we can sort the K8sResources
    # based on their resource group weight using get_install_weight_for_k8s_resource
    _k8s_resource_list_with_weight: List[Tuple[K8sResourceType, int]] = []
    filtered_k8s_resources: List[K8sResourceType] = []
    if k8s_resource_groups:
        # Iterate through k8s_resource_groups
        for k8s_rg_name, k8s_rg in k8s_resource_groups.items():
            # Only process enabled K8sResourceGroup
            if k8s_rg.enabled:
                # Get filtered resources
                _k8s_resources = get_k8s_resources_from_group(
                    k8s_rg, kind_filters, name_filters
                )
                # logger.debug(f"Got: {_k8s_resources}")
                if _k8s_resources:
                    for _k8s_rsrc in _k8s_resources:
                        _k8s_resource_list_with_weight.append(
                            (_k8s_rsrc, k8s_rg.weight)
                        )
                    # filtered_k8s_resources.extend(_k8s_resources)

    # Sort the resources in install order
    if sort_order == "delete":
        _k8s_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_k8s_resource(x[0], x[1]), reverse=True
        )
    else:
        # logger.debug("Sorting _k8s_resource_list_with_weight")
        _k8s_resource_list_with_weight.sort(
            key=lambda x: get_install_weight_for_k8s_resource(x[0], x[1])
        )

    filtered_k8s_resources = [x[0] for x in _k8s_resource_list_with_weight]
    # logger.debug("filtered_k8s_resources: {}".format(filtered_k8s_resources))
    return filtered_k8s_resources
