from pydantic import BaseModel
from typing import List

class PreferencesSchema(BaseModel):
    timezone: str

class UserSchema(BaseModel):
    username: str
    password: str
    roles: List[str]
    preferences: PreferencesSchema
    active: bool
    created_ts: int
