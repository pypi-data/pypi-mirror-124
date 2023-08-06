from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.api.rbac_authorization_k8s_io.v1.policy_rule import CreatePolicyRule
from pak8.k8s.k8s_utils import get_default_cr_name
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluster_role import ClusterRole
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.policy_rule import PolicyRule
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateClusterRoleData(BaseModel):
    name: str
    # TODO: Change CreatePolicyRule to use enums instead of str
    rules: List[CreatePolicyRule]


def create_cluster_role_resource(
    create_cluster_role: Optional[CreateClusterRoleData],
    part_of: str,
    namespace: str,
    common_labels: Optional[Dict[str, str]] = None,
) -> ClusterRole:

    name = (
        create_cluster_role.name
        if create_cluster_role
        else get_default_cr_name(part_of)
    )
    # logger.debug(f"Creating ClusterRole Resource: {name}")

    cr_rules: Optional[List[PolicyRule]] = None
    _rules = (
        create_cluster_role.rules
        if create_cluster_role
        else [CreatePolicyRule(api_groups=["*"], resources=["*"], verbs=["*"])]
    )
    if _rules:
        cr_rules = []
        for rule in _rules:
            cr_rules.append(
                PolicyRule(
                    api_groups=rule.api_groups,
                    resources=rule.resources,
                    verbs=rule.verbs,
                )
            )
    cr_labels = create_component_labels_dict(
        component_name=name,
        part_of=part_of,
        common_labels=common_labels,
    )

    cr = ClusterRole(
        api_version=k8s_enums.ApiVersion.RBAC_AUTH_V1,
        kind=k8s_enums.Kind.CLUSTERROLE,
        metadata=ObjectMeta(
            name=name,
            namespace=namespace,
            labels=cr_labels,
        ),
        rules=cr_rules,
    )
    return cr
