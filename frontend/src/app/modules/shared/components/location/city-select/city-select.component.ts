import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatAutocompleteSelectedEvent } from '@angular/material';
import { CityModel } from '../../../models/address.model';
import { BaseFormComponent } from '../../base-form.component';


@Component({
  selector: 'app-city-select',
  templateUrl: './city-select.component.html',
  styleUrls: ['./city-select.component.css']
})
export class CitySelectComponent extends BaseFormComponent {
  @Input() filteredCities: CityModel[];
  @Output() citySelected = new EventEmitter<number>();
  @Output() searchLocation = new EventEmitter<string>();

  public displayFn(city: CityModel) {
    if (city) {
      return `${city.name}, ${city.state.abbreviation}, ${city.code}`;
    }
  }

  onSearchLocation(value) {
    this.searchLocation.emit(value);
  }

  onSelectionChange(event: MatAutocompleteSelectedEvent) {
    const selectedCityId = event.option.value.id;
    this.citySelected.emit(selectedCityId);
  }
}
