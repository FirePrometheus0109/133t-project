import { Deserializable } from './deserializable.model';
import { FormValue } from './formvalue.model';
import { Serializable } from './serializable.model';


export class Photo implements Serializable, Deserializable, FormValue {
  small: string;
  original: string;
  name: string;

  serialize() {
    return Object.assign({}, this);
  }

  deserialize(input: object): any {
    if (input === null) {
      input = new Object();
    }
    this.small = input['small'];
    this.original = input['original'];
    this.name = input['name'];
    return this;
  }

  fromFormValue(formData): Photo {
    const input = Object.assign({}, formData);
    const result = new Photo();
    return Object.assign(result, formData);
  }

  toFormValue(): object {
    return Object.assign({}, this);
  }
}
