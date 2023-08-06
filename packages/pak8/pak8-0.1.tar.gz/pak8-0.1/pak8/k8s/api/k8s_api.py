import kubernetes


class K8sApi:
    def __init__(self, k8s_api_client: kubernetes.client.ApiClient):
        self.k8s_api_client: kubernetes.client.ApiClient = k8s_api_client
        self.k8s_apps_v1_api: kubernetes.client.AppsV1Api = kubernetes.client.AppsV1Api(
            self.k8s_api_client
        )
        self.k8s_core_v1_api: kubernetes.client.CoreV1Api = kubernetes.client.CoreV1Api(
            self.k8s_api_client
        )
        self.k8s_rbac_auth_v1_api: kubernetes.client.RbacAuthorizationV1Api = (
            kubernetes.client.RbacAuthorizationV1Api(self.k8s_api_client)
        )
        self.k8s_storage_v1_api: kubernetes.client.StorageV1Api = (
            kubernetes.client.StorageV1Api(self.k8s_api_client)
        )
        self.k8s_apiextensions_v1beta1_api: kubernetes.client.ApiextensionsV1beta1Api = kubernetes.client.ApiextensionsV1beta1Api(
            self.k8s_api_client
        )
        self.k8s_custom_objects_api: kubernetes.client.CustomObjectsApi = (
            kubernetes.client.CustomObjectsApi(self.k8s_api_client)
        )
