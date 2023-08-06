from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.k8s_utils import get_default_sa_name
from pak8.k8s.resources.core.v1.service_account import (
    ServiceAccount,
    LocalObjectReference,
)
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateServiceAccountData(BaseModel):
    name: str
    uid: Optional[int] = None
    gid: Optional[int] = None
    image_pull_secrets: Optional[List[str]] = None


def create_service_account_resource(
    create_service_account: Optional[CreateServiceAccountData],
    part_of: str,
    namespace: str,
    common_labels: Optional[Dict[str, str]] = None,
) -> ServiceAccount:

    name = (
        create_service_account.name
        if create_service_account
        else get_default_sa_name(part_of)
    )
    # logger.debug(f"Creating ServiceAccount Resource: {name}")

    sa_image_pull_secrets: Optional[List[LocalObjectReference]] = None
    _image_pull_secrets = (
        create_service_account.image_pull_secrets if create_service_account else None
    )
    if _image_pull_secrets:
        sa_image_pull_secrets = []
        for secret in _image_pull_secrets:
            sa_image_pull_secrets.append(LocalObjectReference(name=secret))
    sa_labels = create_component_labels_dict(
        component_name=name,
        part_of=part_of,
        common_labels=common_labels,
    )

    sa = ServiceAccount(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.SERVICEACCOUNT,
        metadata=ObjectMeta(
            name=name,
            namespace=namespace,
            labels=sa_labels,
        ),
        image_pull_secrets=sa_image_pull_secrets,
    )
    return sa
