from pydantic import BaseModel, Field
from typing import Optional

class BookDto(BaseModel):
    id: Optional[str] = Field(0)
    title: Optional[str] = Field(None)
    category: Optional[str] = Field(None)
    price: float = Field(0)
    availability: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    rating: Optional[str] = Field(None)
    last_updated: Optional[str] = Field(None)
    
    def from_json(self, json_obj):
        self.id = json_obj['id']
        self.title = json_obj['title']
        self.price = json_obj['price']
        self.category = json_obj['category']
        self.availability = json_obj['availability']
        self.image_url = json_obj['image_url']
        self.rating = json_obj['rating']
        self.last_updated = json_obj['last_updated']
        
    