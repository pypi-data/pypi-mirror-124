from typing import Dict, Optional


def create_component_labels_dict(
    component_name: str, part_of: str, common_labels: Optional[Dict[str, str]] = None
) -> Dict[str, str]:
    _labels = {
        "app.kubernetes.io/component": component_name,
        "app.kubernetes.io/part-of": part_of,
    }
    if common_labels:
        _labels.update(common_labels)

    return _labels


def create_common_labels_dict(
    name: str,
    version: Optional[str] = None,
) -> Dict[str, str]:
    _labels = {
        "pak8/name": name,
    }
    if version:
        _labels.update({"pak8/version": version})

    return _labels
