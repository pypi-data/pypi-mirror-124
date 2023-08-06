from typing import Dict, Optional

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.k8s.resources.core.v1.namespace import Namespace
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


def create_namespace_resource(
    name: str,
    part_of: str,
    common_labels: Optional[Dict[str, str]] = None,
) -> Namespace:
    # logger.debug(f"Creating Namespace Resource: {name}")

    if name is None:
        return None

    ns_labels = create_component_labels_dict(
        component_name=name,
        part_of=part_of,
        common_labels=common_labels,
    )
    ns = Namespace(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.NAMESPACE,
        metadata=ObjectMeta(
            name=name,
            labels=ns_labels,
        ),
    )
    return ns
