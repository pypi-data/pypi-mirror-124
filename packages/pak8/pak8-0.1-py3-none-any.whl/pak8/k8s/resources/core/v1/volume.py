from typing import List, Optional, Union

from kubernetes.client.models.v1_config_map_volume_source import V1ConfigMapVolumeSource
from kubernetes.client.models.v1_empty_dir_volume_source import V1EmptyDirVolumeSource
from kubernetes.client.models.v1_gce_persistent_disk_volume_source import (
    V1GCEPersistentDiskVolumeSource,
)
from kubernetes.client.models.v1_git_repo_volume_source import V1GitRepoVolumeSource
from kubernetes.client.models.v1_key_to_path import V1KeyToPath
from kubernetes.client.models.v1_persistent_volume_claim_volume_source import (
    V1PersistentVolumeClaimVolumeSource,
)
from kubernetes.client.models.v1_secret_volume_source import V1SecretVolumeSource
from kubernetes.client.models.v1_volume import V1Volume
from pydantic import BaseModel


class KeyToPath(BaseModel):
    key: str
    mode: int
    path: str


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_secret_volume_source.py
class SecretVolumeSource(BaseModel):
    secret_name: str
    default_mode: Optional[int] = None
    items: Optional[List[KeyToPath]] = None
    optional: Optional[bool] = None

    def get_k8s_object(self) -> V1SecretVolumeSource:
        # Return a V1SecretVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_secret_volume_source.py
        _items: Optional[List[V1KeyToPath]] = None
        if self.items:
            _items = []
            for _item in self.items:
                _items.append(
                    V1KeyToPath(
                        key=_item.key,
                        mode=_item.mode,
                        path=_item.path,
                    )
                )

        _v1_secret_volume_source = V1SecretVolumeSource(
            default_mode=self.default_mode,
            items=_items,
            secret_name=self.secret_name,
            optional=self.optional,
        )
        return _v1_secret_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_config_map_volume_source.py
class ConfigMapVolumeSource(BaseModel):
    name: str
    default_mode: Optional[int] = None
    items: Optional[List[KeyToPath]] = None
    optional: Optional[bool] = None

    def get_k8s_object(self) -> V1ConfigMapVolumeSource:
        # Return a V1ConfigMapVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_config_map_volume_source.py
        _items: Optional[List[V1KeyToPath]] = None
        if self.items:
            _items = []
            for _item in self.items:
                _items.append(
                    V1KeyToPath(
                        key=_item.key,
                        mode=_item.mode,
                        path=_item.path,
                    )
                )

        _v1_config_map_volume_source = V1ConfigMapVolumeSource(
            default_mode=self.default_mode,
            items=_items,
            name=self.name,
            optional=self.optional,
        )
        return _v1_config_map_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_empty_dir_volume_source.py
class EmptyDirVolumeSource(BaseModel):
    medium: Optional[str] = None
    size_limit: Optional[str] = None

    def get_k8s_object(self) -> V1EmptyDirVolumeSource:
        # Return a V1EmptyDirVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_empty_dir_volume_source.py
        _v1_empty_dir_volume_source = V1EmptyDirVolumeSource(
            medium=self.medium,
            size_limit=self.size_limit,
        )
        return _v1_empty_dir_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_gce_persistent_disk_volume_source.py
class GcePersistentDiskVolumeSource(BaseModel):
    fs_type: str
    partition: int
    pd_name: str
    read_only: bool

    def get_k8s_object(
        self,
    ) -> V1GCEPersistentDiskVolumeSource:
        # Return a V1GCEPersistentDiskVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_gce_persistent_disk_volume_source.py
        _v1_gce_persistent_disk_volume_source = V1GCEPersistentDiskVolumeSource(
            fs_type=self.fs_type,
            partition=self.partition,
            pd_name=self.pd_name,
            read_only=self.read_only,
        )
        return _v1_gce_persistent_disk_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_git_repo_volume_source.py
class GitRepoVolumeSource(BaseModel):
    directory: str
    repository: str
    revision: str

    def get_k8s_object(self) -> V1GitRepoVolumeSource:
        # Return a V1GitRepoVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_git_repo_volume_source.py
        _v1_git_repo_volume_source = V1GitRepoVolumeSource(
            directory=self.directory,
            repository=self.repository,
            revision=self.revision,
        )
        return _v1_git_repo_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


# https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim_volume_source.py
class PersistentVolumeClaimVolumeSource(BaseModel):
    claim_name: str
    read_only: Optional[bool] = None

    def get_k8s_object(
        self,
    ) -> V1PersistentVolumeClaimVolumeSource:
        # Return a V1PersistentVolumeClaimVolumeSource object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_persistent_volume_claim_volume_source.py
        _v1_persistent_volume_claim_volume_source = V1PersistentVolumeClaimVolumeSource(
            claim_name=self.claim_name,
            read_only=self.read_only,
        )
        return _v1_persistent_volume_claim_volume_source

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


VolumeSourceType = Union[
    ConfigMapVolumeSource,
    EmptyDirVolumeSource,
    GcePersistentDiskVolumeSource,
    GitRepoVolumeSource,
    PersistentVolumeClaimVolumeSource,
    SecretVolumeSource,
]


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#volume-v1-core
class Volume(BaseModel):

    name: str
    config_map: Optional[ConfigMapVolumeSource] = None
    empty_dir: Optional[EmptyDirVolumeSource] = None
    gce_persistent_disk: Optional[GcePersistentDiskVolumeSource] = None
    git_repo: Optional[GitRepoVolumeSource] = None
    persistent_volume_claim: Optional[PersistentVolumeClaimVolumeSource] = None
    secret: Optional[SecretVolumeSource] = None

    def get_k8s_object(self) -> V1Volume:
        # Return a V1Volume object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_volume.py
        _v1_volume = V1Volume(
            name=self.name,
            config_map=self.config_map.get_k8s_object() if self.config_map else None,
            empty_dir=self.empty_dir.get_k8s_object() if self.empty_dir else None,
            gce_persistent_disk=self.gce_persistent_disk.get_k8s_object()
            if self.gce_persistent_disk
            else None,
            git_repo=self.git_repo.get_k8s_object() if self.git_repo else None,
            persistent_volume_claim=self.persistent_volume_claim.get_k8s_object()
            if self.persistent_volume_claim
            else None,
            secret=self.secret.get_k8s_object() if self.secret else None,
        )
        return _v1_volume

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
