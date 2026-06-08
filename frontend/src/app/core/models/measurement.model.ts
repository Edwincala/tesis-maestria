export type DataQuality = 
    | 'VALID' 
    | 'ESTIMATED' 
    | 'INVALID' 
    | 'MISSING';

export interface Measurement {
    id?: string;
    messageId: string;
    schemaVersion?: string;
    deviceId: string;
    timestamp?: string
    measuredAt?: string;
    receivedAt?: string;
    voltage: number;
    current: number;
    power: number;
    irradiance: number;
    ambientTemperature: number;
    panelTemperature: number;
    relativeHumidity: number;
    quality?: DataQuality;
}

export interface MeasurementQueryParams {
    deviceId: string;
    from?: string;
    to?: string;
    page?: number;
    size?: number;
}