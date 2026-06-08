"""Generation of simulated photovoltaic and climate measurements."""

from __future__ import annotations

import math
from datetime import UTC, datetime
from random import Random
from uuid import uuid4
from zoneinfo import ZoneInfo

from src.config import Settings
from src.schemas import DataQuality, TelemetryMessage
from src.scenarios import Scenario, SensorValues, apply_scenario

BOGOTA_TIME_ZONE = ZoneInfo("America/Bogota")


class TelemetryGenerator:
    """Generate photovoltaic telemetry with daily climate variation."""

    def __init__(
        self,
        settings: Settings,
        random_generator: Random | None = None,
    ) -> None:
        self._settings = settings
        self._random = random_generator or Random(
            settings.simulation_random_seed
        )

    def generate(
        self,
        scenario: Scenario = Scenario.NORMAL,
        generated_at: datetime | None = None,
    ) -> TelemetryMessage:
        """Generate one complete telemetry message."""

        timestamp = generated_at or datetime.now(UTC)

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=UTC)

        local_timestamp = timestamp.astimezone(
            BOGOTA_TIME_ZONE
        )

        values = self._generate_base_values(
            local_timestamp
        )

        values = apply_scenario(
            values,
            scenario,
            self._random,
        )

        return TelemetryMessage(
            message_id=str(uuid4()),
            device_id=self._settings.device_id,
            timestamp=timestamp.astimezone(UTC),
            voltage=round(max(values.voltage, 0), 2),
            current=round(max(values.current, 0), 2),
            power=round(max(values.power, 0), 2),
            irradiance=round(max(values.irradiance, 0), 2),
            ambient_temperature=round(
                values.ambient_temperature,
                2,
            ),
            panel_temperature=round(
                values.panel_temperature,
                2,
            ),
            relative_humidity=round(
                min(
                    max(values.relative_humidity, 0),
                    100,
                ),
                2,
            ),
            quality=DataQuality.VALID,
            scenario=scenario.value,
        )

    def _generate_base_values(
        self,
        local_timestamp: datetime,
    ) -> SensorValues:
        """Generate climate and electrical values for a local time."""

        decimal_hour = (
            local_timestamp.hour
            + local_timestamp.minute / 60
            + local_timestamp.second / 3600
        )

        irradiance = self._generate_irradiance(
            decimal_hour
        )

        ambient_temperature = (
            self._generate_ambient_temperature(
                decimal_hour
            )
        )

        relative_humidity = (
            self._generate_relative_humidity(
                decimal_hour
            )
        )

        panel_temperature = (
            ambient_temperature
            + irradiance * 0.027
            + self._random.uniform(-1.2, 1.2)
        )

        temperature_difference = (
            panel_temperature - 25
        )

        temperature_factor = max(
            0,
            1
            + self._settings.panel_temperature_coefficient
            * temperature_difference,
        )

        power = (
            self._settings.panel_rated_power_w
            * irradiance
            / 1000
            * temperature_factor
        )

        power *= self._random.uniform(0.97, 1.02)

        voltage_factor = max(
            0.70,
            1 - max(panel_temperature - 25, 0) * 0.0025,
        )

        voltage = (
            self._settings.panel_reference_voltage_v
            * voltage_factor
        )

        if irradiance < 20:
            power = 0
            voltage = self._random.uniform(0, 4)

        current = power / voltage if voltage > 0 else 0

        return SensorValues(
            voltage=voltage,
            current=current,
            power=power,
            irradiance=irradiance,
            ambient_temperature=ambient_temperature,
            panel_temperature=panel_temperature,
            relative_humidity=relative_humidity,
        )

    def _generate_irradiance(
        self,
        decimal_hour: float,
    ) -> float:
        """Generate a daylight irradiance curve with cloud variation."""

        sunrise = 5.5
        sunset = 18.3

        if not sunrise <= decimal_hour <= sunset:
            return 0

        daylight_progress = (
            decimal_hour - sunrise
        ) / (sunset - sunrise)

        clear_sky_irradiance = (
            980
            * math.sin(
                math.pi * daylight_progress
            )
        )

        cloud_factor = self._random.uniform(
            0.65,
            1.0,
        )

        short_variation = self._random.uniform(
            -35,
            35,
        )

        return max(
            0,
            clear_sky_irradiance
            * cloud_factor
            + short_variation,
        )

    def _generate_ambient_temperature(
        self,
        decimal_hour: float,
    ) -> float:
        """Generate a moderate daily temperature cycle."""

        daily_cycle = math.sin(
            2
            * math.pi
            * (decimal_hour - 9)
            / 24
        )

        return (
            15
            + 4.2 * daily_cycle
            + self._random.uniform(-0.8, 0.8)
        )

    def _generate_relative_humidity(
        self,
        decimal_hour: float,
    ) -> float:
        """Generate humidity inversely related to temperature."""

        daily_cycle = math.sin(
            2
            * math.pi
            * (decimal_hour - 9)
            / 24
        )

        return (
            74
            - 13 * daily_cycle
            + self._random.uniform(-4, 4)
        )