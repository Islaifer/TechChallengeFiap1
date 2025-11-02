from pydantic import BaseModel, Field
from typing import Optional

class StatsDto(BaseModel):
    avg_price_by_category: Optional[list] = Field([])
    book_by_category: Optional[list] = Field([])