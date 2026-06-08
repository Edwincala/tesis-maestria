import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MeasurementCard } from './measurement-card';

describe('MeasurementCard', () => {
  let component: MeasurementCard;
  let fixture: ComponentFixture<MeasurementCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MeasurementCard],
    }).compileComponents();

    fixture = TestBed.createComponent(MeasurementCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
