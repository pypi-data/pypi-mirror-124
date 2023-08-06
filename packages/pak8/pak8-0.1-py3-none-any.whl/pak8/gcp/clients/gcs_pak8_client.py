# from typing import Optional
#
# from google.cloud import storage
# from google.oauth2 import service_account
#
# from pak8 import exceptions
# import pak8.gcp.resources as gcp_resources
# from pak8.utils.log import logger
#
#
# class Pak8GCSClient:
#     """This class interacts with Google Cloud Storage API
#     https://googleapis.dev/python/storage/latest/client.html
#
#     Each Pak8GCSClient instance is attached to 1 and only 1 Pak8.
#     """
#
#     def __init__(
#         self,
#         gcs_buckets: gcp_resources.GCSBuckets,
#         credentials: service_account.Credentials,
#     ):
#
#         # The gcp_resources.GCSBuckets schema should contain all information required
#         # for interacting with Google Cloud Storage python api
#         self._gcs_buckets: gcp_resources.GCSBuckets = gcs_buckets
#         # A Credentials Object which will be used to create storage client
#         # https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials
#         self._credentials: service_account.Credentials = credentials
#         self._project_id = self._gcs_buckets.project_id
#         # The Client is the API for GCS.
#         # https://googleapis.dev/python/storage/latest/client.html#google.cloud.storage.client.Client
#         self._pak8_gcs_client: storage.Client = storage.Client(
#             project=self._gcs_buckets.project_id,
#             credentials=credentials,
#         )
#
#         # Verify Pak8GCSClient is initialized correctly.
#         self._verify_client()
#
#     ######################################################
#     ## Helpers
#     ######################################################
#
#     def _debug_log(self, msg: Optional[str] = None) -> None:
#         if msg:
#             logger.debug(msg)
#         logger.debug(f"Credentials  : {self._credentials}")
#         logger.debug(f"Pak8GCSClient   : {self._pak8_gcs_client}")
#
#     def _verify_client(self) -> None:
#         """Helper method to verify that we are good to perform GCS operaitons.
#
#         Raises:
#             Pak8GCSClientException if something is wrong
#         """
#         if self._credentials and self._pak8_gcs_client:
#             pass
#         else:
#             self._debug_log()
#             raise exceptions.Pak8GCSClientException("Pak8GCSClient unavailable")
