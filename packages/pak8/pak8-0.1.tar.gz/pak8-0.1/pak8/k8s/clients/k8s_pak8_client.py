from collections import defaultdict
from typing import Any, Dict, List, Optional, Type, Set, cast

from pak8 import exceptions
from pak8.k8s.conf.k8s_pak8_conf import Pak8K8sConf
from pak8.conf.constants import (
    NAMESPACE_RESOURCE_GROUP_KEY,
    DEFAULT_K8S_NAMESPACE,
    RBAC_RESOURCE_GROUP_KEY,
    DEFAULT_K8S_SERVICE_ACCOUNT,
)
from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.k8s_utils import (
    filter_and_flatten_k8s_resource_groups,
    dedup_resource_types,
)
from pak8.utils.log import logger
from pak8.k8s.resources.kubeconfig import Kubeconfig
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.k8s_resource_group import K8sResourceGroup
from pak8.k8s.resources.k8s_resource_types import K8sResourceType


class Pak8K8sClient:
    """This class interacts with the Kubernetes API

    Each Pak8K8sClient instance is attached to 1 and only 1 Pak8.
    Pak8K8sClient should only be initialized after a K8s Cluster is available.
    """

    def __init__(
        self,
        pak8_k8s_conf: Pak8K8sConf,
        kubeconfig: Optional[Kubeconfig],
        k8s_resource_groups: Optional[Dict[str, K8sResourceGroup]],
    ):

        if pak8_k8s_conf is None:
            raise exceptions.Pak8K8sConfInvalidException("Pak8K8sConf not provided")
        logger.debug(f"Creating Pak8K8sClient")

        self._pak8_k8s_conf: Pak8K8sConf = pak8_k8s_conf
        self._kubeconfig: Optional[Kubeconfig] = kubeconfig
        self._kubeconfig_dict: Optional[Dict[str, Any]] = None
        if self._kubeconfig:
            # We set `by_alias=True` on the pydantic schema because in Kubeconfig, the field
            # names have '-' and in python we need to store the field name with '_'
            # Ref: https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict
            self._kubeconfig_dict = self._kubeconfig.dict(by_alias=True)
        self._k8s_api: Optional[K8sApi] = None
        # _k8s_resource_groups is THE MAIN COLLECTION of K8s Resources that will be managed by this Pak8K8sClient.
        # It is a dictionary of {resource_group_name : K8sResourceGroup}
        self._k8s_resource_groups: Optional[
            Dict[str, K8sResourceGroup]
        ] = k8s_resource_groups

    ######################################################
    ## Pak8K8sClient Properties
    ######################################################

    @property
    def kubeconfig(self) -> Optional[Kubeconfig]:
        return self._kubeconfig

    @kubeconfig.setter
    def kubeconfig(self, kconf: Optional[Kubeconfig]) -> None:
        if kconf:
            self._kubeconfig = kconf
            self._kubeconfig_dict = self._kubeconfig.dict(by_alias=True)

    @property
    def k8s_api(self) -> Optional[K8sApi]:
        if self._k8s_api is None:
            self._init_k8s_api()
        return self._k8s_api

    @property
    def k8s_resource_groups(
        self,
    ) -> Optional[Dict[str, K8sResourceGroup]]:
        return self._k8s_resource_groups

    @k8s_resource_groups.setter
    def k8s_resource_groups(
        self, k8s_rgs: Optional[Dict[str, K8sResourceGroup]]
    ) -> None:
        if k8s_rgs:
            self._k8s_resource_groups = k8s_rgs

    ######################################################
    ## K8sApi
    ######################################################

    def _init_k8s_api(self) -> Optional[K8sApi]:
        """Creates an K8s ApiClient which can be used with any API object."""

        import kubernetes

        logger.debug("Creating K8sApi")
        if self._kubeconfig_dict is None:
            logger.error(f"No kubeconfig available")
            return None

        # logger.debug("Creating K8sApi with: {}".format(self._kubeconfig_dict))
        configuration = kubernetes.client.Configuration()
        loader = kubernetes.config.kube_config.KubeConfigLoader(
            config_dict=self._kubeconfig_dict
        )
        loader.load_and_set(configuration)
        kubernetes.client.Configuration.set_default(configuration)
        _k8s_api_client = kubernetes.client.ApiClient(configuration=configuration)

        logger.debug("K8sApi Created")
        self._k8s_api = K8sApi(_k8s_api_client)
        return self._k8s_api

    def get_k8s_namespace_to_use(self) -> str:
        if self._k8s_resource_groups is None:
            return DEFAULT_K8S_NAMESPACE
        ns_rg: K8sResourceGroup = self._k8s_resource_groups[
            NAMESPACE_RESOURCE_GROUP_KEY
        ]
        if ns_rg and ns_rg.enabled and ns_rg.ns is not None:
            return ns_rg.ns.get_resource_name()
        return DEFAULT_K8S_NAMESPACE

    def get_k8s_service_account_to_use(self) -> str:
        if self._k8s_resource_groups is None:
            return DEFAULT_K8S_SERVICE_ACCOUNT
        rbac_rg: K8sResourceGroup = self._k8s_resource_groups[RBAC_RESOURCE_GROUP_KEY]
        if rbac_rg and rbac_rg.enabled and rbac_rg.sa is not None:
            return rbac_rg.sa.get_resource_name()
        return DEFAULT_K8S_SERVICE_ACCOUNT

    ######################################################
    ## Describe Resources
    ######################################################

    def print_k8s_resources(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
        op_format: str = "yaml",  # yaml or json
    ) -> None:

        if op_format not in ("yaml", "json"):
            print(f"Output format {op_format} not supported")
            return

        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return

        self.print_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            as_yaml=(op_format == "yaml"),
        )

    @staticmethod
    def print_k8s_resource_groups(
        k8s_resource_groups: Dict[str, K8sResourceGroup],
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
        as_yaml: Optional[bool] = True,
    ) -> None:

        print(
            "Resources: {}/{}".format(
                kind_filters if kind_filters else "*",
                name_filters if name_filters else "*",
            )
        )
        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="create",
        )
        _resources: List[str] = []
        if _filtered_k8s_resources:
            for resource in _filtered_k8s_resources:
                if resource:
                    if as_yaml:
                        _yml = resource.get_k8s_manifest_yaml()
                        if _yml:
                            _resources.append(_yml)
                    else:
                        _json = resource.get_k8s_manifest_json(indent=2)
                        if _json:
                            _resources.append(_json)

        if _resources:
            if as_yaml:
                print("---")
                print("---\n".join(_resources))
            else:
                print("\n".join(_resources))

    ######################################################
    ## Create Resources
    ######################################################

    def create_namespace_resource(self) -> bool:
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return False
        k8s_api = self.k8s_api

        ns_rg: K8sResourceGroup = self._k8s_resource_groups[
            NAMESPACE_RESOURCE_GROUP_KEY
        ]
        if ns_rg and ns_rg.enabled and ns_rg.ns is not None and k8s_api is not None:
            return ns_rg.ns.create_if(k8s_api=k8s_api)
        return False

    def create_rbac_resources(self) -> bool:
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return False
        k8s_api = self.k8s_api

        rbac_rg: K8sResourceGroup = self._k8s_resource_groups[RBAC_RESOURCE_GROUP_KEY]
        if rbac_rg and rbac_rg.enabled and k8s_api is not None:
            _active_ns = self.get_k8s_namespace_to_use()
            if rbac_rg.sa is not None:
                rbac_rg.sa.create_if(k8s_api=k8s_api, namespace=_active_ns)
            if rbac_rg.cr is not None:
                rbac_rg.cr.create_if(k8s_api=k8s_api, namespace=_active_ns)
            if rbac_rg.crb is not None:
                rbac_rg.crb.create_if(k8s_api=k8s_api, namespace=_active_ns)
            # TODO: return True only if the k8s_resources were created
            return True
        return False

    def create_resources(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> None:

        if self._k8s_api is None:
            logger.debug("No K8sApi available")
            return
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return

        _active_ns = self.get_k8s_namespace_to_use()
        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="create",
        )
        if _filtered_k8s_resources:
            for resource in _filtered_k8s_resources:
                logger.debug(f"Creating: {resource.metadata.name} | NS: {_active_ns}")
                if resource and self.k8s_api:
                    resource.create_if(k8s_api=self.k8s_api, namespace=_active_ns)

    ######################################################
    ## Delete Resources
    ######################################################

    def delete_resources(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> None:

        if self._k8s_api is None:
            logger.debug("No K8sApi available")
            return
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return

        _active_ns = self.get_k8s_namespace_to_use()
        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="delete",
        )
        if _filtered_k8s_resources:
            for resource in _filtered_k8s_resources:
                logger.debug(f"Deleting: {resource.metadata.name} | NS: {_active_ns}")
                if resource and self.k8s_api:
                    resource.delete_if(k8s_api=self.k8s_api, namespace=_active_ns)

    ######################################################
    ## Update Resources
    ######################################################

    def update_resources(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> None:

        if self._k8s_api is None:
            logger.debug("No K8sApi available")
            return
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return

        _active_ns = self.get_k8s_namespace_to_use()
        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="create",
        )
        if _filtered_k8s_resources:
            for resource in _filtered_k8s_resources:
                logger.debug(f"Updating: {resource.metadata.name}")
                if resource and self.k8s_api:
                    resource.update_if(k8s_api=self.k8s_api, namespace=_active_ns)

    ######################################################
    ## List Resources
    ######################################################

    def get_active_resource_classes(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> Optional[Set[Type[K8sResourceBase]]]:
        """This function scans all K8sResourceGroups under this client and
        returns a set of different types of K8sResource(s) as a set of classes.

        When do we need this:
        Let's say your app has 1 Deployment, 1 Pod and 1 Service. You deploy it and now want
        to see the different types of objects running on your cluster on your cluster.
        To do that you need to query the API for each and every resource type to see if there are any running objects of that type.
        We use this function to filter & dedup the resource types this K8s client is managing.
        This way we don't end up scanning everything.

        Also super useful when you want to just see Deployments running, faster responses.
        """
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return None

        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="create",
        )
        return dedup_resource_types(_filtered_k8s_resources)

    def get_active_resources(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> Optional[Dict[str, List]]:
        """Reads the K8s Cluster and returns all active k8s_resources which satisfy the filters."""

        from kubernetes.client.rest import ApiException

        active_resource_classes: Optional[
            Set[Type[K8sResourceBase]]
        ] = self.get_active_resource_classes(kind_filters, name_filters)

        if active_resource_classes is None:
            return None

        _active_ns = self.get_k8s_namespace_to_use()
        active_k8s_objects: Dict[str, List] = defaultdict(list)
        for resource_class in active_resource_classes:
            resource_type: str = resource_class.__name__
            logger.debug(f"Resource Type: {resource_type}")
            try:
                _active_objects: Optional[List[Any]] = resource_class.read_from_cluster(
                    k8s_api=cast(K8sApi, self.k8s_api), namespace=_active_ns
                )
                if _active_objects is not None and isinstance(_active_objects, list):
                    active_k8s_objects[resource_type] = _active_objects
            except ApiException as e:
                logger.debug(
                    f"ApiException while getting {resource_type}, reason: {e.reason}"
                )

        return active_k8s_objects

    def print(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
        as_yaml: Optional[bool] = True,
    ) -> None:

        active_k8s_objects: Optional[Dict[str, List]] = self.get_active_resources(
            kind_filters, name_filters
        )
        if active_k8s_objects:
            for _r_type, active_resources in active_k8s_objects.items():
                print("\n{}:".format(_r_type))
                for _r in active_resources:
                    print("\t- {}".format(_r))

    ######################################################
    ## Debug
    ######################################################

    def debug(
        self,
        kind_filters: Optional[List[str]] = None,
        name_filters: Optional[List[str]] = None,
    ) -> None:

        if self._k8s_api is None:
            logger.debug("No K8sApi available")
            return
        if self._k8s_resource_groups is None:
            logger.debug("No K8sResourceGroups available")
            return
        _filtered_k8s_resources: Optional[
            List[K8sResourceType]
        ] = filter_and_flatten_k8s_resource_groups(
            k8s_resource_groups=self._k8s_resource_groups,
            kind_filters=kind_filters,
            name_filters=name_filters,
            sort_order="create",
        )
        if _filtered_k8s_resources:
            for resource in _filtered_k8s_resources:
                logger.debug(f"Resource: {resource.metadata.name}")
                if resource and self.k8s_api:
                    resource.debug()

    ######################################################
    ## Helpers
    ######################################################

    # def _debug_log(self, msg: Optional[str] = None) -> None:
    #     if msg:
    #         logger.debug(msg)
    #     kubeconfig_avl = True if self._kubeconfig else False
    #     k8s_api_avl = True if self.k8s_api else False
    #     logger.debug(f"Kubeconfig Available  : {kubeconfig_avl}")
    #     logger.debug(f"K8s_api Available  : {k8s_api_avl}")
    #
    # def verify_client(self) -> None:
    #     """Helper method to verify that we are good to perform K8s operaitons.
    #
    #     Raises:
    #         K8sClientException if something is wrong
    #     """
    #     if self._kubeconfig and self._k8s_api:
    #         pass
    #     else:
    #         self._debug_log()
    #         raise exceptions.Pak8K8sClientException("Pak8K8sClient unavailable")
