from pydantic import BaseModel
from typing import Optional

class EmailRequest(BaseModel):
    email_text: Optional[str] = None

class EmailResponse(BaseModel):
    category: str
    confidence: float
    suggested_response: str
    original_text_preview: str