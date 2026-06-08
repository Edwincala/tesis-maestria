package com.edwincala.solarmonitoringbackend.config;

import com.edwincala.solarmonitoringbackend.mqtt.MqttTelemetryMessageHandler;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.channel.DirectChannel;
import org.springframework.integration.mqtt.core.DefaultMqttPahoClientFactory;
import org.springframework.integration.mqtt.inbound.MqttPahoMessageDrivenChannelAdapter;
import org.springframework.messaging.MessageChannel;
import org.springframework.messaging.MessageHandler;

@Configuration
public class MqttConfig {
    @Bean
    public DefaultMqttPahoClientFactory mqttClientFactory(MqttProperties mqttProperties){
        MqttConnectOptions options = new MqttConnectOptions();
        options.setServerURIs(new String[]{mqttProperties.brokerUrl()});
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);

        if(mqttProperties.username() != null && !mqttProperties.username().isBlank()){
            options.setUserName(mqttProperties.username());
        }

        if(mqttProperties.password() != null && !mqttProperties.password().isBlank()){
            options.setPassword(mqttProperties.password().toCharArray());
        }

        DefaultMqttPahoClientFactory factory = new DefaultMqttPahoClientFactory();
        factory.setConnectionOptions(options);

        return factory;
    }

    @Bean
    public MessageChannel mqttInputChannel(){
        return new DirectChannel();
    }

    @Bean
    public MqttPahoMessageDrivenChannelAdapter mqttInboundAdapter(MqttProperties mqttProperties, DefaultMqttPahoClientFactory mqttClientFactory){
        MqttPahoMessageDrivenChannelAdapter adapter = new MqttPahoMessageDrivenChannelAdapter(
                mqttProperties.clientId(),
                mqttClientFactory,
                mqttProperties.telemetryTopic(),
                mqttProperties.statusTopic(),
                mqttProperties.alertsTopic()
        );

        adapter.setCompletionTimeout(5000);
        adapter.setQos(mqttProperties.qos());
        adapter.setOutputChannel(mqttInputChannel());

        return adapter;
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttInputChannel")
    public MessageHandler mqttMessageHandler(MqttTelemetryMessageHandler handler){
        return handler;
    }
}
