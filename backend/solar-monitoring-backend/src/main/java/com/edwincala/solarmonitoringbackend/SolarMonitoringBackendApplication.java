package com.edwincala.solarmonitoringbackend;

import com.edwincala.solarmonitoringbackend.config.MqttProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

@SpringBootApplication
@EnableConfigurationProperties(MqttProperties.class)
public class SolarMonitoringBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(SolarMonitoringBackendApplication.class, args);
    }

}
