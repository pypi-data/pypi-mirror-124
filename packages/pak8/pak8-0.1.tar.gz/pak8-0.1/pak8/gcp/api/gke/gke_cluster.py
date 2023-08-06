from typing import List, Optional, cast

from pydantic import BaseModel

from pak8 import exceptions
import pak8.gcp.enums as gcp_enums
from pak8.utils.log import logger
from pak8.gcp.resources.gke import (
    GKEClusterConfig,
    NodePool,
    NodePoolAutoscaling,
    NodeConfig,
    IpAllocationPolicy,
)


class CreateNodePoolData(BaseModel):
    name: Optional[str]
    machine_type: gcp_enums.GKEMachineType
    initial_node_count: int
    autoscaling_enabled: bool
    min_node_count: Optional[int]
    max_node_count: Optional[int]

    class Config:
        use_enum_values = True


class CreateGkeClusterData(BaseModel):
    name: str
    master_version: Optional[
        gcp_enums.GKEMasterVersion
    ] = gcp_enums.GKEMasterVersion.VERSION_1_16_13_GKE_1
    node_pools: List[CreateNodePoolData]
    use_ip_aliases: Optional[bool] = True

    class Config:
        use_enum_values = True


def create_gke_cluster_config(
    create_gke_cluster_config_data: CreateGkeClusterData,
) -> GKEClusterConfig:

    if create_gke_cluster_config_data is None:
        raise exceptions.Pak8GCPConfInvalidException("CreateGkeClusterData is None")

    _cluster_name = create_gke_cluster_config_data.name
    logger.debug(f"Creating GKEClusterConfig Resource: {_cluster_name}")
    # logger.debug(f"Master Version: {create_gke_cluster_config_data.master_version}")
    # logger.debug(f"Master Version type: {type(create_gke_cluster_config_data.master_version)}")

    _node_pools: List[NodePool] = []
    _np_num = 0
    for pool in create_gke_cluster_config_data.node_pools:
        _np_num += 1

        _autoscaling: NodePoolAutoscaling = NodePoolAutoscaling(enabled=False)
        if pool.autoscaling_enabled and pool.min_node_count and pool.max_node_count:
            _autoscaling = NodePoolAutoscaling(
                enabled=pool.autoscaling_enabled,
                min_node_count=pool.min_node_count,
                max_node_count=pool.max_node_count,
            )
        _np_name = pool.name if pool.name else "{}-{}".format(_cluster_name, _np_num)
        _np_version: gcp_enums.GKENodeVersion
        if isinstance(
            create_gke_cluster_config_data.master_version, gcp_enums.GKEMasterVersion
        ):
            _np_version = cast(
                gcp_enums.GKENodeVersion,
                gcp_enums.GKENodeVersion.from_str(
                    create_gke_cluster_config_data.master_version.value
                ),
            )
        else:
            _np_version = cast(
                gcp_enums.GKENodeVersion,
                gcp_enums.GKENodeVersion.from_str(
                    create_gke_cluster_config_data.master_version
                ),
            )
        _np = NodePool(
            name=_np_name,
            version=_np_version,
            config=NodeConfig(machine_type=pool.machine_type),
            initial_node_count=pool.initial_node_count,
            autoscaling=_autoscaling,
        )
        _node_pools.append(_np)

    _cluster = GKEClusterConfig(
        name=_cluster_name,
        initial_cluster_version=create_gke_cluster_config_data.master_version,
        node_pools=_node_pools,
        ip_allocation_policy=IpAllocationPolicy(
            use_ip_aliases=create_gke_cluster_config_data.use_ip_aliases
        ),
    )
    # logger.info(f"GKEClusterConfig: {_cluster}")
    return _cluster
