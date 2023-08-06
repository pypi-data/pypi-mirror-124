from pathlib import Path
from typing import Optional, List, Any

from pydantic import BaseModel, validator

from pak8.app import Pak8App


class DockerPak8Conf(BaseModel):
    enabled: bool = True
    network: Optional[str] = None
    endpoint: Optional[str] = None
    compose_file_path: Optional[Path] = None
    apps: Optional[List[Any]] = None

    @validator("apps")
    def apps_are_valid(cls, _app_list):
        for _app in _app_list:
            if not isinstance(_app, Pak8App):
                raise TypeError("App not of type Pak8App: {}".format(_app))
        return _app_list
