from pydantic import BaseModel


class ScopedConfig(BaseModel):
    user_ids: list = []
    group_ids: list = []
    time: int = 1
    server_id: int = 14
    rarity: list = []
    send_type: list = []
    cards: list = []
    location_image: bool = True


class Config(BaseModel):
    trader: ScopedConfig