import { Deserializable } from './deserializable.model';
import { FormValue } from './formvalue.model';
import { Serializable } from './serializable.model';


export class Address implements Serializable, Deserializable, FormValue {
  id: number;
  address: string;
  country: CountryModel;
  city: CityModel;
  zip: ZipModel;

  serialize() {
    return Object.assign({}, this);
  }

  deserialize(input: any): any {
    if (input === null) {
      input = new Object();
    }
    this.id = input.id;
    this.address = input.address;
    this.country = input.country;
    this.city = input.city;
    this.zip = input.zip;
    return this;
  }

  fromFormValue(formData): Address {
    const input = Object.assign({}, formData);
    const result = new Address();
    return Object.assign(result, formData);
  }

  toFormValue(): object {
    return Object.assign({}, this);
  }
}


export interface AddressFull {
  id: number;
  address: string;
  country: CountryModel;
  state: StateModel;
  city: CityModel;
  zip: string;
}


export interface CountryModel {
  id: number;
  name: string;
}


export interface StateModel {
  id: number;
  name: string;
  abbreviation: string;
}


export interface CityModel {
  id: number;
  name: string;
  state: StateModel;
}


export interface ZipModel {
  id: number;
  code: string;
}


export enum LocationSearchType {
  COUNTY,
  ZIP_CODE,
  CITY,
  STATE
}


export interface LocationSearchModel {
  name: string;
  _state_id: string;
  _type: string ;
  _type_id: LocationSearchType;
}

export enum LocationType {
  STATE = 'State',
  CITY = 'City'
}
