from typing import List

from pydantic import BaseModel


class CreatePolicyRule(BaseModel):
    api_groups: List[str]
    resources: List[str]
    verbs: List[str]
