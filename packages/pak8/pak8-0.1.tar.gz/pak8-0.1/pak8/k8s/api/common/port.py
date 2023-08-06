from typing import Optional

from pydantic import BaseModel

import pak8.k8s.enums as k8s_enums


class CreatePortData(BaseModel):
    name: str
    container_port: int
    svc_port: Optional[int] = None
    protocol: Optional[k8s_enums.Protocol] = k8s_enums.Protocol.TCP
