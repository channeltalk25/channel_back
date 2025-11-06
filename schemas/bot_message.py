from pydantic import BaseModel
from typing import List, Dict

class MessageBlock(BaseModel):
    type: str
    value: str

class MessageBody(BaseModel):
    blocks: List[MessageBlock]
    options: List[str]