import { CompanyProfile } from '../../company/models/company-profile.model';
import { JobSeekerProfile } from '../../job-seeker/models';
import { Deserializable, FormValue, Serializable } from './../../shared/models';


export interface Permission {
  id: number;
  name: string;
  codename: string;
}


export interface LoggedUser {
  pk: number;
  username: string;
  company: CompanyProfile;
  job_seeker: JobSeekerProfile;
  is_profile_draft: boolean;
  email: string;
  first_name: string;
  last_name: string;
  permissions: Array<Permission>;
}


export class User implements Serializable, Deserializable, FormValue {
  id: number;
  is_superuser: boolean;
  is_staff: boolean;
  is_active: boolean;
  first_name: string;
  last_name: string;
  email: string;
  user_permissions: Array<number>;

  serialize(): object {
    return Object.assign({}, this);
  }

  deserialize(input: any): any {
    this.id = input.id;
    this.is_superuser = input.is_superuser;
    this.is_staff = input.is_staff;
    this.is_active = input.is_active;
    this.first_name = input.first_name;
    this.last_name = input.last_name;
    this.email = input.email;
    return this;
  }

  fromFormValue(formData): User {
    let result = new User();
    result = Object.assign(result, formData);
    return result;
  }

  toFormValue(): object {
    return Object.assign({}, this);
  }
}
