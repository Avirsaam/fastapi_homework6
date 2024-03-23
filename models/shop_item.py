from pydantic import BaseModel, Field

class ShopItem(BaseModel):
    id: int | None = None
    name: str = Field(min_length=1, max_length=128)
    description: str = Field(min_length=3, max_length=128)
    price: float = Field(gt=0)