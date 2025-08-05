from typing import Literal, Union

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant"]
    type: Literal["text", "cta_confirmation"]
    content: str


class Conversation(BaseModel):
    id: Union[str, None] = None
    messages: list[Message] = []
