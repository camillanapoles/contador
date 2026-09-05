import json
from typing import List, Optional
from pydantic import BaseModel

class Stage(BaseModel):
    id: str
    name: str = ""
    objetivo: str = ""
    entregavel: str = ""
    requisito: str = ""
    stack: str = ""
    ucs: str = ""
    tests: List[str] = []
    status: str = "blocked"  # blocked|ready|running|done|failed

class Project(BaseModel):
    name: str
    repo: str = ""
    stages: List[Stage] = []

class Event(BaseModel):
    type: str  # run.finished | stage.override | stage.failed
    payload: dict = {}

    def payload_json(self) -> str:
        return json.dumps(self.payload, ensure_ascii=False)
