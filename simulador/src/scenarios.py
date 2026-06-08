from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from random import Random

class Scenario(StrEnum):
    """Scenarios supported by the simulator."""
    NORMAL = "NORMAL"
    CLOUDY = "CLOUDY"
    SHADING = "SHADING"
    OVERHEATING = "OVERHEATING"
    ELECTRICAL_FAULT = "ELECTRICAL_FAULT"
    COMMUNICATION_LOSS = "COMMUNICATION_LOSS"

@dataclass(frozen=True)
class SensorValues:
    """raw sensor values before creating of the MQTT message."""
    voltage: float
    current: float
    power: float
    irradiance: float
    ambient_temperature: float
    panel_temperature: float
    relative_humidity: float

def apply_scenario(values: SensorValues, scenario: Scenario, random_generator: Random) -> SensorValues:
    """Modify generated values according to a simulation scenario."""

    if scenario == Scenario.NORMAL:
        return values

    elif scenario == Scenario.CLOUDY:
        irradiance_factor = random_generator.uniform(0.2, 0.60)
        irradiance = values.irradiance * irradiance_factor
        power = values.power * irradiance_factor
        current = power / values.voltage if values.voltage > 0 else 0
        return replace(
            values,
            irradiance=irradiance,
            power=power,
            current=current,
            relative_humidity=min(
                100, values.relative_humidity + random_generator.uniform(5, 15)
            )
        )

    elif scenario == Scenario.SHADING:
        output_factor = random_generator.uniform(0.25, 0.55)
        power = values.power * output_factor
        current = power / values.voltage if values.voltage > 0 else 0

        return replace(
            values,
            current=current,
            power=power,
        )

    elif scenario == Scenario.OVERHEATING:
        additional_temperature = random_generator.uniform(15, 28)
        temperature_penalty = random_generator.uniform(0.72, 0.88)
        power = values.power * temperature_penalty
        current = power / values.voltage if values.voltage > 0 else 0

        return replace(
            values,
            current=current,
            power=power,
            panel_temperature=(
                values.panel_temperature + additional_temperature
            ),
        )

    elif scenario == Scenario.ELECTRICAL_FAULT:
        voltage = values.voltage * random_generator.uniform(0.15, 0.45)
        current = values.current * random_generator.uniform(0.05, 0.25)

        return replace(
            values,
            voltage=voltage,
            current=current,
            power=voltage * current,
        )

    # COMMUNICATION_LOSS is handled by main.py by skipping publications.
    return values