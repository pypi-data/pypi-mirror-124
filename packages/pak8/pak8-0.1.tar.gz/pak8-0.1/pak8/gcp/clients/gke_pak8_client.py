# import json
# import time
# from collections import OrderedDict
#
# from typing import Any, Dict, List, Optional, Tuple
#
# import google.api_core.exceptions as gcp_exception
# from google.cloud import container_v1
# from google.oauth2 import service_account
# from google.protobuf.json_format import MessageToDict
#
# from pak8 import enums, exceptions
# import pak8.gcp.resources as gcp_resources
# from pak8.gcp.conf.gcp_conf import Pak8GCPConf
# from pak8.gcp.api.gke.gke_cluster import (
#     create_gke_cluster_config,
# )
# from pak8.utils.log import logger
#
#
# class Pak8GKEClient:
#     """This class interacts with the Google Kubernetes Engine using ClusterManagerV1
#     https://googleapis.dev/python/container/latest/gapic/v1/api.html#module-google.cloud.container_v1
#
#     Each Pak8GKEClient instance is attached to 1 and only 1 Pak8.
#     """
#
#     def __init__(
#         self,
#         pak8_gcp_conf: Pak8GCPConf,
#         credentials: service_account.Credentials,
#     ):
#
#         if pak8_gcp_conf is None or pak8_gcp_conf.gke is None:
#             raise exceptions.Pak8GKEClientException("CreateGkeClusterData not provided")
#         if credentials is None:
#             raise exceptions.Pak8GKEClientException("Credentials not provided")
#         logger.debug(f"Creating Pak8GKEClient for cluster: {pak8_gcp_conf.gke.name}")
#
#         self._pak8_gcp_conf: Pak8GCPConf = pak8_gcp_conf
#         # The _gke_cluster holds the data required to create this GKEClusterSchema.
#         # The gcp_resources.GKEClusterSchema schema should contain all information required
#         self._gke_cluster: gcp_resources.gke.GKECluster = (
#             self.create_gke_cluster_resource(pak8_gcp_conf=pak8_gcp_conf)
#         )
#         # A Credentials Object which will be used to create a ClusterManagerClient
#         # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#         self._credentials: service_account.Credentials = credentials
#         # The ClusterManagerClient is the API for GKE.
#         # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient
#         self._gcp_cluster_manager: container_v1.ClusterManagerClient = (
#             container_v1.ClusterManagerClient(credentials=credentials)
#         )
#         # The Cluster Output from GCP.
#         # https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
#         # TODO: Create/Use gcp_resources.GKEClusterOutput instead of container_v1.types.Cluster
#         self._gke_cluster_gcp: Optional[container_v1.types.Cluster] = None
#         # If we create this cluster, the CREATE_CLUSTER Operation
#         # https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Operation
#         self._create_gke_cluster_op: Optional[container_v1.types.Operation] = None
#         self._server_config: Optional[container_v1.types.ServerConfig] = None
#
#         self._cluster_id = self._gke_cluster.gke_cluster_config.name
#         self._project_id = self._gke_cluster.project_id
#         self._zone = self._gke_cluster.zone
#
#         # Verify Pak8GKEClient is initialized correctly.
#         self._verify_client()
#
#     ######################################################
#     ## Pak8GKEClient Properties
#     ######################################################
#
#     @property
#     def gke_cluster(self) -> gcp_resources.gke.GKECluster:
#         return self._gke_cluster
#
#     @property
#     def credentials(self) -> service_account.Credentials:
#         return self._credentials
#
#     @property
#     def gke_cluster_name(self) -> str:
#         return self._cluster_id
#
#     @property
#     def project_id(self) -> str:
#         return self._project_id
#
#     @property
#     def zone(self) -> str:
#         return self._zone
#
#     ######################################################
#     ## Initialization functions
#     ######################################################
#
#     @staticmethod
#     def create_gke_cluster_resource(pak8_gcp_conf: Pak8GCPConf):
#
#         if pak8_gcp_conf.gke is None:
#             raise exceptions.Pak8GKEClientException("CreateGkeClusterData not provided")
#         gke_cluster_config: gcp_resources.gke.GKEClusterConfig = (
#             create_gke_cluster_config(pak8_gcp_conf.gke)
#         )
#         return gcp_resources.gke.GKECluster(
#             project_id=pak8_gcp_conf.project_id,
#             zone=pak8_gcp_conf.zone,
#             gke_cluster_config=gke_cluster_config,
#         )
#
#     ######################################################
#     ## GET data from GKE API
#     ######################################################
#
#     def get_gke_cluster_from_gcp(
#         self, skip_cache: bool = False
#     ) -> Optional[container_v1.types.Cluster]:
#         """Returns the GKE cluster for this Pak8 if available.
#         Uses the cached version unless skip_cache = True
#
#         References:
#             * GKE: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster
#             * Type: https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
#         """
#
#         # Return the cached version if available
#         if self._gke_cluster_gcp and not skip_cache:
#             return self._gke_cluster_gcp
#         self._verify_client()
#
#         # If a cluster is not available or skip_cache = True, get the cluster from GCP
#         logger.debug(f"Getting Cluster: {self._cluster_id}")
#         try:
#             _cluster: container_v1.types.Cluster = (
#                 self._gcp_cluster_manager.get_cluster(
#                     project_id=self._project_id,
#                     zone=self._zone,
#                     cluster_id=self._cluster_id,
#                 )
#             )
#             self._gke_cluster_gcp = _cluster
#         except (gcp_exception.PermissionDenied, gcp_exception.NotFound) as e:
#             logger.error(
#                 "Caught exception while trying to get cluster from GCP: {}".format(
#                     e.message
#                 )
#             )
#             raise exceptions.GKEClusterNotFoundException(e.message)
#
#         # logger.info(f"cluster type: {type(self._gke_cluster_gcp)}")
#         # logger.info(f"cluster: {self._gke_cluster_gcp}")
#         return self._gke_cluster_gcp
#
#     def wait_for_operation(
#         self,
#         operation_id: str,
#         wait_for_status: enums.GKEOperationStatus = enums.GKEOperationStatus.DONE,
#         timeout_sec: int = 3600,
#         ping_interval_sec: int = 30,
#     ) -> Tuple[bool, Optional[container_v1.types.Operation]]:
#         """Waits for operation_id to reach wait_for_status (default: DONE)
#         Returns (operation_successful, types.Operation)
#         """
#
#         logger.debug(f"Waiting for {operation_id} to be {wait_for_status.value}")
#         # Start a timer
#         start = time.time()
#         # Break if time elapsed > timeout
#         while (time.time() - start) < timeout_sec:
#             # Check if the create cluster operation is DONE
#             _op: Optional[
#                 container_v1.types.Operation
#             ] = self._get_gke_operation_from_gcp(operation_id)
#             if _op:
#                 # https://github.com/protocolbuffers/protobuf/blob/master/python/google/protobuf/internal/enum_type_wrapper.py#L53
#                 _op_status: str = container_v1.types.Operation.Status.Name(_op.status)
#                 if _op_status:
#                     logger.debug(f"Operation Status: {_op_status}")
#                     if _op_status == enums.GKEOperationStatus.RUNNING.value:
#                         logger.debug(
#                             f"Operation Running, checking again in {ping_interval_sec} seconds"
#                         )
#                         time.sleep(ping_interval_sec)
#                     elif _op_status == wait_for_status.value:
#                         logger.debug(f"Operation is {wait_for_status.value}")
#                         return (True, _op)
#                     else:
#                         logger.error("Encountered an issue while waiting for operation")
#                         return (False, None)
#             else:
#                 logger.error("Could not parse Operation")
#                 break
#         return (False, None)
#
#     def _get_gke_operations_from_gcp(
#         self,
#         gke_operation_type: Optional[enums.GKEOperationType] = None,
#         gke_operation_status: Optional[enums.GKEOperationStatus] = None,
#     ) -> Optional[List[Dict[str, Any]]]:
#         """Returns a list of all GKE operations in this project.
#         From the GKE API, we get a container_v1.types.ListOperationsResponse message.
#         This ListOperationsResponse message is then converted to a Dict
#         using google.protobuf.json_format.MessageToDict
#
#         We return the `operations` variable from the Dict of ListOperationsResponse.
#
#         TODO:
#             * Wrap in try/catch
#         References:
#             * GKE: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/ListOperationsResponse
#             * Type: https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.ListOperationsResponse
#         """
#
#         self._verify_client()
#
#         # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.list_operations
#         __list_operations_response: container_v1.types.ListOperationsResponse = (
#             self._gcp_cluster_manager.list_operations(
#                 project_id=self._project_id,
#                 zone=self._zone,
#             )
#         )
#         list_operations_response = MessageToDict(__list_operations_response)
#         # operations has type List[Operation]
#         # where Operation: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.operations#Operation
#         operations = list_operations_response.get("operations", None)
#         logger.info(f"operations type: {type(operations)}")
#         logger.info(f"operations: {operations}")
#         return operations
#
#     def _get_gke_operation_from_gcp(
#         self,
#         operation_id: str,
#         # skip_cache: bool = False
#     ) -> Optional[container_v1.types.Operation]:
#         """Queries the GKE API for the Operation.
#         From the GKE API, we get a container_v1.types.Operation message.
#
#         TODO:
#             * Cache this response and implement skip_cache
#
#         References:
#             * GKE: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.operations#Operation
#             * Type: https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Operation
#         """
#         self._verify_client()
#         # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.get_operation
#         _operation: container_v1.types.Operation = (
#             self._gcp_cluster_manager.get_operation(
#                 project_id=self._project_id,
#                 zone=self._zone,
#                 operation_id=operation_id,
#             )
#         )
#         # logger.debug(f"_operation type: {type(_operation)}")
#         # logger.debug(f"_operation: {_operation}")
#         return _operation
#
#     def get_gke_server_config(
#         self, skip_cache: bool = False
#     ) -> container_v1.types.ServerConfig:
#         """Returns the Server Config for the GKE cluster.
#         Uses the cached version unless skip_cache = True
#
#         TODO:
#             * Output should be gcp_resources.ServerConfigOutput
#         References:
#             * https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.ServerConfig
#         """
#         try:
#             if self._server_config and not skip_cache:
#                 return self._server_config
#             self._verify_client()
#
#             _server_config: container_v1.types.ServerConfig = (
#                 self._gcp_cluster_manager.get_server_config(
#                     project_id=self._project_id,
#                     zone=self._zone,
#                 )
#             )
#             self._server_config = _server_config
#             # logger.info(f"_server_config type: {type(self._server_config)}")
#             # logger.info(f"_server_config: {self._server_config}")
#             return self._server_config
#         except Exception as e:
#             # self._debug_log(f"Could not get server config: {self._cluster_id}")
#             raise exceptions.Pak8GKEClientException("Could not get server config")
#
#     def get_valid_gke_node_versions_from_gcp(self) -> Optional[List[str]]:
#         ## https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.ServerConfig.valid_node_versions
#         server_config = self.get_gke_server_config()
#         if server_config:
#             return server_config.valid_node_versions
#         return None
#
#     def get_valid_gke_master_versions_from_gcp(self) -> Optional[List[str]]:
#         ## https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.ServerConfig.valid_master_versions
#         server_config = self.get_gke_server_config()
#         if server_config:
#             return server_config.valid_master_versions
#         return None
#
#     ######################################################
#     ## Create GKE Resources
#     ######################################################
#
#     def _create_gke_cluster(self) -> container_v1.types.Operation:
#         """Creates a GKE Cluster using the gcp_resources.GKEClusterSchema
#         Desc:
#             * Get GKEClusterConfig from GKEClusterSchema
#             * Create cluster using GKEClusterConfig
#
#         Raises:
#             * GKEClusterCreateException if cluster could not be created
#         """
#         self._verify_client()
#
#         # https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters
#         # TODO: Build a dedicated parse_object() method to convert pydantic schemas
#         #       to json/dict.
#         cluster_config: Dict[str, Any] = self._gke_cluster.gke_cluster_config.dict(
#             exclude_defaults=True
#         )
#         logger.info("Creating GKEClusterSchema")
#         # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.create_cluster
#         # TODO: fix the cluster config
#         self._create_gke_cluster_op = self._gcp_cluster_manager.create_cluster(
#             project_id=self._project_id,
#             zone=self._zone,
#             # cluster=cluster_config,
#         )
#         # logger.info(f"create_gke_cluster_op type: {type(self._create_gke_cluster_op)}")
#         # logger.info(f"Create Cluster Operation:\n{self._create_gke_cluster_op}")
#         return self._create_gke_cluster_op
#
#     def get_or_create_gke_cluster(
#         self, is_async: bool = False
#     ) -> Tuple[
#         Optional[container_v1.types.Cluster], Optional[container_v1.types.Operation]
#     ]:
#         """
#         Desc:
#             * Get the current active GKE Cluster from GCP.
#             * If no cluster is available, creates a GKE Cluster using the available config
#             * Waits for the Cluster to be created if is_async = False
#             * Always use this to create a cluster
#
#         Returns:
#             * Tuple(gke_cluster_response_from_gcp, None) if cluster is is already created
#             * Tuple(gke_cluster_response_from_gcp, create_cluster_operation) if is_async = True
#             * Tuple(None, create_cluster_operation) if is_async = True
#         """
#         self._verify_client()
#
#         logger.debug("In Pak8 get_or_create_gke_cluster")
#         try:
#             _gke_cluster: Optional[
#                 container_v1.types.Cluster
#             ] = self.get_gke_cluster_from_gcp()
#             # Indicates that this cluster is already created
#             if _gke_cluster is not None:
#                 logger.debug("GKEClusterSchema Available")
#                 return _gke_cluster, None
#         except exceptions.GKEClusterNotFoundException as e:
#             logger.debug("GKEClusterSchema Not found: {}".format(e))
#
#         try:
#             # Create a new GKE Cluster
#             _create_cluster_operation: container_v1.types.Operation = (
#                 self._create_gke_cluster()
#             )
#         except gcp_exception.PermissionDenied as e:
#             logger.exception(e)
#             raise exceptions.GKEClusterCreateException(e.message)
#         # logger.info(
#         #     f"_create_cluster_operation type: {type(_create_cluster_operation)}"
#         # )
#         # logger.info(f"_create_cluster_operation: {_create_cluster_operation}")
#
#         # Get the operation_id for Cluster Create
#         if _create_cluster_operation:
#             _create_op_name = _create_cluster_operation.name
#         if not _create_op_name:
#             logger.error(f"Could not extract name from {_create_cluster_operation}")
#             logger.error("This usually indicates something is wrong")
#             raise exceptions.GKEClusterCreateException(
#                 "Encountered an issue while creating GKE Cluster"
#             )
#
#         if is_async:
#             return (None, _create_cluster_operation)
#         else:
#             _op_success, _completed_op = self.wait_for_operation(_create_op_name)
#             if _op_success:
#                 try:
#                     _gke_cluster = self.get_gke_cluster_from_gcp()
#                     if _gke_cluster:
#                         return (_gke_cluster, _completed_op)
#                 except exceptions.GKEClusterNotFoundException as e:
#                     pass
#
#         raise exceptions.GKEClusterCreateException(
#             "Encountered an issue while creating GKE Cluster"
#         )
#
#     ######################################################
#     ## Delete GKE Resources
#     ######################################################
#
#     def _delete_gke_cluster(self) -> Optional[container_v1.types.Operation]:
#
#         if self._credentials and self._gcp_cluster_manager:
#             logger.debug(f"Deleting Cluster: {self._cluster_id}")
#             if self._gcp_cluster_manager:
#                 # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.delete_cluster
#                 delete_cluster_operation: Optional[
#                     container_v1.types.Operation
#                 ] = self._gcp_cluster_manager.delete_cluster(
#                     project_id=self._project_id,
#                     zone=self._zone,
#                     cluster_id=self._cluster_id,
#                 )
#                 # logger.info(
#                 #     f"delete_cluster_operation type: {type(delete_cluster_operation)}"
#                 # )
#                 # logger.info(f"Delete Cluster Operation:\n{delete_cluster_operation}")
#                 return delete_cluster_operation
#         return None
#
#     def delete_if_exists_cluster(self) -> Optional[container_v1.types.Operation]:
#         """Deletes a GKE Cluster if it exists.
#         Returns container_v1.types.Operation if cluster exists and is being deleted
#         """
#         self._verify_client()
#
#         try:
#             _cluster_gcp: Optional[
#                 container_v1.types.Cluster
#             ] = self.get_gke_cluster_from_gcp()
#             # Indicates that this cluster is available
#             return self._delete_gke_cluster()
#         except exceptions.GKEClusterNotFoundException as e:
#             logger.debug("No cluster available, returning None")
#
#         return None
#
#     ######################################################
#     ## Print data from GKE Api
#     ######################################################
#
#     def print_gke_cluster_status(self) -> None:
#         self._verify_client()
#         # https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
#         _gke_cluster: Optional[
#             container_v1.types.Cluster
#         ] = self.get_gke_cluster_from_gcp()
#         # print(f"_gke_cluster: {_gke_cluster}")
#         if _gke_cluster is None:
#             print(f"  - Cluster {self._cluster_id} not found")
#             return
#
#         _name = _gke_cluster.name
#         print(f"GKE Cluster: {_name}")
#
#         _node_pools = _gke_cluster.node_pools
#         print("  - Node Pools:")
#         for _np in _node_pools:
#             print(f"    - name: {_np.name}")
#             print(f"    - machine_type: {_np.config.machine_type}")
#             print(f"    - node_version: {_np.version}")
#
#         _current_master_version = _gke_cluster.current_master_version
#         print(f"  - Master Version: {_current_master_version}")
#
#         _current_node_count = _gke_cluster.current_node_count
#         print(f"  - Node Count: {_current_node_count}")
#
#     def print_gke_operations(
#         self,
#         limit: Optional[int] = None,
#         keys_to_print: List[str] = [
#             "name",
#             "zone",
#             "operationType",
#             "status",
#             "startTime",
#             "endTime",
#         ],
#     ) -> Optional[List[Dict[str, Any]]]:
#
#         self._verify_client()
#         try:
#             _operations: Optional[
#                 List[Dict[str, Any]]
#             ] = self._get_gke_operations_from_gcp()
#             if not _operations:
#                 logger.debug(f"No operations available")
#                 return None
#             logger.debug(f"Received {len(_operations)} _operations")
#
#             operations: List[Dict[str, Any]] = []
#             for op in _operations:
#                 formatted_op: Dict[str, Any] = OrderedDict()
#                 for k in keys_to_print:
#                     formatted_op[k] = op.get(k, None)
#                 operations.append(formatted_op)
#
#             if operations:
#                 operations.sort(key=lambda x: x["startTime"], reverse=True)
#                 if limit:
#                     operations = operations[:limit]
#                 print(json.dumps(operations, indent=2))
#             return operations
#         except exceptions.GKEClusterNotFoundException as e:
#             logger.error(f"Cluster {self._cluster_id} not available")
#             return None
#
#     def print_gke_cluster(
#         self,
#         keys_to_print: List[str] = [
#             "name",
#             "locations",
#             "self_link",
#             "status",
#             "create_time",
#             "node_pools",
#         ],
#     ) -> Optional[Dict[str, Any]]:
#
#         self._verify_client()
#         try:
#             _cluster: Optional[
#                 container_v1.types.Cluster
#             ] = self.get_gke_cluster_from_gcp()
#             if not _cluster:
#                 logger.info(f"No cluster available")
#                 return None
#             # logger.debug(f"cluster: {_cluster}")
#
#             cluster: Dict[str, Any] = OrderedDict()
#             for k in keys_to_print:
#                 cluster[k] = getattr(_cluster, k, None)
#
#             print(json.dumps(cluster, indent=2))
#             return cluster
#         except exceptions.GKEClusterNotFoundException as e:
#             logger.error(f"Cluster {self._cluster_id} not available")
#             return None
#
#     def print_gke_cluster_config(self) -> None:
#         print("GKE Cluster Config:")
#         if self.gke_cluster:
#             print(
#                 self.gke_cluster.gke_cluster_config.json(
#                     exclude_defaults=True, indent=2
#                 )
#             )
#
#     def print_gke_server_config(self) -> container_v1.types.ServerConfig:
#         self._verify_client()
#         _server_config: container_v1.types.ServerConfig = self.get_gke_server_config()
#         print(json.dumps(_server_config, indent=2))
#         return _server_config
#
#     ######################################################
#     ## Helpers
#     ######################################################
#
#     def _debug_log(self, msg: Optional[str] = None) -> None:
#         if msg:
#             logger.debug(msg)
#         logger.debug(f"Credentials  : {self._credentials}")
#         logger.debug(f"Pak8GKEClient   : {self._gcp_cluster_manager}")
#
#     def _verify_client(self) -> None:
#         """Helper method to verify that we are good to perform GKE operaitons.
#
#         Raises:
#             Pak8GKEClientException if something is wrong
#         """
#         # logger.debug  ("Verifying Pak8GKEClient")
#         if self._credentials and self._gcp_cluster_manager and self._cluster_id:
#             pass
#         else:
#             self._debug_log()
#             raise exceptions.Pak8GKEClientException("Pak8GKEClient unavailable")
#
#     ######################################################
#     ## Deprecated
#     ######################################################
#
#     # @classmethod
#     # def from_service_account_file(
#     #     cls, gke_cluster: gcp_resources.GKEClusterSchema, file_path: Path
#     # ):
#     #     try:
#     #         # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#     #         # Why we need the scopes: https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl
#     #         _credentials = service_account.Credentials.from_service_account_file(
#     #             file_path,
#     #             scopes=[
#     #                 "https://www.googleapis.com/auth/cloud-platform",
#     #                 "https://www.googleapis.com/auth/userinfo.email",
#     #             ],
#     #         )
#     #         return cls(gke_cluster, _credentials)
#     #     except Exception as e:
#     #         raise exceptions.GCPAuthException("Could not Authenticate with GCP", e)
#
#     # @classmethod
#     # def from_service_account_key(
#     #     cls, gke_cluster: gcp_resources.GKEClusterSchema, key: str
#     # ):
#     #     try:
#     #         # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#     #         _credentials = service_account.Credentials.from_service_account_info(
#     #             key,
#     #             scopes=[
#     #                 "https://www.googleapis.com/auth/cloud-platform",
#     #                 "https://www.googleapis.com/auth/userinfo.email",
#     #             ],
#     #         )
#     #         return cls(gke_cluster, _credentials)
#     #     except Exception as e:
#     #         raise exceptions.GCPAuthException("Could not Authenticate with GCP", e)
#
#     # def get_gke_clusters_from_gcp(
#     #     self, gke_cluster_status: Optional[enums.GKEClusterStatus] = None,
#     # ) -> Optional[List[Dict[Any, Any]]]:
#     #     """Returns a list of all GKE clusters in this project.
#     #     From the GKE API, we get a container_v1.types.ListClustersResponse message.
#     #     This ListClustersResponse message is then converted to a Dict
#     #     using google.protobuf.json_format.MessageToDict
#
#     #     We return the `clusters` variable from the Dict of ListClustersResponse.
#
#     #     References:
#     #         * GKE: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/ListClustersResponse
#     #         * Type: https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.ListClustersResponse
#     #     """
#     #     clusters = None
#     #     if self._credentials and self._gcp_cluster_manager:
#     #         # https://googleapis.dev/python/container/latest/gapic/v1/api.html#google.cloud.container_v1.ClusterManagerClient.list_clusters
#     #         __list_clusters_response: container_v1.types.ListClustersResponse = self._gcp_cluster_manager.list_clusters(
#     #             project_id=self._project_id, zone=self._zone
#     #         )
#     #         list_clusters_response = MessageToDict(__list_clusters_response)
#     #         # clusters has type List[Cluster]
#     #         # where Cluster: https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster
#     #         clusters = list_clusters_response.get("clusters", None)
#     #         logger.info(f"clusters type: {type(clusters)}")
#     #         logger.info(f"clusters: {clusters}")
#     #     return clusters
