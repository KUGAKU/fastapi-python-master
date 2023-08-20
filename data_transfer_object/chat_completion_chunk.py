from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Choice:
    index: int
    delta: Dict[str, Any]
    finish_reason: str


@dataclass
class ChatCompletionChunk:
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice] = field(default_factory=list)
