from pak8.utils.enums import ExtendedEnum


class DockerPak8Status(ExtendedEnum):
    """Enum describing the current status of a DockerPak8"""

    # Level 0: The DockerPak8 has just been created
    INIT = "INIT"

    # Level 1: Ready to Deploy Containers
    CLIENT_VALID = "CLIENT_VALID"

    # Level 2: Containers Running
    CONTAINERS_RUNNING = "CONTAINERS_RUNNING"

    # Level 3: Containers Stopped
    CONTAINERS_STOPPED = "CONTAINERS_STOPPED"

    # Errors
    ERROR = "ERROR"

    def can_create_resources(self) -> bool:
        return self in (
            DockerPak8Status.CLIENT_VALID,
            DockerPak8Status.CONTAINERS_RUNNING,
            DockerPak8Status.CONTAINERS_STOPPED,
        )

    def can_delete_resources(self) -> bool:
        return self in (
            DockerPak8Status.CLIENT_VALID,
            DockerPak8Status.CONTAINERS_RUNNING,
            DockerPak8Status.CONTAINERS_STOPPED,
        )
