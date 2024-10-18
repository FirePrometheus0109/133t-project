import { Address, Deserializable, FormValue, Photo, Serializable } from '../../shared/models';
import { SubscriptionModel } from '../../subscription/models/subsctiption-plan.model';


export class CompanyProfile implements Serializable, Deserializable, FormValue {
  id: number;
  name: string;
  photo: Photo;
  description: string;
  phone: string;
  fax: string;
  website: string;
  email: string;
  address: Address;
  is_trial_available: boolean;
  is_billing_info_provided: boolean;
  subscription: SubscriptionModel;
  jobs: Array<any>;

  serialize() {
    const result = Object.assign({}, this);
    Object.assign(result, {
      photo: this.photo.serialize(),
    });
    return result;
  }

  deserialize(input: any): any {
    Object.assign(this, input);
    this.address = new Address().deserialize(input.address);
    this.photo = new Photo().deserialize(input.photo);
    return this;
  }

  fromFormValue(formData): CompanyProfile {
    let result = new CompanyProfile();
    result = Object.assign(result, formData);
    result.photo = new Photo().fromFormValue(formData.photo);
    return result;
  }

  toFormValue(): object {
    const result = Object.assign({}, this);
    return Object.assign(result, {
      photo: result.photo.toFormValue(),
    });
  }
}
