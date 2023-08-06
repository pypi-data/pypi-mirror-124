from typing import List, Union

import pydantic

from classiq_interface.status import Status


class AnglesResult(pydantic.BaseModel):
    status: Status
    details: List[float]
