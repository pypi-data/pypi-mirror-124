from typing import List, Optional

from kubernetes.client import AppsV1Api
from kubernetes.client.models.v1_deployment import V1Deployment
from kubernetes.client.models.v1_deployment_list import V1DeploymentList
from kubernetes.client.models.v1_deployment_spec import V1DeploymentSpec
from kubernetes.client.models.v1_status import V1Status
from pydantic import BaseModel, Field

from pak8.k8s.api.k8s_api import K8sApi
from pak8.k8s.resources.apps.v1.deployment_strategy import DeploymentStrategy
from pak8.k8s.resources.core.v1.pod_template_spec import PodTemplateSpec
from pak8.k8s.resources.k8s_resource_base import K8sResourceBase
from pak8.k8s.resources.meta.v1.label_selector import LabelSelector
from pak8.utils.log import logger


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#deploymentspec-v1-apps
class DeploymentSpec(BaseModel):
    min_ready_seconds: Optional[int] = Field(None, alias="minReadySeconds")
    replicas: int
    # The selector field defines how the Deployment finds which Pods to manage
    selector: LabelSelector
    strategy: Optional[DeploymentStrategy] = None
    template: PodTemplateSpec

    def get_k8s_object(self) -> V1DeploymentSpec:

        # Return a V1DeploymentSpec object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_deployment_spec.py
        _strategy = self.strategy.get_k8s_object() if self.strategy else None
        _v1_deployment_spec = V1DeploymentSpec(
            min_ready_seconds=self.min_ready_seconds,
            replicas=self.replicas,
            selector=self.selector.get_k8s_object(),
            strategy=_strategy,
            template=self.template.get_k8s_object(),
        )
        return _v1_deployment_spec

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Deployment(K8sResourceBase):
    """Pak8 representation of a K8s Deployment.
    A Deployment provides declarative updates for Pods and ReplicaSets.
    In simple terms, we use deployments to run containers.
    Containers are run in Pods or ReplicaSets, and Deployments manages those Pods or ReplicaSets for us.
    Let's say a rogue application running in an airflow task takes down the container which is running in a pod.
    Previously we'd have to fix the pod, but now, the Deployment will make sure the Pod/ReplicaSet restarts and reaches desired state.

    References:
        * Docs:
            https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#deployment-v1-apps
            https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
        * Type: https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_deployment.py
    """

    spec: DeploymentSpec

    # V1Deployment object received as the output after creating the deploy
    v1_deployment: Optional[V1Deployment] = None
    # List of attributes to include in the K8s manifest
    attributes_for_k8s_manifest: List[str] = ["spec"]

    def get_k8s_object(self) -> V1Deployment:
        """Creates a body for this Deployment"""

        # Return a V1Deployment object to create a ClusterRole
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_deployment.py
        _v1_deployment = V1Deployment(
            api_version=self.api_version,
            kind=self.kind,
            metadata=self.metadata.get_k8s_object(),
            spec=self.spec.get_k8s_object(),
        )
        return _v1_deployment

    def get_active_k8s_object(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> Optional[V1Deployment]:
        """Returns the "Active" Deployment from the cluster"""

        _active_deploy: Optional[V1Deployment] = None
        _active_deploys: Optional[List[V1Deployment]] = self.read_from_cluster(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        # logger.debug(f"_active_deploys: {_active_deploys}")
        if _active_deploys is None:
            return None

        _active_deploys_dict = {
            _deploy.metadata.name: _deploy for _deploy in _active_deploys
        }

        _deploy_name = self.get_resource_name()
        if _deploy_name in _active_deploys_dict:
            _active_deploy = _active_deploys_dict[_deploy_name]
            self.__setattr__("v1_deployment", _active_deploy)
            # logger.debug(f"Found {_deploy_name}")
        return _active_deploy

    @staticmethod
    def read_from_cluster(
        k8s_api: K8sApi, namespace: Optional[str] = None, **kwargs: str
    ) -> Optional[List[V1Deployment]]:
        """Reads Deployments from K8s cluster.

        Args:
            k8s_api: K8sApi for the cluster
            namespace: Ignored for cluter roles.
        """
        k8s_apps_v1_api: AppsV1Api = k8s_api.k8s_apps_v1_api
        deploy_list: Optional[V1DeploymentList] = None
        if namespace:
            # logger.debug(f"Getting Deploys for ns: {namespace}")
            deploy_list = k8s_apps_v1_api.list_namespaced_deployment(
                namespace=namespace
            )
        else:
            # logger.debug("Getting Deploys for all namespaces")
            deploy_list = k8s_apps_v1_api.list_deployment_for_all_namespaces()

        deploys: Optional[List[V1Deployment]] = None
        if deploy_list:
            deploys = deploy_list.items
        # logger.debug(f"deploys: {deploys}")
        # logger.debug(f"deploys type: {type(deploys)}")

        return deploys

    def _create(self, k8s_api: K8sApi, namespace: Optional[str] = None) -> bool:

        k8s_apps_v1_api: AppsV1Api = k8s_api.k8s_apps_v1_api
        logger.debug("Creating: {}".format(self.get_resource_name()))

        _k8s_object: V1Deployment = self.get_k8s_object()
        v1_deployment: V1Deployment = k8s_apps_v1_api.create_namespaced_deployment(
            namespace=namespace, body=_k8s_object
        )
        # logger.debug("Created:\n{}".format(pformat(v1_deployment.to_dict(), indent=2)))
        if v1_deployment.metadata.creation_timestamp is not None:
            logger.debug("Deployment Created")
            self.__setattr__("v1_deployment", v1_deployment)
            return True
        logger.error("Deployment could not be created")
        return False

    def _delete(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_termination: Optional[bool] = False,
    ) -> bool:

        k8s_apps_v1_api: AppsV1Api = k8s_api.k8s_apps_v1_api
        # TODO: Implement wait_for_termination
        _deploy_name = self.get_resource_name()
        logger.debug("Deleting: {}".format(_deploy_name))

        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_status.py
        _delete_status: V1Status = k8s_apps_v1_api.delete_namespaced_deployment(
            name=_deploy_name, namespace=namespace
        )
        # logger.debug("_delete_status: {}".format(pformat(_delete_status, indent=2)))
        if _delete_status.status == "Success":
            logger.debug("Deployment Deleted")
            self.__setattr__("v1_deployment", None)
            return True
        return False

    def _update(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        wait_for_completion: Optional[bool] = False,
    ) -> bool:

        k8s_apps_v1_api: AppsV1Api = k8s_api.k8s_apps_v1_api
        # TODO: Implement wait_for_completion
        _deploy_name = self.get_resource_name()
        logger.debug("Updating: {}".format(_deploy_name))

        _k8s_object: V1Deployment = self.get_k8s_object()
        v1_deployment: V1Deployment = k8s_apps_v1_api.patch_namespaced_deployment(
            name=_deploy_name, namespace=namespace, body=_k8s_object
        )
        # logger.debug("Updated:\n{}".format(pformat(v1_deployment.to_dict(), indent=2)))
        if v1_deployment.metadata.creation_timestamp is not None:
            logger.debug("Deployment Updated")
            self.__setattr__("v1_deployment", v1_deployment)
            return True
        logger.error("Deployment could not be updated")
        return False

    def is_active_on_cluster(
        self, k8s_api: K8sApi, namespace: Optional[str] = None
    ) -> bool:

        _active_deploy: Optional[V1Deployment] = self.get_active_k8s_object(
            k8s_api=k8s_api,
            namespace=namespace,
        )
        if _active_deploy:
            return True
        return False

    def create_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        only_if_not_active: Optional[bool] = True,
    ) -> bool:

        if only_if_not_active and self.is_active_on_cluster(k8s_api, namespace):
            logger.debug(
                f"Deployment {self.get_resource_name()} is already active, skipping create"
            )
            return True
        return self._create(k8s_api, namespace)

    def delete_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._delete(k8s_api, namespace)
        logger.debug(
            f"Deployment {self.get_resource_name()} does not exist, skipping delete"
        )
        return True

    def update_if(
        self,
        k8s_api: K8sApi,
        namespace: Optional[str] = None,
        is_active: Optional[bool] = True,
    ) -> bool:

        if is_active and self.is_active_on_cluster(k8s_api):
            return self._update(k8s_api, namespace)
        logger.debug(
            f"Deployment {self.get_resource_name()} does not exist, skipping update"
        )
        return True
