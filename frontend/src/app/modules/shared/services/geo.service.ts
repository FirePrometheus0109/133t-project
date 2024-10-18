import { Injectable } from '@angular/core';
import { ApiService } from './api.service';


@Injectable({
  providedIn: 'root',
})
export class GeoService {
  route = 'geo';
  country = 'country';
  state = 'state';
  city = 'city';
  zip = 'zip';
  locations = 'locations';

  constructor(private api: ApiService) {
  }

  public getCountries(params?) {
    return this.api.get(`${this.route}/${this.country}`, params);
  }

  public getStates(params?) {
    return this.api.get(`${this.route}/${this.state}`, params);
  }

  public getCities(params?) {
    return this.api.get(`${this.route}/${this.city}`, params);
  }

  public getZips(cityId: number, params?) {
    return this.api.get(`${this.route}/${this.city}/${cityId}/${this.zip}`, params);
  }

  public searchForCity(searchStr) {
    return this.api.get(`${this.route}/${this.city}`, {search: searchStr});
  }

  public filterLocation(searchStr) {
    return this.api.get(`${this.route}/${this.locations}`, {search: searchStr});
  }
}
