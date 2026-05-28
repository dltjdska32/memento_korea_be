
from pydantic import BaseModel

class JwtUserInfo(BaseModel):
    user_id: int
    username: str
    email: str
    role: str