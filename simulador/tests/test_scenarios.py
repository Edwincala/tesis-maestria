from random import Random

from src.scenarios import (
    Scenario,
    SensorValues,
    apply_scenario,
)


def create_values() -> SensorValues:
    return SensorValues(
        voltage=35,
        current=8,
        power=280,
        irradiance=800,
        ambient_temperature=18,
        panel_temperature=38,
        relative_humidity=65,
    )


def test_shading_reduces_generated_power() -> None:
    original = create_values()

    modified = apply_scenario(
        original,
        Scenario.SHADING,
        Random(42),
    )

    assert modified.power < original.power
    assert modified.current < original.current


def test_overheating_increases_panel_temperature() -> None:
    original = create_values()

    modified = apply_scenario(
        original,
        Scenario.OVERHEATING,
        Random(42),
    )

    assert modified.panel_temperature > original.panel_temperature
    assert modified.power < original.power


def test_electrical_fault_reduces_voltage_and_current() -> None:
    original = create_values()

    modified = apply_scenario(
        original,
        Scenario.ELECTRICAL_FAULT,
        Random(42),
    )

    assert modified.voltage < original.voltage
    assert modified.current < original.current
    assert modified.power < original.power


def test_cloudy_scenario_reduces_irradiance() -> None:
    original = create_values()

    modified = apply_scenario(
        original,
        Scenario.CLOUDY,
        Random(42),
    )

    assert modified.irradiance < original.irradiance
    assert modified.power < original.power
    assert modified.relative_humidity >= original.relative_humidity


def test_normal_scenario_does_not_modify_values() -> None:
    original = create_values()

    modified = apply_scenario(
        original,
        Scenario.NORMAL,
        Random(42),
    )

    assert modified == original