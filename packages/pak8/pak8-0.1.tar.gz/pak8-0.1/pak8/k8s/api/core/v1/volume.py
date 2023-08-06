from typing import Optional, Union

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.k8s.resources.core.v1.volume import Volume
from pak8.k8s.resources.core.v1.volume import PersistentVolumeClaimVolumeSource
from pak8.k8s.resources.core.v1.volume import ConfigMapVolumeSource
from pak8.k8s.resources.core.v1.volume import SecretVolumeSource
from pak8.k8s.resources.core.v1.volume import EmptyDirVolumeSource

# class CreatePersistentVolumeClaim(BaseModel):
#     claim_name: str
#     read_only: bool


class CreateVolumeData(BaseModel):
    name: str
    mount_path: str
    read_only: Optional[bool] = None
    volume_type: k8s_enums.VolumeType
    pvc_name: Optional[str] = None
    configmap_name: Optional[str] = None
    secret_name: Optional[str] = None
    # Accepts a PVC Name or a CreatePersistentVolumeClaim object
    # pvc_name: Optional[Union[str, CreatePersistentVolumeClaim]] = None


def create_volume_resource(
    group_name: str, volume: CreateVolumeData
) -> Optional[Volume]:
    # logger.debug(f"Creating Volume: {volume.name}")

    if volume is None:
        return None

    _config_map = None
    _empty_dir = None
    _gce_persistent_disk = None
    _git_repo = None
    _pvc = None
    _secret = None

    if volume.volume_type == k8s_enums.VolumeType.PERSISTENT_VOLUME_CLAIM:
        if volume.pvc_name:
            _pvc = PersistentVolumeClaimVolumeSource(
                claim_name=volume.pvc_name, read_only=volume.read_only
            )
    elif volume.volume_type == k8s_enums.VolumeType.CONFIG_MAP:
        if volume.configmap_name:
            _config_map = ConfigMapVolumeSource(name=volume.configmap_name)
    elif volume.volume_type == k8s_enums.VolumeType.SECRET:
        if volume.secret_name:
            _secret = SecretVolumeSource(secret_name=volume.secret_name)
    elif volume.volume_type == k8s_enums.VolumeType.EMPTY_DIR:
        _empty_dir = EmptyDirVolumeSource()

    volume_resource = Volume(
        name=volume.name,
        config_map=_config_map,
        empty_dir=_empty_dir,
        gce_persistent_disk=_gce_persistent_disk,
        git_repo=_git_repo,
        persistent_volume_claim=_pvc,
        secret=_secret,
    )
    return volume_resource
