"""Entry point for the photovoltaic sensor simulator."""

from __future__ import annotations

import argparse
import logging
import signal
import time
from random import Random

from src.config import Settings
from src.generator import TelemetryGenerator
from src.mqtt_client import MqttPublisher
from src.scenarios import Scenario

logger = logging.getLogger(__name__)

running = True


def stop_application(
    signal_number: int,
    frame: object,
) -> None:
    """Request a graceful application shutdown."""

    del signal_number
    del frame

    global running
    running = False


def parse_arguments() -> argparse.Namespace:
    """Parse optional command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Photovoltaic sensor simulator "
            "for the solar monitoring platform."
        )
    )

    parser.add_argument(
        "--scenario",
        choices=[scenario.value for scenario in Scenario],
        help=(
            "Override SIMULATION_SCENARIO "
            "for this execution."
        ),
    )

    parser.add_argument(
        "--once",
        action="store_true",
        help="Generate and publish only one message.",
    )

    return parser.parse_args()


def main() -> None:
    """Run the simulator until interrupted."""

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )

    arguments = parse_arguments()
    settings = Settings.from_environment()

    scenario_name = (
        arguments.scenario
        or settings.simulation_scenario
    )

    try:
        scenario = Scenario(scenario_name)
    except ValueError as error:
        allowed_values = ", ".join(
            value.value for value in Scenario
        )

        raise ValueError(
            f"Unknown scenario '{scenario_name}'. "
            f"Allowed values: {allowed_values}"
        ) from error

    random_generator = Random(
        settings.simulation_random_seed
    )

    telemetry_generator = TelemetryGenerator(
        settings=settings,
        random_generator=random_generator,
    )

    mqtt_publisher = MqttPublisher(settings)

    signal.signal(
        signal.SIGINT,
        stop_application,
    )
    signal.signal(
        signal.SIGTERM,
        stop_application,
    )

    mqtt_publisher.connect()

    logger.info(
        "Solar simulator started: device=%s "
        "scenario=%s interval=%.2f seconds",
        settings.device_id,
        scenario.value,
        settings.simulation_interval_seconds,
    )

    try:
        while running:
            if (
                scenario
                == Scenario.COMMUNICATION_LOSS
            ):
                logger.warning(
                    "Communication-loss scenario: "
                    "telemetry publication skipped."
                )
            else:
                message = telemetry_generator.generate(
                    scenario=scenario
                )

                mqtt_publisher.publish_telemetry(
                    message
                )

            if arguments.once:
                break

            time.sleep(
                settings.simulation_interval_seconds
            )
    finally:
        mqtt_publisher.disconnect()
        logger.info(
            "Solar simulator stopped."
        )


if __name__ == "__main__":
    main()