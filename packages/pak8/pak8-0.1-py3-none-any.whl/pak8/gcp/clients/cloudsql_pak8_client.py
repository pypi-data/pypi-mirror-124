# from typing import Optional, Dict, Any
#
# import googleapiclient.discovery
# from google.oauth2 import service_account
#
# from pak8 import exceptions
# import pak8.gcp.resources as gcp_resources
# from pak8.utils.log import logger
#
#
# class Pak8CloudSQLClient:
#     """This class interacts with Google CloudSQL API
#     http://googleapis.github.io/google-api-python-client/docs/dyn/sqladmin_v1beta4.html
#
#     Since there doesn't exist a Google Cloud Client library for CloudSQL, we have to use
#     the google-api-python-client: https://github.com/googleapis/google-api-python-client
#
#     Since this process gets complicated very quickly, here are some references:
#         * https://github.com/googleapis/google-api-python-client/blob/master/docs/start.md
#         * https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth-server.md#calling-google-apis
#
#     Each Pak8CloudSQLClient instance is attached to 1 and only 1 Pak8.
#     """
#
#     def __init__(
#         self,
#         cloud_sql_instances: gcp_resources.CloudSQLInstances,
#         credentials: service_account.Credentials,
#     ):
#
#         # The gcp_resources.CloudSQLInstances schema should contain all information required
#         # for interacting with Google CloudSQL python api
#         self._cloud_sql_instances: gcp_resources.CloudSQLInstances = cloud_sql_instances
#         # A Credentials Object which will be used to create storage client
#         # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#         self._credentials: service_account.Credentials = credentials
#         self._project_id = self._cloud_sql_instances.project_id
#
#         # The Client is the API for CloudSQL.
#         # http://googleapis.github.io/google-api-python-client/docs/dyn/sqladmin_v1beta4.html
#         self._pak8_cloudsql_client: googleapiclient.discovery.Resource = (
#             googleapiclient.discovery.build(
#                 "sqladmin", "v1beta4", credentials=credentials
#             )
#         )
#
#         # Verify Pak8CloudSQLClient is initialized correctly.
#         self._verify_client()
#
#     ######################################################
#     ## GET data from CloudSQL API
#     ######################################################
#
#     def _get_cloudsql_instance_from_gcp(
#         self,
#         instance_id: str,
#         # skip_cache: bool = False
#     ) -> Optional[Dict[str, Any]]:
#         """Returns the CloudSQL Instance if available.
#         Uses the cached version unless skip_cache = True
#
#         TODO:
#             * Cache this response and implement skip_cache
#
#         References:
#             * http://googleapis.github.io/google-api-python-client/docs/dyn/sqladmin_v1beta4.instances.html#get
#         """
#         try:
#             self._verify_client()
#             # http://googleapis.github.io/google-api-python-client/docs/dyn/sqladmin_v1beta4.instances.html#get
#             _instance: Optional[Dict[str, Any]] = (
#                 self._pak8_cloudsql_client.instances()
#                 .get(project=self._project_id, instance=instance_id)
#                 .execute()
#             )
#             return _instance
#         except Exception as e:
#             # self._debug_log(f"Could not get instance: {instance_id}")
#             raise exceptions.CloudSQLInstanceNotFoundException(e)
#
#     ######################################################
#     ## Print data from GKE Api
#     ######################################################
#
#     def print_cloudsql_instance_status(self) -> None:
#         for instance_id in self._cloud_sql_instances.instance_ids:
#             try:
#                 # http://googleapis.github.io/google-api-python-client/docs/dyn/sqladmin_v1beta4.instances.html#get
#                 _instance: Optional[
#                     Dict[str, Any]
#                 ] = self._get_cloudsql_instance_from_gcp(instance_id)
#                 if _instance is None:
#                     # print(f"Instance {instance_id} not found")
#                     continue
#                 # print(f"_instance: {_instance}")
#
#                 _name = _instance.get("name", None)
#                 print(f"CloudSQL Instance: {_name}")
#
#                 _state = _instance.get("state", None)
#                 print(f"  - State: {_state}")
#
#                 _activation_policy = _instance.get("settings", {}).get(
#                     "activationPolicy", None
#                 )
#                 print(f"  - Active: {_activation_policy}")
#             except exceptions.CloudSQLInstanceNotFoundException as e:
#                 print(f"Instance {instance_id} not found")
#
#     ######################################################
#     ## Helpers
#     ######################################################
#
#     def _debug_log(self, msg: Optional[str] = None) -> None:
#         if msg:
#             logger.debug(msg)
#         logger.debug(f"Credentials  : {self._credentials}")
#         logger.debug(f"Pak8CloudSQLClient   : {self._pak8_cloudsql_client}")
#
#     def _verify_client(self) -> None:
#         """Helper method to verify that we are good to perform CloudSQL operaitons.
#
#         Raises:
#             Pak8CloudSQLClientException if something is wrong
#         """
#         if self._credentials and self._pak8_cloudsql_client:
#             pass
#         else:
#             self._debug_log()
#             raise exceptions.Pak8CloudSQLClientException(
#                 "Pak8CloudSQLClient unavailable"
#             )
