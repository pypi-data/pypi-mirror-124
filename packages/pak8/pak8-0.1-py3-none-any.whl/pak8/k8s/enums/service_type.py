from pak8.utils.enums import ExtendedEnum


class ServiceType(ExtendedEnum):
    CLUSTERIP = "ClusterIP"
    NODEPORT = "NodePort"
    LOADBALANCER = "LoadBalancer"
