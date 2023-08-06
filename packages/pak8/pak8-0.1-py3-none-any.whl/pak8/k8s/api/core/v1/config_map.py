from typing import Any, Dict, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.utils.log import logger
from pak8.utils.common import is_empty
from pak8.k8s.resources.core.v1.config_map import ConfigMap
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateConfigMapData(BaseModel):
    name: str
    data: Dict[str, Any]


def create_configmap_resource(
    group_name: str,
    namespace: str,
    create_cm_data: CreateConfigMapData,
    common_labels: Optional[Dict[str, str]] = None,
) -> Optional[ConfigMap]:
    """Creates a ConfigMap resource.

    TODO:
        * Add doc
        * Add Error Handling
    """
    if create_cm_data is None:
        return None

    cm_name: str = create_cm_data.name if create_cm_data.name else ""
    if is_empty(cm_name):
        logger.error(f"CreateConfigMapData.name unavailable for group: {group_name}")

    # logger.debug(f"Creating ConfigMap Resource: {cm_name}")
    cm_labels = create_component_labels_dict(
        component_name=cm_name,
        part_of=group_name,
        common_labels=common_labels,
    )

    configmap = ConfigMap(
        api_version=k8s_enums.ApiVersion.CORE_V1,
        kind=k8s_enums.Kind.CONFIGMAP,
        metadata=ObjectMeta(
            name=cm_name,
            namespace=namespace,
            labels=cm_labels,
        ),
        data=create_cm_data.data,
    )

    # logger.info(f"ConfigMap {cm_name}:\n{configmap.json(exclude_defaults=True, indent=2)}")
    return configmap
