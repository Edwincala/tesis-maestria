package com.edwincala.solarmonitoringbackend.mqtt;

import com.edwincala.solarmonitoringbackend.service.TelemetryProcessingService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageHandler;
import org.springframework.messaging.MessagingException;
import org.springframework.stereotype.Component;

@Component
public class MqttTelemetryMessageHandler implements MessageHandler {
    public static final Logger LOGGER = LoggerFactory.getLogger(MqttTelemetryMessageHandler.class);

    private final TelemetryProcessingService telemetryProcessingService;

    public MqttTelemetryMessageHandler(TelemetryProcessingService telemetryProcessingService){
        this.telemetryProcessingService = telemetryProcessingService;
    }

    @Override
    public void handleMessage(Message<?> message) throws MessagingException {
        String topic = String.valueOf(message.getHeaders().get(MqttHeaders.RECEIVED_TOPIC));

        String payload = String.valueOf(message.getPayload());
        LOGGER.debug("MQTT message received from topic {}: {}", topic, payload);

        telemetryProcessingService.process(topic, payload);
    }
}
