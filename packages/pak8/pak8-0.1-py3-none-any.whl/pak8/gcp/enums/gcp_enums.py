from typing import Any, Optional
from pak8.utils.enums import ExtendedEnum
from pak8.utils.log import logger


class GKEClusterStatus(ExtendedEnum):
    """The current status of the cluster.
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster.Status
    """

    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    PROVISIONING = "PROVISIONING"
    RUNNING = "RUNNING"
    RECONCILING = "RECONCILING"
    STOPPING = "STOPPING"
    ERROR = "ERROR"
    DEGRADED = "DEGRADED"


class GKEOperationType(ExtendedEnum):
    """The type of the GKE operation.
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1beta1/projects.locations.operations#Operation.Type
    """

    TYPE_UNSPECIFIED = "TYPE_UNSPECIFIED"
    CREATE_CLUSTER = "CREATE_CLUSTER"
    DELETE_CLUSTER = "DELETE_CLUSTER"
    UPGRADE_MASTER = "UPGRADE_MASTER"
    UPGRADE_NODES = "UPGRADE_NODES"
    REPAIR_CLUSTER = "REPAIR_CLUSTER"
    UPDATE_CLUSTER = "UPDATE_CLUSTER"
    CREATE_NODE_POOL = "CREATE_NODE_POOL"
    DELETE_NODE_POOL = "DELETE_NODE_POOL"
    SET_NODE_POOL_MANAGEMENT = "SET_NODE_POOL_MANAGEMENT"
    AUTO_REPAIR_NODES = "AUTO_REPAIR_NODES"
    AUTO_UPGRADE_NODES = "AUTO_UPGRADE_NODES"
    SET_LABELS = "SET_LABELS"
    SET_MASTER_AUTH = "SET_MASTER_AUTH"
    SET_NODE_POOL_SIZE = "SET_NODE_POOL_SIZE"
    SET_NETWORK_POLICY = "SET_NETWORK_POLICY"
    SET_MAINTENANCE_POLICY = "SET_MAINTENANCE_POLICY"


class GKEOperationStatus(ExtendedEnum):
    """The current status of the GKE operation.
    https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster.Status
    https://github.com/googleapis/google-cloud-python/blob/master/container/google/cloud/container_v1/proto/cluster_service_pb2.py#L143
    """

    STATUS_UNSPECIFIED = "STATUS_UNSPECIFIED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    ABORTING = "ABORTING"


# Get using  gcloud container get-server-config --zone  us-central1-a
class GKEMasterVersion(ExtendedEnum):
    """Currently supported GKE Master Versions."""

    VERSION_1_16_13_GKE_1 = "1.16.13-gke.1"
    VERSION_1_16_11_GKE_5 = "1.16.11-gke.5"
    VERSION_1_15_12_GKE_16 = "1.15.12-gke.16"
    VERSION_1_15_12_GKE_13 = "1.15.12-gke.13"
    VERSION_1_15_12_GKE_9 = "1.15.12-gke.9"
    VERSION_1_15_12_GKE_2 = "1.15.12-gke.2"
    VERSION_1_14_10_GKE_46 = "1.14.10-gke.46"
    VERSION_1_14_10_GKE_45 = "1.14.10-gke.45"
    VERSION_1_14_10_GKE_42 = "1.14.10-gke.42"

    @classmethod
    def from_str(cls: Any, str_to_convert_to_enum: Optional[str]) -> Optional[Any]:
        "Convert a string value to an enum object."
        # logger.info("In from_str of {}".format(cls))
        if str_to_convert_to_enum is None:
            return None

        # _parsed_version_str = str_to_convert_to_enum.replace(".", "_").replace("-", "_").upper()
        # parsed_version_str = f"VERSION_{_parsed_version_str}"
        # logger.info("str_to_convert_to_enum: {}".format(str_to_convert_to_enum))
        # logger.info("_value2member_map_: {}".format(cls._value2member_map_))
        if str_to_convert_to_enum in cls._value2member_map_:
            return cls._value2member_map_.get(str_to_convert_to_enum)
        else:
            raise NotImplementedError(
                "{} is not a member of {}: {}".format(
                    str_to_convert_to_enum, cls, cls._value2member_map_.keys()
                )
            )


class GKENodeVersion(ExtendedEnum):
    """Currently supported GKE Versions."""

    VERSION_1_16_13_GKE_1 = "1.16.13-gke.1"
    VERSION_1_16_11_GKE_5 = "1.16.11-gke.5"
    VERSION_1_15_12_GKE_16 = "1.15.12-gke.16"
    VERSION_1_15_12_GKE_13 = "1.15.12-gke.13"
    VERSION_1_15_12_GKE_9 = "1.15.12-gke.9"
    VERSION_1_15_12_GKE_2 = "1.15.12-gke.2"
    VERSION_1_14_10_GKE_46 = "1.14.10-gke.46"
    VERSION_1_14_10_GKE_45 = "1.14.10-gke.45"
    VERSION_1_14_10_GKE_42 = "1.14.10-gke.42"


class GKEMachineType(ExtendedEnum):
    """Currently supported Machine types."""

    GCP_N1_STANDARD_1 = "n1-standard-1"
    GCP_N1_STANDARD_2 = "n1-standard-2"


class GCPProductType(ExtendedEnum):
    """Currently supported GCP Products."""

    GKE = "GKE"
    GCS = "GCS"
