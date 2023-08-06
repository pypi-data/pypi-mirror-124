from pak8.utils.enums import ExtendedEnum


class Kind(ExtendedEnum):
    CLUSTERROLE = "ClusterRole"
    CLUSTERROLEBINDING = "ClusterRoleBinding"
    CONFIG = "Config"
    CONFIGMAP = "ConfigMap"
    DEPLOYMENT = "Deployment"
    NAMESPACE = "Namespace"
    SERVICE = "Service"
    SERVICEACCOUNT = "ServiceAccount"
    SECRET = "Secret"
    PERSISTENTVOLUMECLAIM = "PersistentVolumeClaim"
    STORAGECLASS = "StorageClass"
    CUSTOMRESOURCEDEFINITION = "CustomResourceDefinition"
    # CRDs for Traefik
    INGRESSROUTE = "IngressRoute"
    INGRESSROUTETCP = "IngressRouteTCP"
    MIDDLEWARE = "Middleware"
    TLSOPTION = "TLSOption"
