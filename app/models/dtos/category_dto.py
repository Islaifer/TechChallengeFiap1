from pydantic import BaseModel, Field
from typing import Optional

class CategoryDto(BaseModel):
    category: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    
    def from_json(self, json_data):
        self.category = json_data['category']
        self.url = json_data['url']
