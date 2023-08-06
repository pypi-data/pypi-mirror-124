from typing import Optional, Union

from kubernetes.client.models.v1_deployment_strategy import V1DeploymentStrategy
from kubernetes.client.models.v1_rolling_update_deployment import (
    V1RollingUpdateDeployment,
)
from pydantic import BaseModel


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#rollingupdatedeployment-v1-apps
class RollingUpdateDeployment(BaseModel):
    max_surge: Union[int, str]
    max_unavailable: Union[int, str]

    def get_k8s_object(self) -> V1RollingUpdateDeployment:

        # Return a V1RollingUpdateDeployment object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_rolling_update_deployment.py
        _v1_rolling_update_deployment = V1RollingUpdateDeployment(
            max_surge=self.max_surge,
            max_unavailable=self.max_unavailable,
        )
        return _v1_rolling_update_deployment

    class Config:
        arbitrary_types_allowed = True


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#deploymentstrategy-v1-apps
class DeploymentStrategy(BaseModel):
    rolling_update: RollingUpdateDeployment
    type: str = "RollingUpdate"

    def get_k8s_object(self) -> V1DeploymentStrategy:

        # Return a V1DeploymentStrategy object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_deployment_strategy.py
        _v1_deployment_strategy = V1DeploymentStrategy(
            rolling_update=self.rolling_update.get_k8s_object(),
            type=self.type,
        )
        return _v1_deployment_strategy

    class Config:
        arbitrary_types_allowed = True
