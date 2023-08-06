from pak8.utils.enums import ExtendedEnum


class Pak8Status(ExtendedEnum):
    """Enum describing the current status of a Pak8"""

    # PHASE 0
    # The Pak8 has just been created, not initialized yet
    # The Pak8 maintains this status till it is initialized, usually through the get_pak8_status()
    PRE_INIT = "PRE_INIT"
    INIT_VALIDATION_COMPLETE = "INIT_VALIDATION_COMPLETE"

    # READY_TO_PROVISION_INFRA = 2
    # PHASE 1
    READY_TO_CREATE_K8S_CLUSTER = "READY_TO_CREATE_K8S_CLUSTER"
    CREATING_K8S_CLUSTER = "CREATING_K8S_CLUSTER"
    K8S_CLUSTER_AVAILABLE = "K8S_CLUSTER_AVAILABLE"

    # PHASE 2
    READY_TO_DEPLOY_K8S_RESOURCES = "READY_TO_DEPLOY_K8S_RESOURCES"
    K8S_RESOURCES_ACTIVE = "K8S_RESOURCES_ACTIVE"

    # Negative codes for shutting down pak8
    DELETING_K8S_CLUSTER = "DELETING_K8S_CLUSTER"
    K8S_CLUSTER_ERROR = "K8S_CLUSTER_ERROR"
    SHUTDOWN = "SHUTDOWN"

    # Errors
    PAK8_INIT_ERROR = "PAK8_INIT_ERROR"

    def can_create_k8s_cluster(self) -> bool:
        return self in (
            Pak8Status.READY_TO_CREATE_K8S_CLUSTER,
            Pak8Status.CREATING_K8S_CLUSTER,
            Pak8Status.K8S_CLUSTER_AVAILABLE,
            Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES,
            Pak8Status.K8S_RESOURCES_ACTIVE,
        )

    def can_delete_k8s_cluster(self) -> bool:
        return self in (
            Pak8Status.CREATING_K8S_CLUSTER,
            Pak8Status.K8S_CLUSTER_AVAILABLE,
            Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES,
            Pak8Status.K8S_RESOURCES_ACTIVE,
        )

    def k8s_cluster_is_available(self) -> bool:
        return self in (
            Pak8Status.K8S_CLUSTER_AVAILABLE,
            Pak8Status.READY_TO_DEPLOY_K8S_RESOURCES,
            Pak8Status.K8S_RESOURCES_ACTIVE,
        )

    def k8s_cluster_is_deleted(self) -> bool:
        return self in (
            Pak8Status.PRE_INIT,
            Pak8Status.INIT_VALIDATION_COMPLETE,
            Pak8Status.READY_TO_CREATE_K8S_CLUSTER,
            Pak8Status.DELETING_K8S_CLUSTER,
        )
