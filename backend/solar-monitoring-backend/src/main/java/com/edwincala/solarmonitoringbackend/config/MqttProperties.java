package com.edwincala.solarmonitoringbackend.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "mqtt")
public record MqttProperties (
    String host,
    int port,
    String username,
    String password,
    String clientId,
    int qos,
    String telemetryTopic,
    String statusTopic,
    String alertsTopic
){
    public String brokerUrl(){
        return "tcp://" + host + ":" + port;
    }
}
