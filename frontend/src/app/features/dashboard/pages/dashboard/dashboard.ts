import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Measurement } from '../../../../core/models/measurement.model';
import { MeasurementService } from '../../../../core/services/measurement';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.html'
})
export class DashboardComponent implements OnInit{
  deviceId = 'panel-001';
  latestMeasurement?: Measurement;
  isLoading = false;
  errorMessage = '';

  constructor(
    private readonly measurementService: MeasurementService,
  ){}

  ngOnInit(): void {
    this.loadLatestMeasurement();
  }

  loadLatestMeasurement(): void{
    this.isLoading = true;
    this.errorMessage = '';

    this.measurementService
      .findLatest(this.deviceId)
      .subscribe({
        next: (measurement) => {
          this.latestMeasurement = measurement;
          this.isLoading = false;
        },
        error: () => {
          this.errorMessage = 'No fue posible cargar la última medición.';
          this.isLoading = false;
        },
      });
  }

  isHumidityOutOfRange(): boolean{
    if(!this.latestMeasurement){
      return false;
    }

    return (
      this.latestMeasurement.relativeHumidity < 0 ||
      this.latestMeasurement.relativeHumidity > 100
    );
  }

  isNegative(value: number): boolean {
    return value < 0;
  }
}
