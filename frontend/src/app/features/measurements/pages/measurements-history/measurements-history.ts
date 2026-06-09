import { Component } from '@angular/core';
import { Measurement, MeasurementVariable } from '../../../../core/models/measurement.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MeasurementService } from '../../../../core/services/measurement';
import { MeasurementLineChart } from '../../../../shared/components/measurement-line-chart/measurement-line-chart';

interface VariableOption{
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
  ){}

  searchMeasurements(): void{
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

  getSelectedVariableLabel(): string{
    const option = this.variableOptions.find(
      (variable) => variable.value === this.selectedVariable,
    );

    return  option?.label ?? 'variable';
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
    if(!value) {
      return 'N/A';
    }

    return new Intl.DateTimeFormat('es-CO', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(new Date(value));
  }

  isValueOutOfRange(measurement: Measurement): boolean{
    const value = this.getMeasurementValue(measurement);

    if(this.selectedVariable === 'relativeHumidity' && (value < 0 || value > 100)){
      return true;
    }

    if(['voltage', 'current', 'power', 'irradiance'].includes(this.selectedVariable)){
      return value < 0;
    }
    return false;
  }
}
