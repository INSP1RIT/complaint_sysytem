from datetime import datetime

from pydantic import BaseModel

from models.enums import State
from schemas.base import BaseComplaint


class ComplaintOut(BaseComplaint):
    id: int
    created_at: datetime
    status: State