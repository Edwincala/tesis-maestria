import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { Measurement, MeasurementVariable } from '../../../core/models/measurement.model';
import { ChartConfiguration, ChartOptions } from 'chart.js';

@Component({
  selector: 'app-measurement-line-chart',
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './measurement-line-chart.html'
})
export class MeasurementLineChart implements OnChanges {
  @Input({required: true}) measurements: Measurement[] = [];
  @Input({required: true}) variable: MeasurementVariable = 'power';
  @Input({required: true}) label = 'Variable';
  @Input() unit = '';

  chartData: ChartConfiguration<'line'>['data'] = {
    labels: [],
    datasets:[
      {
        data: [],
        label: '',
        tension: 0.35,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: false
      },
    ],
  };

  chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
      },
      tooltip: {
        enabled: true,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Tiempo'
        },
      },
      y: {
        title: {
          display: true,
          text: '',
        },
      },
    },
  };

  ngOnChanges(changes: SimpleChanges): void {
    this.updateChart();
  }

  private updateChart(): void{
    const labels = this.measurements.map((measurement) => 
      this.formatTime(
        measurement.measuredAt || measurement.timestamp,
      ),
    );

    const values = this.measurements.map((measurement) => 
      Number(measurement[this.variable]),
    );

    this.chartData = {
      labels,
      datasets: [
        {
          data: values,
          label: this.unit
            ? `${this.label} (${this.unit})`
            : this.label,
          tension: 0.35,
          pointRadius: 4,
          pointHoverRadius: 6,
          fill: false,
        },
      ],
    };

    this.chartOptions = {
      ...this.chartOptions,
      scales: {
        ...this.chartOptions.scales,
        y: {
          title: {
            display: true,
            text: this.unit || this.label
          },
        },
      },
    };
  }

  private formatTime(value?: string): string {
    if(!value){
      return 'N/A';
    }

    return new Intl.DateTimeFormat('es-CO', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(value));
  }
}
