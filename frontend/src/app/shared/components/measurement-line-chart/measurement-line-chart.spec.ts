import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MeasurementLineChart } from './measurement-line-chart';

describe('MeasurementLineChart', () => {
  let component: MeasurementLineChart;
  let fixture: ComponentFixture<MeasurementLineChart>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MeasurementLineChart],
    }).compileComponents();

    fixture = TestBed.createComponent(MeasurementLineChart);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
