import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatAutocompleteSelectedEvent } from '@angular/material';
import { LocationFilterService } from '../../../services/location-filter.service';
import { BaseFormComponent } from '../../base-form.component';


@Component({
  selector: 'app-location-select-filter',
  templateUrl: './location-select-filter.component.html',
  styleUrls: ['./location-select-filter.component.css']
})
export class LocationSelectFilterComponent extends BaseFormComponent {
  @Input() filteredLocationItems: any[];
  @Output() locationSelected = new EventEmitter<any>();

  public displayFn(locationItem: any) {
    return LocationFilterService.buildLocationString(locationItem);
  }

  public onSelectionChange(event: MatAutocompleteSelectedEvent) {
    const selectedCityId = event.source['value'];
    this.locationSelected.emit(selectedCityId);
  }
}
