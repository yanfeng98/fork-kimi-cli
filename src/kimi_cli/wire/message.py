from __future__ import annotations

import asyncio
from typing import Any, Literal, cast

from kosong.chat_provider import TokenUsage
from kosong.message import ContentPart, ToolCall, ToolCallPart
from kosong.tooling import ToolResult
from kosong.utils.typing import JsonType
from pydantic import BaseModel, Field, field_serializer, field_validator

from kimi_cli.utils.typing import flatten_union
from kimi_cli.wire.display import DisplayBlock


class TurnBegin(BaseModel):
    user_input: str | list[ContentPart]


class StepBegin(BaseModel):
    n: int


class StepInterrupted(BaseModel):
    pass


class CompactionBegin(BaseModel):
    pass


class CompactionEnd(BaseModel):
    pass


class StatusUpdate(BaseModel):
    context_usage: float | None = None
    token_usage: TokenUsage | None = None
    message_id: str | None = None


class SubagentEvent(BaseModel):
    task_tool_call_id: str
    event: Event

    @field_serializer("event", when_used="json")
    def _serialize_event(self, event: Event) -> dict[str, Any]:
        envelope = WireMessageEnvelope.from_wire_message(event)
        return envelope.model_dump(mode="json")

    @field_validator("event", mode="before")
    @classmethod
    def _validate_event(cls, value: Any) -> Event:
        if is_wire_message(value):
            if is_event(value):
                return value
            raise ValueError("SubagentEvent event must be an Event")

        if not isinstance(value, dict):
            raise ValueError("SubagentEvent event must be a dict")
        event_type = cast(dict[str, Any], value).get("type")
        event_payload = cast(dict[str, Any], value).get("payload")
        envelope = WireMessageEnvelope.model_validate(
            {"type": event_type, "payload": event_payload}
        )
        event = envelope.to_wire_message()
        if not is_event(event):
            raise ValueError("SubagentEvent event must be an Event")
        return cast(Event, event)


class ApprovalRequest(BaseModel):
    id: str
    tool_call_id: str
    sender: str
    action: str
    description: str
    display: list[DisplayBlock] = Field(default_factory=list[DisplayBlock])

    type Response = Literal["approve", "approve_for_session", "reject"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._future = asyncio.Future[ApprovalRequest.Response]()

    async def wait(self) -> Response:
        return await self._future

    def resolve(self, response: ApprovalRequest.Response) -> None:
        self._future.set_result(response)

    @property
    def resolved(self) -> bool:
        return self._future.done()


class ApprovalRequestResolved(BaseModel):
    request_id: str
    response: ApprovalRequest.Response


type Event = (
    TurnBegin
    | StepBegin
    | StepInterrupted
    | CompactionBegin
    | CompactionEnd
    | StatusUpdate
    | ContentPart
    | ToolCall
    | ToolCallPart
    | ToolResult
    | SubagentEvent
    | ApprovalRequestResolved
)


type Request = ApprovalRequest
type WireMessage = Event | Request


_EVENT_TYPES: tuple[type[Event]] = flatten_union(Event)
_REQUEST_TYPES: tuple[type[Request]] = flatten_union(Request)
_WIRE_MESSAGE_TYPES: tuple[type[WireMessage]] = flatten_union(WireMessage)


def is_event(msg: Any) -> bool:
    return isinstance(msg, _EVENT_TYPES)


def is_request(msg: Any) -> bool:
    """Check if the message is a Request."""
    return isinstance(msg, _REQUEST_TYPES)


def is_wire_message(msg: Any) -> bool:
    return isinstance(msg, _WIRE_MESSAGE_TYPES)


_NAME_TO_WIRE_MESSAGE_TYPE: dict[str, type[WireMessage]] = {
    cls.__name__: cls for cls in _WIRE_MESSAGE_TYPES
}


class WireMessageEnvelope(BaseModel):
    type: str
    payload: dict[str, JsonType]

    @classmethod
    def from_wire_message(cls, msg: WireMessage) -> WireMessageEnvelope:
        typename: str | None = None
        for name, typ in _NAME_TO_WIRE_MESSAGE_TYPE.items():
            if issubclass(type(msg), typ):
                typename = name
                break
        assert typename is not None, f"Unknown wire message type: {type(msg)}"
        return cls(
            type=typename,
            payload=msg.model_dump(mode="json"),
        )

    def to_wire_message(self) -> WireMessage:
        msg_type = _NAME_TO_WIRE_MESSAGE_TYPE.get(self.type)
        if msg_type is None:
            raise ValueError(f"Unknown wire message type: {self.type}")
        return msg_type.model_validate(self.payload)
