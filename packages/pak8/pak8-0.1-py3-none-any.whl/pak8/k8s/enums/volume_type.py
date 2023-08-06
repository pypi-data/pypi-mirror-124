from pak8.utils.enums import ExtendedEnum


class VolumeType(ExtendedEnum):
    CONFIG_MAP = "CONFIG_MAP"
    EMPTY_DIR = "EMPTY_DIR"
    GCE_PERSISTENT_DISK = "GCE_PERSISTENT_DISK"
    GIT_REPO = "GIT_REPO"
    NAME = "NAME"
    PERSISTENT_VOLUME_CLAIM = "PERSISTENT_VOLUME_CLAIM"
    SECRET = "SECRET"
