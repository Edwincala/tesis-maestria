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

    findHistory(
        query: MeasurementQueryParams,
    ): Observable<Measurement[]> {
        const baseDate = new Date();

        const measurements: Measurement[] = Array.from(
            { length: 12 },
            (_, index) => {
                const measuredAt = new Date(
                    baseDate.getTime() - index * 5 * 60 * 1000,
                ).toISOString();

                const irradiance = Math.max(0, 780 - index * 18);
                const voltage = Number((32.5 - index * 0.08).toFixed(2));
                const current = Number((7.8 - index * 0.05).toFixed(2));
                const power = Number((voltage * current).toFixed(2));

                return {
                    id: `${index + 1}`,
                    messageId: `mock-message-${index + 1}`,
                    schemaVersion: '1.0',
                    deviceId: query.deviceId,
                    timestamp: measuredAt,
                    measuredAt,
                    receivedAt: measuredAt,
                    voltage,
                    current,
                    power,
                    irradiance,
                    ambientTemperature: Number((19.2 + index * 0.05).toFixed(2)),
                    panelTemperature: Number((35.4 + index * 0.12).toFixed(2)),
                    relativeHumidity: Number((67 - index * 0.3).toFixed(2)),
                    quality: 'VALID',
                };
            },
        );

        return of(measurements.reverse());
    }
}
