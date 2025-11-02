from pydantic import BaseModel, Field
from typing import Optional

class OverviewDto(BaseModel):
    total_books: Optional[int] = Field(0)
    average_price: Optional[float] = Field(0)
    top_books: Optional[list] = Field([])
    
