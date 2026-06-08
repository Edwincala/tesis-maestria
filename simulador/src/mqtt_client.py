"""MQTT publisher used by the simulator."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from uuid import uuid4

import paho.mqtt.client as mqtt

from src.config import Settings
from src.schemas import (
    DeviceStatus,
    StatusMessage,
    TelemetryMessage,
)

logger = logging.getLogger(__name__)


class MqttPublisher:
    """Manage MQTT connection and publication."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

        self._client = mqtt.Client(
            callback_api_version=(
                mqtt.CallbackAPIVersion.VERSION2
            ),
            client_id=settings.mqtt_client_id,
            protocol=mqtt.MQTTv311,
        )

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        if (
            settings.mqtt_username
            and settings.mqtt_password
        ):
            self._client.username_pw_set(
                settings.mqtt_username,
                settings.mqtt_password,
            )

        offline_message = self._build_status_message(
            DeviceStatus.OFFLINE
        )

        self._client.will_set(
            topic=settings.status_topic,
            payload=offline_message.to_json(),
            qos=settings.mqtt_qos,
            retain=True,
        )

    def connect(self) -> None:
        """Connect to the MQTT broker and start its network loop."""

        logger.info(
            "Connecting MQTT client %s to %s:%s",
            self._settings.mqtt_client_id,
            self._settings.mqtt_host,
            self._settings.mqtt_port,
        )

        self._client.connect(
            host=self._settings.mqtt_host,
            port=self._settings.mqtt_port,
            keepalive=(
                self._settings.mqtt_keepalive_seconds
            ),
        )

        self._client.loop_start()

    def disconnect(self) -> None:
        """Publish OFFLINE state and close the MQTT connection."""

        try:
            self.publish_status(
                DeviceStatus.OFFLINE
            )
        finally:
            self._client.disconnect()
            self._client.loop_stop()

    def publish_telemetry(
        self,
        message: TelemetryMessage,
    ) -> None:
        """Publish one telemetry message."""

        result = self._client.publish(
            topic=self._settings.telemetry_topic,
            payload=message.to_json(),
            qos=self._settings.mqtt_qos,
            retain=False,
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(
                "Unable to publish telemetry. "
                f"MQTT result code: {result.rc}"
            )

        logger.info(
            "Telemetry published: device=%s message_id=%s "
            "scenario=%s power=%.2f W",
            message.device_id,
            message.message_id,
            message.scenario,
            message.power,
        )

    def publish_status(
        self,
        status: DeviceStatus,
    ) -> None:
        """Publish a retained device-status message."""

        message = self._build_status_message(
            status
        )

        result = self._client.publish(
            topic=self._settings.status_topic,
            payload=message.to_json(),
            qos=self._settings.mqtt_qos,
            retain=True,
        )

        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.warning(
                "Unable to publish status %s. MQTT code: %s",
                status,
                result.rc,
            )

    def _build_status_message(
        self,
        status: DeviceStatus,
    ) -> StatusMessage:
        """Create a status message."""

        return StatusMessage(
            message_id=str(uuid4()),
            device_id=self._settings.device_id,
            timestamp=datetime.now(UTC),
            status=status,
        )

    def _on_connect(
        self,
        client: mqtt.Client,
        userdata: object,
        flags: mqtt.ConnectFlags,
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None,
    ) -> None:
        """Handle a successful or failed MQTT connection."""

        if reason_code == 0:
            logger.info(
                "Connected successfully to MQTT broker."
            )
            self.publish_status(
                DeviceStatus.ONLINE
            )
            return

        logger.error(
            "MQTT connection failed: %s",
            reason_code,
        )

    def _on_disconnect(
        self,
        client: mqtt.Client,
        userdata: object,
        disconnect_flags: (
            mqtt.DisconnectFlags
        ),
        reason_code: mqtt.ReasonCode,
        properties: mqtt.Properties | None,
    ) -> None:
        """Record MQTT disconnections."""

        if reason_code == 0:
            logger.info(
                "MQTT client disconnected normally."
            )
        else:
            logger.warning(
                "Unexpected MQTT disconnection: %s",
                reason_code,
            )