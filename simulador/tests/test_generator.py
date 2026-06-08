from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from src.schemas import TelemetryMessage


def create_valid_message() -> TelemetryMessage:
    return TelemetryMessage(
        message_id="9a39231b-e049-4d8e-9427-df702574ebfb",
        device_id="panel-001",
        timestamp=datetime.now(UTC),
        voltage=32.5,
        current=7.8,
        power=253.5,
        irradiance=780,
        ambient_temperature=19.2,
        panel_temperature=35.4,
        relative_humidity=67,
    )


def test_schema_serializes_fields_in_camel_case() -> None:
    message = create_valid_message()

    serialized = message.model_dump(
        by_alias=True
    )

    assert serialized["deviceId"] == "panel-001"
    assert serialized["relativeHumidity"] == 67
    assert serialized["schemaVersion"] == "1.0"


def test_schema_rejects_negative_voltage() -> None:
    with pytest.raises(ValidationError):
        TelemetryMessage(
            message_id="message-001",
            device_id="panel-001",
            timestamp=datetime.now(UTC),
            voltage=-1,
            current=5,
            power=10,
            irradiance=500,
            ambient_temperature=18,
            panel_temperature=30,
            relative_humidity=60,
        )


def test_schema_rejects_humidity_above_one_hundred() -> None:
    with pytest.raises(ValidationError):
        TelemetryMessage(
            message_id="message-001",
            device_id="panel-001",
            timestamp=datetime.now(UTC),
            voltage=30,
            current=5,
            power=150,
            irradiance=500,
            ambient_temperature=18,
            panel_temperature=30,
            relative_humidity=101,
        )