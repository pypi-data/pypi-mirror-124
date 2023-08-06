from typing import List

from pydantic import BaseModel


class GCSBuckets(BaseModel):
    project_id: str
    bucket_names: List[str]
