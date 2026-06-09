import { Component } from '@angular/core';
import { Measurement, MeasurementVariable } from '../../../../core/models/measurement.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MeasurementService } from '../../../../core/services/measurement';
import { MeasurementLineChart } from '../../../../shared/components/measurement-line-chart/measurement-line-chart';
import { renderText } from 'chart.js/helpers';

interface VariableOption {
  label: string;
  value: MeasurementVariable;
  unit: string;
}

@Component({
  selector: 'app-measurements-history',
  standalone: true,
  imports: [CommonModule, FormsModule, MeasurementLineChart],
  templateUrl: './measurements-history.html',
})
export class MeasurementsHistory {
  deviceId = 'panel-001';
  from = '';
  to = '';
  selectedVariable: MeasurementVariable = 'power';

  measurements: Measurement[] = [];
  isLoading = false;
  errorMessage = '';
  hasSearched = false;

  readonly variableOptions: VariableOption[] = [
    {
      label: 'Voltaje DC',
      value: 'voltage',
      unit: 'V'
    },
    {
      label: 'Corriente DC',
      value: 'current',
      unit: 'A'
    },
    {
      label: 'Potencia instantánea',
      value: 'power',
      unit: 'W'
    },
    {
      label: 'Irradiancia solar',
      value: 'irradiance',
      unit: 'W/m²',
    },
    {
      label: 'Temperatura ambiente',
      value: 'ambientTemperature',
      unit: '°C',
    },
    {
      label: 'Temperatura del panel',
      value: 'panelTemperature',
      unit: '°C',
    },
    {
      label: 'Humedad relativa',
      value: 'relativeHumidity',
      unit: '%',
    },
  ];

  constructor(
    private readonly measurementService: MeasurementService
  ) { }

  searchMeasurements(): void {
    this.isLoading = true;
    this.errorMessage = '';
    this.hasSearched = true;

    this.measurementService
      .findHistory({
        deviceId: this.deviceId,
        from: this.from || undefined,
        to: this.to || undefined,
        page: 0,
        size: 100
      }).subscribe({
        next: (measurements) => {
          this.measurements = measurements;
          this.isLoading = false;
        },
        error: () => {
          this.errorMessage = "No fue posible consultar las mediciones históricas";
          this.isLoading = false;
        }
      })
  }

  getSelectedVariableLabel(): string {
    const option = this.variableOptions.find(
      (variable) => variable.value === this.selectedVariable,
    );

    return option?.label ?? 'variable';
  }

  getSelectedVariableUnit(): string {
    const option = this.variableOptions.find(
      (variable) => variable.unit === this.selectedVariable
    );

    return option?.unit ?? '';
  }

  getMeasurementValue(measurement: Measurement): number {
    return measurement[this.selectedVariable];
  }

  formatDate(value?: string): string {
    if (!value) {
      return 'N/A';
    }

    return new Intl.DateTimeFormat('es-CO', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(new Date(value));
  }

  isValueOutOfRange(measurement: Measurement): boolean {
    const value = this.getMeasurementValue(measurement);

    if (this.selectedVariable === 'relativeHumidity' && (value < 0 || value > 100)) {
      return true;
    }

    if (['voltage', 'current', 'power', 'irradiance'].includes(this.selectedVariable)) {
      return value < 0;
    }
    return false;
  }

  downloadCsv(): void {
    if (this.measurements.length === 0) {
      this.errorMessage = 'No hay mediciones para exportar.';
      return;
    }

    this.errorMessage = '';

    const headers = [
      'Fecha de medición',
      'Panel',
      'Voltaje (V)',
      'Corriente (A)',
      'Potencia (W)',
      'Irradiancia (W/m²)',
      'Temperatura ambiente (°C)',
      'Temperatura del panel (°C)',
      'Humedad relativa (%)',
      'Calidad',
    ];

    const rows = this.measurements.map((measurement) => [
      measurement.measuredAt ?? measurement.timestamp ?? '',
      measurement.deviceId,
      measurement.voltage,
      measurement.current,
      measurement.power,
      measurement.irradiance,
      measurement.ambientTemperature,
      measurement.panelTemperature,
      measurement.relativeHumidity,
      measurement.quality ?? ''
    ]);

    const csvContent = [
      headers, ...rows,
    ]
      .map((row) => 
        row.map((value) => this.escapeCsvValue(value)).join(','),
      ).join('\n');

    const csvWithBom = '\uFEFF' + csvContent;

    const blob = new Blob(
      [csvWithBom],
      {
        type: 'text/csv;charset=utf-8;',
      },
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');

    link.href = url;
    link.download = this.buildCsvFileName();

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  }

  private escapeCsvValue(value:string | number,): string{
    const text = String(value);
    if(text.includes(',') || text.includes('"') || text.includes('\n')){
      return `${text.replace(/"/g, '""')}`;
    }

    return text;
  }

  private buildCsvFileName(): string {
    const currentDate = new Date().toISOString().slice(0, 10);
    const normalizedDeviceId = this.deviceId.trim().toLowerCase().replace(/[^a-z0-9-_]/g, '-');

    return `historico-${normalizedDeviceId}-${currentDate}.csv`;
  }
}
