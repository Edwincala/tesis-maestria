import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MeasurementsHistory } from './measurements-history';

describe('MeasurementsHistory', () => {
  let component: MeasurementsHistory;
  let fixture: ComponentFixture<MeasurementsHistory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MeasurementsHistory],
    }).compileComponents();

    fixture = TestBed.createComponent(MeasurementsHistory);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
