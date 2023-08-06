from typing import List

from pydantic import BaseModel


class CloudSQLInstances(BaseModel):
    project_id: str
    instance_ids: List[str]
