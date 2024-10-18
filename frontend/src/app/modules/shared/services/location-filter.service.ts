import { Injectable } from '@angular/core';
import { LocationSearchModel, LocationSearchType } from '../models/address.model';
import { Filter } from '../models/filters.model';
import { SearchLocationPipe } from '../pipes/search-location.pipe';


@Injectable({
  providedIn: 'root'
})
export class LocationFilterService {
  private city_id = 'city_id';
  private state_id = 'state_id';

  constructor() {
  }

  public static autoApplyPrepareLocationData(formData) {
    const locationItem = formData.location;
    const params: any = {
      ...formData
    };
    delete params.location;
    if (locationItem) {
      if (locationItem.hasOwnProperty('state')) {
        return Object.assign(params, {city_id: locationItem.id});
      } else if (locationItem.hasOwnProperty('abbreviation')) {
        return Object.assign(params, {state_id: locationItem.id});
      }
    }
    return params;
  }

  public static buildLocationString(locationItem: any) {
    if (locationItem && locationItem.state) {
      return `${locationItem.name} (${locationItem.state.abbreviation})`;
    } else if (locationItem) {
      return `${locationItem.name}`;
    }
  }

  public static getLocationFilter(locationSearchFilter, selectedLocation: LocationSearchModel) {
    const viewValue = new SearchLocationPipe().transform(selectedLocation);
    const keyValue = LocationFilterService.getLocationFilterKeyValue(selectedLocation);
    return new Filter(locationSearchFilter, {key: keyValue, value: viewValue});
  }

  private static getLocationFilterKeyValue(selectedLocation: LocationSearchModel) {
    if (selectedLocation._type_id === LocationSearchType.STATE) {
      return selectedLocation._state_id;
    } else if (selectedLocation._type_id === LocationSearchType.CITY) {
      return `${selectedLocation.name},${selectedLocation._state_id}`;
    }
    return selectedLocation.name;
  }
}
