import { Service } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Measurement, MeasurementQueryParams } from '../models/measurement.model';

@Service()
export class MeasurementService {
    findLatest(deviceId: string): Observable<Measurement> {
        const measurement: Measurement = {
            id: '1',
            messageId: 'mock-message-001',
            schemaVersion: '1.0',
            deviceId,
            timestamp: new Date().toISOString(),
            measuredAt: new Date().toISOString(),
            receivedAt: new Date().toISOString(),
            voltage: 32.5,
            current: 7.8,
            power: 253.5,
            irradiance: 780,
            ambientTemperature: 19.2,
            panelTemperature: 35.4,
            relativeHumidity: 67,
            quality: 'VALID'
        };
        return of(measurement);
    }

    findHistory(query: MeasurementQueryParams): Observable<Measurement[]> {
        const measurements: Measurement[] = [
            {
                id: '1',
                messageId: 'mock-message-002',
                deviceId: query.deviceId,
                measuredAt: new Date().toISOString(),
                voltage: 31.8,
                current: 7.4,
                power: 235.3,
                irradiance: 720,
                ambientTemperature: 18.9,
                panelTemperature: 34.2,
                relativeHumidity: 65,
                quality: 'VALID',
            },
            {
                id: '2',
                messageId: 'mock-message-003',
                deviceId: query.deviceId,
                measuredAt: new Date().toISOString(),
                voltage: 32.1,
                current: 7.6,
                power: 244,
                irradiance: 750,
                ambientTemperature: 19.1,
                panelTemperature: 35,
                relativeHumidity: 66,
                quality: 'VALID',
            },
        ];
        return of(measurements);
    }
}
