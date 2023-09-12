from pydantic import BaseModel


class ScopedConfig(BaseModel):
    user_ids: list[int] = []
    group_ids: list[int] = []
    time: int = 1
    server_id: int = 14
    rarity: list[str] = []
    send_type: list[str] = []
    cards: list[str] = []
    location_image: bool = True


class Config(BaseModel):
    trader: ScopedConfig