import { Component, EventEmitter, Input, Output } from '@angular/core';
import { InputLengths } from '../../../constants/validators/input-length';
import { ZipModel } from '../../../models/address.model';
import { BaseFormComponent } from '../../base-form.component';


@Component({
  selector: 'app-zip-select',
  templateUrl: './zip-select.component.html',
  styleUrls: ['./zip-select.component.css']
})
export class ZipSelectComponent extends BaseFormComponent {
  @Input() availableZips: ZipModel[];
  @Input() isDisabled = false;
  @Output() searchZip = new EventEmitter<string>();

  public displayFn(zip: ZipModel) {
    if (zip) {
      return zip.code;
    }
  }

  onSearchZip(value: string) {
    this.searchZip.emit(value);
  }
}
