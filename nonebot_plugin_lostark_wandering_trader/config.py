from pydantic import BaseModel


class ScopedConfig(BaseModel):
    user_ids: list[int] = []
    group_ids: list[int] = []
    time: int = 1
    server_id: int = 14


class Config(BaseModel):
    trader: ScopedConfig