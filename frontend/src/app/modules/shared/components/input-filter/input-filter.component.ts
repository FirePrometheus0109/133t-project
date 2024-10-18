import { Component, Input } from '@angular/core';
import { BaseFormComponent } from '../base-form.component';


@Component({
  selector: 'app-input-filter',
  templateUrl: './input-filter.component.html',
  styleUrls: ['./input-filter.component.css']
})
export class InputFilterComponent extends BaseFormComponent {
  @Input() placeholder: string;
  @Input() controlName: string;
  @Input() isNumeric: boolean;
}
