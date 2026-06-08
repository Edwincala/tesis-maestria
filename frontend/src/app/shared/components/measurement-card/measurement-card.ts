import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-measurement-card',
  imports: [CommonModule],
  templateUrl: './measurement-card.html'
})
export class MeasurementCard {
  @Input({required: true}) title = '';
  @Input({required: true}) value: string | number | undefined = '';
  @Input() unit='';
  @Input() description = '';
  @Input() warning = false;

}
