from pak8.utils.enums import ExtendedEnum


class ApiVersion(ExtendedEnum):
    CORE_V1 = "v1"
    APPS_V1 = "app/v1"
    RBAC_AUTH_V1 = "rbac.authorization.k8s.io/v1"
    STORAGE_V1 = "storage.k8s.io/v1"
    APIEXTENSIONS_V1BETA1 = "apiextensions.k8s.io/v1beta1"
    # CRDs for Traefik
    TRAEFIK_CONTAINO_US_V1ALPHA1 = "traefik.containo.us/v1alpha1"
