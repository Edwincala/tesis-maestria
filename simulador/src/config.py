from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    """Configuration required by the solar sensor simulator."""
    device_id: str
    mqtt_host: str
    mqtt_port: int
    mqtt_username: str | None
    mqtt_password: str | None
    mqtt_client_id: str
    mqtt_qos: int
    mqtt_keepalive_seconds: int
    
    simulation_interval_seconds: float
    simulation_scenario: str
    simulation_random_seed: int | None

    panel_rated_power_w: float
    panel_reference_voltage_v: float
    panel_temperature_coefficient: float

    @property
    def telemetry_topic(self) -> str:
        """Returns the telemetry for the configured device."""
        return f"solar/{self.device_id}/telemetry"

    @property
    def status_topic(self) -> str:
        """Returns the status topic for the configured device."""
        return f"solar/{self.device_id}/status"

    @classmethod
    def from_environment(cls) -> "Settings":
        """Create and validate settings from environment variables."""

        load_dotenv()

        device_id = os.getenv("DEVICE_ID", "panel-001").strip()

        if not device_id:
            raise ValueError("DEVICE_ID cannot be empty.")

        mqtt_qos = int(os.getenv("MQTT_QOS", "1"))

        if mqtt_qos not in {0, 1, 2}:
            raise ValueError("MQTT_QOS must be 0, 1 or 2.")

        interval = float(
            os.getenv(
                "SIMULATION_INTERVAL_SECONDS",
                "5",
            )
        )

        if interval <= 0:
            raise ValueError(
                "SIMULATION_INTERVAL_SECONDS must be greater than zero."
            )

        seed_value = os.getenv("SIMULATION_RANDOM_SEED", "").strip()
        random_seed = int(seed_value) if seed_value else None

        return cls(
            device_id=device_id,
            mqtt_host=os.getenv("MQTT_HOST", "localhost"),
            mqtt_port=int(os.getenv("MQTT_PORT", "1883")),
            mqtt_username=os.getenv("MQTT_USERNAME") or None,
            mqtt_password=os.getenv("MQTT_PASSWORD") or None,
            mqtt_client_id=os.getenv(
                "MQTT_CLIENT_ID",
                f"solar-simulator-{device_id}",
            ),
            mqtt_qos=mqtt_qos,
            mqtt_keepalive_seconds=int(
                os.getenv(
                    "MQTT_KEEPALIVE_SECONDS",
                    "60",
                )
            ),
            simulation_interval_seconds=interval,
            simulation_scenario=os.getenv(
                "SIMULATION_SCENARIO",
                "NORMAL",
            ).upper(),
            simulation_random_seed=random_seed,
            panel_rated_power_w=float(
                os.getenv(
                    "PANEL_RATED_POWER_W",
                    "350",
                )
            ),
            panel_reference_voltage_v=float(
                os.getenv(
                    "PANEL_REFERENCE_VOLTAGE_V",
                    "36",
                )
            ),
            panel_temperature_coefficient=float(
                os.getenv(
                    "PANEL_TEMPERATURE_COEFFICIENT",
                    "-0.004",
                )
            ),
        )