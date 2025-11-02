from app.core.config.redis_settings import RedisConnection
from fastapi import HTTPException, status
from typing import Any, Dict
from datetime import datetime
import json

class RedisService:
    
    async def save(self, ty: str, key: str, data: Any):
        json_data = json.dumps(data)
        await RedisConnection.hset(ty, key, json_data)
        
    async def save_all(self, ty: str, mapper: Dict[str, Any]):
        data_to_set = {k: json.dumps(v) for k, v in mapper.items()}
        await RedisConnection.hset(ty, mapping=data_to_set)
        
    async def update_last_date(self):
        date = datetime.now()
        last_update = { "last_date": date.isoformat() }
        data_to_set = json.dumps(last_update)
        await RedisConnection.set("LAST_UPDATE", data_to_set)
        
        
    async def get_value(self, ty: str, key: str):
        json_data = await RedisConnection.hget(ty, key)
        if json_data is None:
            raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="Key not found",
        )
        
        return json.loads(json_data)
    
    async def get_all(self, ty: str):
        values = await RedisConnection.hvals(ty)
        return [json.loads(v) for v in values]
    
    async def get_last_update(self):
        value = await RedisConnection.get("LAST_UPDATE");
        return json.loads(value)
    
    async def delete_value(self, ty: str, key: str):
        result = await RedisConnection.delete(ty, key)
        if result == 0:
            raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="Key not found",
        )