import { Pipe, PipeTransform } from '@angular/core';
import { LocationSearchModel, LocationType } from '../models';

@Pipe({
  name: 'searchLocation'
})
export class SearchLocationPipe implements PipeTransform {
  transform(value: LocationSearchModel): any {
    if (value._type === LocationType.CITY) {
      return `${value.name}${value._state_id ? `, ${value._state_id}` : ''}`;
    } else if (value._type === LocationType.STATE) {
      return `${value.name} State`;
    }
    return `${value.name}`;
  }
}
