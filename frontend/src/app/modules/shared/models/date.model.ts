import * as moment from 'moment';
import { Deserializable } from './deserializable.model';
import { FormValue } from './formvalue.model';
import { Serializable } from './serializable.model';


export class DateModel implements Serializable, Deserializable, FormValue {
  year: number;
  month: number;
  day: number;

  serialize(): string {
    return moment(new Date(this.year, this.month, this.day)).format();
  }

  deserialize(input: string): DateModel {
    const date = new Date(input);
    this.year = date.getFullYear();
    this.month = date.getMonth();
    this.day = date.getDay();
    return this;
  }

  fromFormValue(formData): DateModel {
    const input = Object.assign({}, formData);
    const result = new DateModel();
    return Object.assign(result, formData);
  }

  toFormValue(): object {
    return Object.assign({}, this);
  }
}
