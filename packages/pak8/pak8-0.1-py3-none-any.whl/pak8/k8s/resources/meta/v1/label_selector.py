from typing import Dict, Optional

from kubernetes.client.models.v1_label_selector import V1LabelSelector
from pydantic import BaseModel, Field


# https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.14/#labelselector-v1-meta
class LabelSelector(BaseModel):
    match_labels: Dict[str, str] = Field(None, alias="matchLabels")

    def get_k8s_object(self) -> V1LabelSelector:
        # Return a V1LabelSelector object
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/client/models/v1_label_selector.py
        _v1_label_selector = V1LabelSelector(
            match_labels=self.match_labels,
        )
        return _v1_label_selector

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
