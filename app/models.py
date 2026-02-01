from pydantic import BaseModel
from typing import List, Dict, Any

class InputModerationRequest(BaseModel):
    user_input: str

class OutputModerationRequest(BaseModel):
    ai_response: str

class ModerationResult(BaseModel):
    passed: bool
    score: float
    metric_name: str
    reason: str

class ModerationResponse(BaseModel):
    results: List[ModerationResult]
    overall_passed: bool
    details: Dict[str, Any]
