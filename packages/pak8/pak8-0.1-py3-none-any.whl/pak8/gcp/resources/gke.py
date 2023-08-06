from typing import Any, Dict, List, Optional

from pydantic import BaseModel

import pak8.gcp.enums as gcp_enums


# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/NodeConfig
# https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.NodeConfig
class NodeConfig(BaseModel):
    machine_type: gcp_enums.GKEMachineType
    disk_size_gb: Optional[str] = None

    class Config:
        use_enum_values = True


# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool.NodePoolAutoscaling
class NodePoolAutoscaling(BaseModel):
    enabled: bool
    min_node_count: Optional[int] = None
    max_node_count: Optional[int] = None


# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters.nodePools#NodePool
# https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.NodePool
class NodePool(BaseModel):
    name: str
    version: gcp_enums.GKENodeVersion
    config: NodeConfig
    initial_node_count: int
    autoscaling: NodePoolAutoscaling

    class Config:
        use_enum_values = True


# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.locations.clusters#Cluster.IPAllocationPolicy
# https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.IPAllocationPolicy
class IpAllocationPolicy(BaseModel):
    use_ip_aliases: bool


# https://cloud.google.com/kubernetes-engine/docs/reference/rest/v1/projects.zones.clusters
# https://googleapis.dev/python/container/latest/gapic/v1/types.html#google.cloud.container_v1.types.Cluster
# TODO: Use use_enum_values from https://pydantic-docs.helpmanual.io/usage/model_config/
# instead of storing the enums as strings
class GKEClusterConfig(BaseModel):
    name: str
    description: Optional[str] = None
    initial_cluster_version: gcp_enums.GKENodeVersion
    node_pools: List[NodePool]
    ip_allocation_policy: IpAllocationPolicy

    class Config:
        use_enum_values = True


class GKECluster(BaseModel):
    project_id: str
    zone: str
    gke_cluster_config: GKEClusterConfig
