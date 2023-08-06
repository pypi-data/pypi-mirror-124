from typing import Any, Dict, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.resources.core.v1.secret import Secret
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateSecretData(BaseModel):
    name: str
    secret_type: Optional[str] = "Opaque"
    data: Optional[Dict[str, Any]] = None
    string_data: Optional[Dict[str, Any]] = None


def create_secret_resource(
    group_name: str,
    namespace: str,
    secret: CreateSecretData,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[Secret]:
    """Creates a Secret resource.

    TODO:
        * Add doc
        * Add Error Handling
    """
    # logger.debug(f"Creating Secret Resource: {group_name}")

    if secret is None:
        return None

    secret_name = secret.name
    secret_labels = create_component_labels_dict(
        component_name=secret_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    _secret = Secret(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.SECRET,
        metadata=ObjectMeta(
            name=secret_name,
            namespace=namespace,
            labels=secret_labels,
        ),
        data=secret.data,
        string_data=secret.string_data,
        type=secret.secret_type,
    )

    # logger.info(
    #     f"Secret {secret_name}:\n{_secret.json(exclude_defaults=True, indent=2)}"
    # )
    return _secret
