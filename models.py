from pydantic import BaseModel
from typing import Optional

class DocumentSchema(BaseModel):
    id: Optional[str] = None
    filename: str
    content: str
