from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

def to_camel_case(value: str) -> str:
    """Convert a snake_case name to camelCase."""

    first, *remaining = value.split("_")
    return first + "".join(word.capitalize() for word in remaining)

class DataQuality(StrEnum):
    """Supported data-quality values."""
    VALID = "VALID"
    ESTIMATED = "ESTIMATED"
    INVALID = "INVALID"
    MISSING = "MISSING"

class DeviceStatus(StrEnum):
    """Supported device connection states."""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    WARNING = "WARNING"
    ERROR = "ERROR"

class TelemetryMessage(BaseModel):
    """Telemetry contract published through MQTT."""

    model_config = ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )

    schema_version: str = "1.0"
    message_id: str
    device_id: str
    timestamp: datetime

    voltage: float = Field(ge=0)
    current: float = Field(ge=0)
    power: float = Field(ge=0)
    irradiance: float = Field(ge=0)

    ambient_temperature: float
    panel_temperature: float

    relative_humidity: float = Field(ge=0, le=100)

    quality: DataQuality = DataQuality.VALID
    scenario: str = "NORMAL"

    @field_validator("device_id")
    @classmethod
    def validate_device_id(cls, value: str) -> str:
        """Reject blank device identifiers."""
        if not value.strip():
            raise ValueError("device_id cannot be empty.")
        return value


    def to_json(self) -> str:
        """Serialize the message using the public MQTT field names."""
        return self.model_dump_json(by_alias=True, exclude_none=True)


class StatusMessage(BaseModel):
    """Device status contract published through MQTT."""
    model_config =  ConfigDict(
        alias_generator=to_camel_case,
        populate_by_name=True,
    )

    schema_version: str = "1.0"
    message_id: str
    device_id: str
    timestamp: datetime
    status: DeviceStatus

    def to_json(self) -> str:
        """Serialize status using camelCase field names."""
        return self.model_dump_json(by_alias=True, exclude_none=True)
