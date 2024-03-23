from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ModelOrder(BaseModel):
    id: int | None = None
    user_id: int
    shop_item_id: int
    timestamp: datetime
    is_completed: bool