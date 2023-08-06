# import json
# import base64
# from typing import Any, Dict, List, Optional
# from collections import OrderedDict
#
# from google.cloud import container_v1
# from google.oauth2 import service_account
#
# from pak8 import enums, exceptions
# from pak8.conf import Pak8Conf
# from pak8.gcp.conf import Pak8GCPConf, Pak8GCPCredentials
# from pak8.k8s.conf import Pak8K8sConf
# from pak8.gcp.clients.pak8_gke_client import Pak8GKEClient
# from pak8.k8s.pak8_k8s_client import Pak8K8sClient
#
# # from pak8.k8s.api.k8s_resource_group import get_k8s_resource_groups_for_pak8_conf
# from pak8.k8s.api.kubeconfig import create_kubeconfig_resource_for_gke_cluster
# from pak8.k8s.k8s_utils import (
#     get_default_ns_name,
#     get_default_ctx_name,
#     filter_and_flatten_k8s_resource_groups,
#     get_k8s_resources_from_group,
# )
# from pak8.utils.log import logger
# from pak8.utils.common import is_empty
# from pak8.k8s.resources.k8s_resource_group import K8sResourceGroup
# from pak8.k8s.resources.k8s_resource_types import K8sResourceType
# from pak8.k8s.resources.kubeconfig import Kubeconfig
#
#
# class GCPPak8:
#     """The GCPPak8 class is our interface to Google Cloud
#     Initialize this class using a Pak8Conf. This class is designed for quick
#     initialization and lazy loading because the stupid `service_account.Credentials` object can't be pickled.
#     We can't pickle this class and save it for the user, so we're optimizing for quick initialization
#
#     To deploy this Pak8, first call `get_pak8_status()`. This initializes the Pak8 by
#     calling `init_pak8()` (which can be called manually as well).
#
#     Then it is better to use the Pak8GKEClient + Pak8K8sClient to perform any actions.
#     """
#
#     def __init__(
#         self,
#         pak8_conf: Pak8Conf,
#         pak8_gcp_conf: Pak8GCPConf,
#         pak8_k8s_conf: Pak8K8sConf,
#     ):
#
#         if pak8_conf is None or pak8_conf.name is None:
#             raise exceptions.Pak8ConfInvalidException("Invalid Pak8Conf")
#
#         self._pak8_conf: Pak8Conf = pak8_conf
#         self._pak8_gcp_conf: Pak8GCPConf = pak8_gcp_conf
#         self._pak8_k8s_conf: Pak8K8sConf = pak8_k8s_conf
#         self._pak8_name: str = self._pak8_conf.name
#         self._pak8_status: enums.Pak8Status = enums.Pak8Status.PRE_INIT
#         logger.debug("Pak8 Initialized, status: {}".format(self._pak8_status.value))
#
#         # Clients
#         self._pak8_gke_client: Optional[Pak8GKEClient] = None
#         # self._pak8_gcs_client: Optional[Pak8GCSClient] = None
#         # self._pak8_cloudsql_client: Optional[Pak8CloudSQLClient] = None
#         self._pak8_k8s_client: Optional[Pak8K8sClient] = None
#
#         # Pak8 K8s Resources
#         self._k8s_resource_groups: Optional[Dict[str, K8sResourceGroup]] = None
#
#         # GCP Credentials object which is saved because it is used to init all other GCP clients
#         self._credentials: Optional[service_account.Credentials] = None
#
#     @property
#     def pak8_name(self) -> str:
#         return self._pak8_name
#
#     @property
#     def pak8_conf(self) -> Pak8Conf:
#         return self._pak8_conf
#
#     @property
#     def pak8_gke_client(self) -> Optional[Pak8GKEClient]:
#         if self._pak8_gke_client is None:
#             self._init_pak8_gke_client()
#         return self._pak8_gke_client
#
#     # @property
#     # def pak8_gcs_client(self) -> Optional[Pak8GCSClient]:
#     #     if self._pak8_gcs_client is None:
#     #         self._init_pak8_gcs_client()
#     #     return self._pak8_gcs_client
#
#     # @property
#     # def pak8_cloudsql_client(self) -> Optional[Pak8CloudSQLClient]:
#     #     if self._pak8_cloudsql_client is None:
#     #         self._init_pak8_cloudsql_client()
#     #     return self._pak8_cloudsql_client
#
#     def get_pak8_k8s_client(
#         self,
#         refresh: bool = False,
#     ) -> Optional[Pak8K8sClient]:
#         if self._pak8_k8s_client is None or refresh:
#             self._init_pak8_k8s_client()
#         return self._pak8_k8s_client
#
#     def get_k8s_resource_groups(
#         self,
#     ) -> Optional[Dict[str, K8sResourceGroup]]:
#         if is_empty(self._k8s_resource_groups):
#             # self._k8s_resource_groups = get_k8s_resource_groups_for_pak8_conf(
#             #     pak8_conf=self._pak8_conf, pak8_k8s_conf=self._pak8_k8s_conf
#             # )
#             if is_empty(self._k8s_resource_groups):
#                 logger.debug("Could not initialize K8sResourceGroups")
#         return self._k8s_resource_groups
#
#     def init_pak8(self) -> None:
#         """This function must be run before using the Pak8. We defer the initial pak8
#         validation because in the database we can only store the pak8_conf. This is
#         because an object of GCPPak8 class cannot be pickled because of the _credentials
#         variable. service_account.Credentials uses a CFFI class which can't be pickled
#
#         Since it can't be pickled, we only store the pickle of the Pak8Conf and create/init
#         the GCPPak8 for each action - so so bad. So it would really help if our initial validation of the
#         GCPPak8 object was very quick and we lazily initialized only the pieces we needed.
#         This function is the lazy loader for the GCPPak8. It must be run before deploying
#         But we normally call this through the get_pak8_status() function
#
#         Currently we dont run a lot of validation but this function is the
#         place to add the validation in the future
#         """
#         logger.debug("Running Initial Pak8 Validation")
#         if self._pak8_status == enums.Pak8Status.PRE_INIT:
#             if self._pak8_gcp_conf is not None:
#                 self._pak8_status = enums.Pak8Status.INIT_VALIDATION_COMPLETE
#                 logger.debug(f"New Pak8 status: {self._pak8_status}")
#
#     def get_pak8_status(self, refresh: bool = False) -> enums.Pak8Status:
#         """Returns the current Pak8Status
#         Before returning the status, verifies if it needs to be updated.
#         """
#
#         logger.debug("Getting current Pak8 status")
#         # PHASE 0
#         if refresh:
#             self._pak8_status = enums.Pak8Status.PRE_INIT
#             logger.debug(
#                 "Refreshing Pak8 status to {}".format(enums.Pak8Status.PRE_INIT)
#             )
#         # This function sets the status to INIT_VALIDATION_COMPLETE after validating
#         self.init_pak8()
#
#         # PHASE 1
#         # Once the config is validated and initialized, pak8_status == INIT_VALIDATION_COMPLETE
#         # Now we initialize the GKE Client and set the status to READY_TO_CREATE_K8S_CLUSTER
#         # This implies we can move to PHASE 1
#         if self._pak8_status == enums.Pak8Status.INIT_VALIDATION_COMPLETE:
#             try:
#                 init_pak8_gke_client_success = self._init_pak8_gke_client()
#                 if init_pak8_gke_client_success:
#                     self._pak8_status = enums.Pak8Status.READY_TO_CREATE_K8S_CLUSTER
#                     logger.debug(f"New Pak8 status: {self._pak8_status}")
#             except exceptions.Pak8GCPConfInvalidException as e:
#                 logger.exception(e)
#                 return self._pak8_status
#
#         # If pak8_status == READY_TO_CREATE_K8S_CLUSTER, check if the cluster is PROVISIONING OR RUNNING
#         # and set the new status accordingly
#         # If pak8_status == CREATING_K8S_CLUSTER, check if the cluster is RUNNING
#         # and mark_pak8_status = K8S_CLUSTER_AVAILABLE.
#         # If pak8_status == K8S_CLUSTER_AVAILABLE verify that the cluster is still running.
#         if self._pak8_gke_client is not None and self._pak8_status in (
#             enums.Pak8Status.READY_TO_CREATE_K8S_CLUSTER,
#             enums.Pak8Status.CREATING_K8S_CLUSTER,
#             enums.Pak8Status.K8S_CLUSTER_AVAILABLE,
#         ):
#             # Get the cluster state from GCP and update the Pak8Status
#             _gke_cluster_gcp: Optional[container_v1.types.Cluster] = None
#             try:
#                 _gke_cluster_gcp = self._pak8_gke_client.get_gke_cluster_from_gcp(
#                     skip_cache=True
#                 )
#                 if _gke_cluster_gcp is not None:
#                     _gke_cluster_status_str: str = (
#                         container_v1.types.Cluster.Status.Name(_gke_cluster_gcp.status)
#                     )
#                     logger.debug(
#                         "GKE Cluster status: {}".format(_gke_cluster_status_str)
#                     )
#
#                     if _gke_cluster_status_str in (
#                         enums.GKEClusterStatus.PROVISIONING.value,
#                         enums.GKEClusterStatus.RECONCILING.value,
#                     ):
#                         self._pak8_status = enums.Pak8Status.CREATING_K8S_CLUSTER
#
#                     if _gke_cluster_status_str == enums.GKEClusterStatus.RUNNING.value:
#                         self._pak8_status = enums.Pak8Status.K8S_CLUSTER_AVAILABLE
#
#                     if _gke_cluster_status_str == enums.GKEClusterStatus.STOPPING.value:
#                         self._pak8_status = enums.Pak8Status.DELETING_K8S_CLUSTER
#
#                     if _gke_cluster_status_str in (
#                         enums.GKEClusterStatus.ERROR.value,
#                         enums.GKEClusterStatus.DEGRADED.value,
#                     ):
#                         self._pak8_status = enums.Pak8Status.K8S_CLUSTER_ERROR
#
#                     logger.debug(f"New Pak8 status: {self._pak8_status}")
#             except exceptions.GKEClusterNotFoundException as e:
#                 logger.debug("GKEClusterSchema Not found: {}".format(e))
#                 return self._pak8_status
#
#         # PHASE 2
#         # Once the cluster is available, pak8_status == K8S_CLUSTER_AVAILABLE
#         # We can initialize the K8s Client and set the status to READY_TO_DEPLOY_K8S_RESOURCES
#         # This implies we can move to PHASE 2
#         if self._pak8_status == enums.Pak8Status.K8S_CLUSTER_AVAILABLE:
#             try:
#                 if self._pak8_k8s_client is None:
#                     self._init_pak8_k8s_client()
#                 if self._pak8_k8s_client is not None:
#                     self._pak8_status = enums.Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES
#                     logger.debug(f"New Pak8 status: {self._pak8_status}")
#             except (
#                 exceptions.GKEClusterNotFoundException,
#                 exceptions.Pak8K8sConfInvalidException,
#                 exceptions.Pak8KubeconfigException,
#                 exceptions.Pak8GCPCredentialsInvalidException,
#                 exceptions.GCPAuthException,
#             ) as e:
#                 logger.exception(e)
#                 return self._pak8_status
#
#         # If pak8_status == READY_TO_DEPLOY_K8S_RESOURCES, check if app are running, if they are
#         # set pak8_status = K8S_RESOURCES_ACTIVE
#         # if self.pak8_status == enums.Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES:
#         #     try:
#         #         # TODO: Add check that app are running by getting the current status
#         #         self.pak8_status = enums.Pak8Status.K8S_RESOURCES_ACTIVE
#         #         logger.debug(f"New Pak8 status: {self.pak8_status}")
#         #     except Exception as e:
#         #         logger.error(f"Got exception while getting k8s client: {e}")
#         #         pass
#
#         return self._pak8_status
#
#     ######################################################
#     ## K8s
#     ######################################################
#
#     def _init_pak8_k8s_client(self) -> None:
#         _kubeconfig = self.get_kubeconfig()
#         _k8s_resource_groups = self.get_k8s_resource_groups()
#         self._pak8_k8s_client = Pak8K8sClient(
#             pak8_k8s_conf=self._pak8_k8s_conf,
#             kubeconfig=_kubeconfig,
#             k8s_resource_groups=_k8s_resource_groups,
#         )
#
#     def get_k8s_resources_as_dicts(
#         self,
#         kind_filters: Optional[List[str]] = None,
#         name_filters: Optional[List[str]] = None,
#     ) -> List[Dict[str, Any]]:
#
#         k8s_rgs = self.get_k8s_resource_groups()
#         if k8s_rgs is None:
#             logger.debug("No K8sResourceGroups available")
#             return []
#
#         _filtered_k8s_resources: Optional[
#             List[K8sResourceType]
#         ] = filter_and_flatten_k8s_resource_groups(
#             k8s_resource_groups=k8s_rgs,
#             kind_filters=kind_filters,
#             name_filters=name_filters,
#             sort_order="create",
#         )
#         _resources: List[Dict[str, Any]] = []
#         if _filtered_k8s_resources:
#             for resource in _filtered_k8s_resources:
#                 if resource:
#                     _dict = resource.get_k8s_manifest_dict()
#                     if _dict:
#                         _resources.append(_dict)
#
#         return _resources
#
#     def get_k8s_resource_groups_as_dicts(
#         self,
#         kind_filters: Optional[List[str]] = None,
#         name_filters: Optional[List[str]] = None,
#     ) -> Optional[Dict[str, List[Dict[str, Any]]]]:
#
#         # logger.debug("Getting K8sResourceGroups as Dicts")
#         k8s_rgs = self.get_k8s_resource_groups()
#         if k8s_rgs is None:
#             logger.debug("No K8sResourceGroups available")
#             return None
#
#         k8s_rg_dict: Dict[str, List[Dict[str, Any]]] = OrderedDict()
#         for rg_name, k8s_rg in k8s_rgs.items():
#             if not k8s_rg.enabled:
#                 continue
#             _k8s_resources_for_rg: Optional[
#                 List[K8sResourceType]
#             ] = get_k8s_resources_from_group(
#                 k8s_resource_group=k8s_rg,
#                 kind_filters=kind_filters,
#                 name_filters=name_filters,
#             )
#             if _k8s_resources_for_rg is None:
#                 continue
#
#             _k8s_resource_dicts: List[Dict[str, Any]] = []
#             for resource in _k8s_resources_for_rg:
#                 _dict = resource.get_k8s_manifest_dict()
#                 if _dict:
#                     _k8s_resource_dicts.append(_dict)
#
#             if len(_k8s_resource_dicts) > 0:
#                 k8s_rg_dict[rg_name] = _k8s_resource_dicts
#
#         # logger.debug("K8sResourceGroups:\n{}".format(k8s_rg_dict))
#         return k8s_rg_dict
#
#     ######################################################
#     ## GCP
#     ######################################################
#
#     def _get_gcp_credentials(
#         self, refresh_credentials: bool = False
#     ) -> service_account.Credentials:
#
#         # Return credentials if already available
#         if self._credentials:
#             return self._credentials
#
#         _gcp_credentials: Optional[Pak8GCPCredentials] = (
#             self._pak8_gcp_conf.credentials if self._pak8_gcp_conf else None
#         )
#         if _gcp_credentials is None:
#             raise exceptions.Pak8GCPCredentialsInvalidException(
#                 "Pak8GCPCredentials is not available"
#             )
#
#         logger.debug("Creating GCP Credentials")
#         # https://developers.google.com/identity/protocols/googlescopes#containerv1
#         _SCOPES = [
#             "https://www.googleapis.com/auth/cloud-platform",
#             "https://www.googleapis.com/auth/userinfo.email",
#             "https://www.googleapis.com/auth/sqlservice.admin",
#             "https://www.googleapis.com/auth/compute",
#         ]
#         # Generate credentials for this project
#         try:
#             if _gcp_credentials.service_account_key_dict:
#                 logger.debug("Creating credentials using json key")
#                 logger.debug(f"Key: {_gcp_credentials.service_account_key_dict}")
#                 # This part is a little tricky. The format of the key may differ depending on how it is generated.
#                 # Keys generated with the REST API or client libraries have "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE"
#                 # When "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE":
#                 # the privateKeyData returned is a base64-encoded string representation of the TYPE_GOOGLE_CREDENTIALS_FILE value
#                 # so we must decode it and use the decoded value as the credentials instead
#                 # ref issue: https://github.com/googleapis/google-cloud-python/issues/7824#issuecomment-507706448
#
#                 if (
#                     _gcp_credentials.service_account_key_dict.get(
#                         "privateKeyType", None
#                     )
#                     == "TYPE_GOOGLE_CREDENTIALS_FILE"
#                     and "privateKeyData" in _gcp_credentials.service_account_key_dict
#                 ):
#                     _decoded_key_str = base64.b64decode(
#                         _gcp_credentials.service_account_key_dict["privateKeyData"]
#                     )
#                     logger.debug(f"_decoded_key_str type: {type(_decoded_key_str)}")
#                     # logger.debug("_decoded_key_str: {}".format(_decoded_key_str))
#                     _decoded_key = json.loads(_decoded_key_str)
#                     logger.debug(f"_decoded_key type: {type(_decoded_key)}")
#                     logger.debug(f"_decoded_key: {_decoded_key}")
#                     self._credentials = (
#                         service_account.Credentials.from_service_account_info(
#                             _decoded_key,
#                             scopes=_SCOPES,
#                         )
#                     )
#                 else:
#                     # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#                     self._credentials = (
#                         service_account.Credentials.from_service_account_info(
#                             _gcp_credentials.service_account_key_dict,
#                             scopes=_SCOPES,
#                         )
#                     )
#                 logger.debug(f"Credentials: {self._credentials}")
#             elif (
#                 _gcp_credentials.service_account_key_path
#                 and _gcp_credentials.service_account_key_path.exists()
#                 and _gcp_credentials.service_account_key_path.is_file()
#             ):
#                 logger.debug(
#                     f"Creating credentials using: {_gcp_credentials.service_account_key_path}"
#                 )
#                 # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#                 # Why we need the scopes: https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl
#                 self._credentials = (
#                     service_account.Credentials.from_service_account_file(
#                         str(_gcp_credentials.service_account_key_path),
#                         scopes=_SCOPES,
#                     )
#                 )
#
#             if refresh_credentials:
#                 logger.debug(
#                     f"Refreshing Credentials, SVC: {self._credentials.service_account_email}"
#                 )
#                 import google.auth.transport.requests as google_auth_requests
#
#                 http_request = google_auth_requests.Request()
#                 self._credentials.refresh(http_request)
#                 logger.debug("Credentials refreshed")
#         except Exception as e:
#             logger.exception(e)
#             raise exceptions.GCPAuthException("Could not Authenticate with GCP", e)
#
#         return self._credentials
#
#     def _init_pak8_gke_client(self) -> bool:
#
#         if self._pak8_gcp_conf is None:
#             return False
#
#         self._pak8_gke_client = Pak8GKEClient(
#             pak8_gcp_conf=self._pak8_gcp_conf, credentials=self._get_gcp_credentials()
#         )
#         if self._pak8_gke_client is None:
#             logger.error("Could not create Pak8GKEClient")
#             return False
#         return True
#
#     # def _init_pak8_gcs_client(self) -> bool:
#     #
#     #     if self._pak8_gcp_conf is None:
#     #         logger.error("self.pak8_conf.gcp is None")
#     #         raise exceptions.Pak8GCPConfInvalidException("gcp config not provided")
#     #
#     #     _gcs_buckets_list = self._pak8_gcp_conf.gcs_buckets
#     #     if _gcs_buckets_list is None:
#     #         return False
#     #
#     #     logger.debug(f"Initializing Pak8GCSClient: {_gcs_buckets_list}")
#     #     _gcs_buckets: GCSBuckets = GCSBuckets(
#     #         project_id=self._pak8_gcp_conf.project_id, bucket_names=_gcs_buckets_list
#     #     )
#     #
#     #     _credentials: service_account.Credentials = self._get_gcp_credentials()
#     #     if _credentials:
#     #         self._pak8_gcs_client = Pak8GCSClient(_gcs_buckets, _credentials)
#     #         return True
#     #     else:
#     #         logger.error("Could not create GCP Credentials")
#     #         return False
#
#     # def _init_pak8_cloudsql_client(self) -> bool:
#     #
#     #     if self._pak8_gcp_conf is None:
#     #         logger.error("self.pak8_conf.gcp is None")
#     #         raise exceptions.Pak8GCPConfInvalidException("gcp config not provided")
#     #
#     #     _cloudsql_instance_list = self._pak8_gcp_conf.cloudsql
#     #     if _cloudsql_instance_list is None:
#     #         return False
#     #
#     #     logger.debug(f"Initializing Pak8CloudSQLClient: {_cloudsql_instance_list}")
#     #     _cloud_sql_instances: gcp_resources.CloudSQLInstances = (
#     #         gcp_resources.CloudSQLInstances(
#     #             project_id=self._pak8_gcp_conf.project_id,
#     #             instance_ids=_cloudsql_instance_list,
#     #         )
#     #     )
#     #
#     #     _credentials: service_account.Credentials = self._get_gcp_credentials()
#     #     if _credentials:
#     #         self._pak8_cloudsql_client = Pak8CloudSQLClient(
#     #             _cloud_sql_instances, _credentials
#     #         )
#     #         return True
#     #     else:
#     #         logger.error("Could not create GCP Credentials")
#     #         return False
#
#     ######################################################
#     ## K8s Helpers
#     ######################################################
#
#     def get_kubeconfig(self, force_create: bool = False) -> Optional[Kubeconfig]:
#         """Returns the kubeconfig for this Pak8.
#         A GKE Cluster must be available to create a kubeconfig
#
#         Raises:
#             * exceptions.GKEClusterNotFoundException if a GKEClusterSchema is not available
#         """
#         if self._pak8_k8s_conf is None:
#             logger.error("self._pak8_k8s_conf is None")
#             raise exceptions.Pak8K8sConfInvalidException("k8s config not provided")
#
#         logger.debug("Getting Kubeconfig for {}".format(self._pak8_name))
#         _kubeconfig: Optional[Kubeconfig] = None
#
#         if not force_create:
#             # Only read existing kubeconfig if recreate_kubeconfig = False
#             if self._pak8_k8s_conf.kubeconfig_resource is not None:
#                 logger.debug("Kubeconfig provided through kubeconfig_resource")
#                 _kubeconfig = self._pak8_k8s_conf.kubeconfig_resource
#             elif self._pak8_k8s_conf.kubeconfig_dict is not None:
#                 logger.debug("Kubeconfig provided through kubeconfig_dict")
#                 logger.debug("Not yet implemented")
#                 # TODO: Create Kubeconfig from self._pak8_k8s_conf.kubeconfig_dict
#                 _kubeconfig = None  # self._pak8_k8s_conf.kubeconfig_dict
#             elif self._pak8_k8s_conf.kubeconfig_path is not None:
#                 logger.debug("Kubeconfig provided through kubeconfig_path")
#                 logger.debug("Not yet implemented")
#                 _kubeconfig = None
#                 # _kubeconfig = unpickle_object_from_file(
#                 #     self._pak8_k8s_conf.kubeconfig_path, Kubeconfig
#                 # )
#
#         # Create a kubeconfig if the kubeconfig isn't available through
#         # resource, dict or path OR recreate_kubeconfig = True
#         if _kubeconfig is None or force_create:
#
#             if self._pak8_gke_client is None:
#                 raise exceptions.GKEClusterNotFoundException(
#                     "Pak8GKEClient unavailable, cannot create Kubeconfig"
#                 )
#             _gke_cluster_gcp: Optional[
#                 container_v1.types.Cluster
#             ] = self._pak8_gke_client.get_gke_cluster_from_gcp()
#             if _gke_cluster_gcp is None:
#                 raise exceptions.GKEClusterNotFoundException(
#                     "GKEClusterSchema not found~~"
#                 )
#
#             _kubeconfig = create_kubeconfig_resource_for_gke_cluster(
#                 _gke_cluster_gcp,
#                 self._pak8_gke_client.credentials,
#                 self._pak8_k8s_conf.namespace
#                 if self.pak8_conf
#                 and self._pak8_k8s_conf
#                 and self._pak8_k8s_conf.namespace
#                 else get_default_ns_name(self._pak8_name),
#                 self._pak8_k8s_conf.context
#                 if self.pak8_conf
#                 and self._pak8_k8s_conf
#                 and self._pak8_k8s_conf.context
#                 else get_default_ctx_name(self._pak8_name),
#             )
#             if _kubeconfig:
#                 logger.debug("New Kubeconfig Created")
#                 self._pak8_k8s_conf.kubeconfig_resource = _kubeconfig
#                 self._pak8_k8s_conf.kubeconfig_dict = _kubeconfig.dict()
#                 # if self._pak8_k8s_conf.kubeconfig_path:
#                 #     logger.debug(
#                 #         f"Saving Kubeconfig to: {self._pak8_k8s_conf.kubeconfig_path}"
#                 #     )
#                 #     pickle_object_to_file(
#                 #         _kubeconfig, self._pak8_k8s_conf.kubeconfig_path
#                 #     )
#             else:
#                 raise exceptions.Pak8KubeconfigException("Could not create Kubeconfig")
#
#         # logger.info(f"_kubeconfig: {_kubeconfig}")
#         return _kubeconfig
#
#     ######################################################
#     ## Print
#     ######################################################
#
#     # def print_status(self) -> None:
#     #
#     #     print_section_break()
#     #     if self.pak8_cloudsql_client:
#     #         self.pak8_cloudsql_client.print_cloudsql_instance_status()
#     #         print_section_break()
#     #     if self.pak8_gke_client:
#     #         self.pak8_gke_client.print_gke_cluster_status()
#     #         print_section_break()
#     #     try:
#     #         pak8_k8s_client = self.get_pak8_k8s_client()
#     #         if pak8_k8s_client:
#     #             # pak8_k8s_client.show()
#     #             print_section_break()
#     #     except exceptions.GKEClusterNotFoundException as e:
#     #         pass
#
#     # def print_pak8(self, k8s_manifests: bool = False) -> None:
#
#     #     print_section_break()
#     #     print("Pak8 Configuratio:\n{}".format(self.pak8_conf.json(indent=2)))
#     #     print_section_break()
#     #     if self.pak8_gke_client:
#     #         self.pak8_gke_client.print_gke_cluster_config()
#     #         print_section_break()
#     #     if k8s_manifests:
#     #         Pak8K8sClient.print_k8s_resource_groups(self._k8s_resource_groups)
#     #         print_section_break()
#
#     # def print_k8s_resource_groups(
#     #     self,
#     #     kind_filters: Optional[List[str]] = None,
#     #     name_filters: Optional[List[str]] = None,
#     #     as_yaml: Optional[bool] = True,
#     # ) -> None:
#
#     #     print_section_break()
#     #     if self._k8s_resource_groups:
#     #         Pak8K8sClient.print_k8s_resource_groups(self._k8s_resource_groups)
#     #         print_section_break()
