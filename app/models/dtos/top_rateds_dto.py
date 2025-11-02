from pydantic import BaseModel, Field
from typing import Optional

class TopRatedsDto(BaseModel):
    top_books: Optional[list] = Field([])