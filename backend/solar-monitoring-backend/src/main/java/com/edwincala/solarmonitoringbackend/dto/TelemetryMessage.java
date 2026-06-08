package com.edwincala.solarmonitoringbackend.dto;

import jakarta.validation.constraints.*;

import java.time.Instant;
import java.util.UUID;

public record TelemetryMessage(
        @NotBlank
        String schemaVersion,

        @NotNull
        UUID messageId,

        @NotBlank
        String deviceId,

        @NotNull
        Instant timestamp,

        @PositiveOrZero
        Double voltage,

        @PositiveOrZero
        Double current,

        @PositiveOrZero
        Double power,

        @PositiveOrZero
        Double irradiance,

        Double ambientTemperature,

        Double panelTemperature,

        @DecimalMin("0.0")
        @DecimalMax("100.0")
        Double relativeHumidity,

        @NotBlank
        String quality
){}
