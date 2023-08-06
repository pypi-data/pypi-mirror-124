from typing import Dict, List, Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums
from pak8.k8s.k8s_utils import (
    get_default_cr_name,
    get_default_crb_name,
    get_default_sa_name,
)
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.cluste_role_binding import (
    ClusterRoleBinding,
)
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.subject import Subject
from pak8.k8s.resources.rbac_authorization_k8s_io.v1.role_ref import RoleRef
from pak8.k8s.resources.common.labels import create_component_labels_dict
from pak8.k8s.resources.meta.v1.object_meta import ObjectMeta


class CreateClusterRoleBindingData(BaseModel):
    name: str
    cluster_role_name: str
    service_account_name: str


def create_cluster_role_binding_resource(
    create_cluster_role_binding: Optional[CreateClusterRoleBindingData],
    part_of: str,
    namespace: str,
    common_labels: Optional[Dict[str, str]] = None,
) -> ClusterRoleBinding:

    name = (
        create_cluster_role_binding.name
        if create_cluster_role_binding
        else get_default_crb_name(part_of)
    )
    # logger.debug(f"Creating CreateClusterRoleBindingData Resource: {name}")

    sa_name = (
        create_cluster_role_binding.service_account_name
        if create_cluster_role_binding
        else get_default_sa_name(part_of)
    )
    subjects: List[Subject] = [
        Subject(kind=k8s_enums.Kind.SERVICEACCOUNT, name=sa_name, namespace=namespace)
    ]
    cr_name = (
        create_cluster_role_binding.cluster_role_name
        if create_cluster_role_binding
        else get_default_cr_name(part_of)
    )

    crb_labels = create_component_labels_dict(
        component_name=name,
        part_of=part_of,
        common_labels=common_labels,
    )
    crb = ClusterRoleBinding(
        api_version=k8s_enums.ApiVersion.RBAC_AUTH_V1,
        kind=k8s_enums.Kind.CLUSTERROLEBINDING,
        metadata=ObjectMeta(
            name=name,
            namespace=namespace,
            labels=crb_labels,
        ),
        role_ref=RoleRef(
            api_group=k8s_enums.ApiGroup.RBAC_AUTH,
            kind=k8s_enums.Kind.CLUSTERROLE,
            name=cr_name,
        ),
        subjects=subjects,
    )
    return crb
