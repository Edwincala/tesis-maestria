package com.edwincala.solarmonitoringbackend.service;

import com.edwincala.solarmonitoringbackend.dto.TelemetryMessage;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.Set;

@Service
public class TelemetryProcessingService {
    private static final Logger LOGGER = LoggerFactory.getLogger(TelemetryProcessingService.class);

    private static final String SUPPORTED_SCHEMA_VERSION = "1.0";

    private final ObjectMapper objectMapper;

    private final Validator validator;

    public TelemetryProcessingService(ObjectMapper objectMapper, Validator validator){
        this.objectMapper = objectMapper;
        this.validator = validator;
    }

    public void process(String topic, String payload){
        try {
            TelemetryMessage message = objectMapper.readValue(payload, TelemetryMessage.class);
            validateMessage(topic, message);

            LOGGER.info("Valid telemetry received, deviceId={}, messageId={}, timestamp={}", message.deviceId(), message.messageId(), message.timestamp());
        } catch (JsonProcessingException exception){
            LOGGER.warn("Invalid JSON received from topic {}. Error: {}", topic, exception.getMessage());
        } catch (IllegalArgumentException exception) {
            LOGGER.warn("Invalid telemetry message received from topic {}. Error: {}", topic, exception.getMessage());
        } catch (Exception exception){
            LOGGER.error("Unexpected error processing MQTT message from topic {}", topic, exception);
        }
    }

    private void validateMessage(String topic, TelemetryMessage message){
        Set<ConstraintViolation<TelemetryMessage>> violations = validator.validate(message);

        if(!violations.isEmpty()) {
            String errors = violations
                    .stream()
                    .map(violation -> violation
                            .getPropertyPath() + " " + violation.getMessage())
                    .reduce((a, b) -> a + ";" + b).orElse("Unknown validation error");
            throw new IllegalArgumentException(errors);
        }

        if(!SUPPORTED_SCHEMA_VERSION.equals(message.schemaVersion())){
            throw new IllegalArgumentException(
                    "Unsupported schema version: " + message.schemaVersion()
            );
        }

        String deviceIdFromTopic = extractDeviceIdFromTopic(topic);

        if(!deviceIdFromTopic.equals(message.deviceId())){
            throw new IllegalArgumentException(
                    "DeviceId mismatch. Topic deviceId=" + deviceIdFromTopic + ", payload deviceId=" + message.deviceId()
            );
        }

        if(!"VALID".equals(message.quality())
                && !"ESTIMATED".equals(message.quality())
                && !"INVALID".equals(message.quality())
                && !"MISSING".equals(message.quality())){
            throw new IllegalArgumentException(
                    "Unsupported quality value: " + message.quality()
            );
        }
    }

    private String extractDeviceIdFromTopic(String topic){
        String[] parts = topic.split("/");

        if(parts.length != 3){
            throw new IllegalArgumentException(
                    "Invalid MQTT topic structure " + topic
            );
        }

        if(!"solar".equals(parts[0])) {
            throw new IllegalArgumentException(
                    "Invalid MQTT topic domain " + parts[0]
            );
        }

        if(!"telemetry".equals(parts[2])
                && !"status".equals(parts[2])
                && !"alerts".equals(parts[2])
        ){
            throw new IllegalArgumentException(
                    "Invalid MQTT message type: " + parts[2]
            );
        }

        return parts[1];
    }
}
