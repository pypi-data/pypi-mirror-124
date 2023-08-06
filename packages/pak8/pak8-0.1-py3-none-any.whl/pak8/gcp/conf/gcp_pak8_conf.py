from pathlib import Path
from typing import Optional, Dict, Any, List

from pydantic import BaseModel

from pak8.gcp.api.gke.gke_cluster import CreateGkeClusterData


class Pak8GCPCredentials(BaseModel):
    # Use service_account_key_path when json key is in a file
    service_account_key_path: Optional[Path] = None
    # Use service_account_key_dict when json key is already loaded as a dict
    service_account_key_dict: Optional[Dict[str, Any]] = None


class Pak8GCPConf(BaseModel):
    project_id: str
    zone: str
    credentials: Optional[Pak8GCPCredentials]
    gke: Optional[CreateGkeClusterData]
    gcs: Optional[List[str]]
    cloudsql: Optional[List[str]]
    vpc_network: Optional[str]
