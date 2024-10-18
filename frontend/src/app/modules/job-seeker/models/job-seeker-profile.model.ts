import { environment } from '../../../../environments/environment';
import { User } from '../../auth/models/user.model';
import { Address, Deserializable, FormValue, Photo, Serializable } from '../../shared/models';
import { CertificationItem, EducationItem } from '../../shared/models/education.model';
import { JobItem } from '../../shared/models/experience.model';
import { SkillItem } from '../../shared/models/skill.model';


export interface RequiredFieldToPublishProfile {
  value: string;
  viewValue: string;
  type: RequiredFieldToPublishProfileType;
  validLength?: number;
}


export enum RequiredFieldToPublishProfileType {
  string,
  array,
  object
}


export interface JSNameAndId {
  first_name: string;
  last_name: string;
  id: number;
}


export class JobSeekerProfile implements Serializable, Deserializable, FormValue {
  id: number;
  user: User;
  photo: Photo;
  phone: string;
  address: Address;
  position_type: string;
  education: string;
  salary_negotiable: boolean;
  salary_min: number;
  salary_max: number;
  clearance: string;
  experience: string;
  benefits: string;
  travel: string;
  job_title: string;
  company: string;
  about: string;
  is_public: boolean;
  is_shared: boolean;
  skills: Array<any>;
  modified_at: Date;

  public get isProfileCanBePublic(): boolean {
    return this.requiredFieldsToPublishProfile.every((field) => {
      return this.validateField(field);
    });
  }

  private requiredFieldsToPublishProfile: RequiredFieldToPublishProfile[] = [
    {
      viewValue: 'First name',
      value: 'user__first_name',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'Last name',
      value: 'user__last_name',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'Email',
      value: 'user__email',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'Country',
      value: 'address__country__name',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'City',
      value: 'address__city',
      type: RequiredFieldToPublishProfileType.object,
    },
    {
      viewValue: 'Zip',
      value: 'address__zip',
      type: RequiredFieldToPublishProfileType.object,
    },
    {
      viewValue: 'Address',
      value: 'address__address',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'Position',
      value: 'position_type',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: 'Education',
      value: 'education',
      type: RequiredFieldToPublishProfileType.string,
    },
    {
      viewValue: `Skills (at least ${environment.jspMinPublishSkillsCount})`,
      value: 'skills',
      type: RequiredFieldToPublishProfileType.array,
      validLength: environment.jspMinPublishSkillsCount,
    },
  ];

  public getPublishHideProfileValidationText(): string {
    const checkMark = '\u2713';
    const validationMarks = [];
    this.requiredFieldsToPublishProfile.forEach((validationField) => {
      let mark = validationField.viewValue;
      if (this.validateField(validationField)) {
        mark += checkMark;
      }
      validationMarks.push(mark);
    });
    return validationMarks.join('\n');
  }

  serialize() {
    const result = Object.assign({}, this);
    Object.assign(result, {
      user: this.user.serialize(),
      photo: this.photo.serialize(),
      address: this.address.serialize(),
    });
    return result;
  }

  deserialize(input: any): any {
    this.id = input.id;
    this.user = new User().deserialize(input.user);
    this.photo = new Photo().deserialize(input.photo);
    this.address = new Address().deserialize(input.address);
    this.position_type = input.position_type;
    this.education = input.education;
    this.salary_negotiable = input.salary_public;
    this.salary_min = input.salary_min;
    this.salary_max = input.salary_max;
    this.clearance = input.clearance;
    this.experience = input.experience;
    this.benefits = input.benefits;
    this.travel = input.travel;
    this.job_title = input.job_title;
    this.company = input.company;
    this.about = input.about;
    this.skills = input.skills;
    this.is_public = input.is_public;
    this.is_shared = input.is_shared;
    return this;
  }

  fromFormValue(formData): JobSeekerProfile {
    const result = new JobSeekerProfile();
    result.user = new User().fromFormValue(formData.mainInfoFormGroup);
    result.photo = new Photo().fromFormValue(formData.photo);
    result.address = new Address().fromFormValue(formData.mainInfoFormGroup.address);
    result.job_title = formData.currentJobFormGroup.job_title;
    result.company = formData.currentJobFormGroup.company;
    result.about = formData.aboutFormGroup.about;
    result.position_type = formData.profileDetailsFormGroup.position_type;
    result.education = formData.profileDetailsFormGroup.education;
    result.clearance = formData.profileDetailsFormGroup.clearance;
    result.benefits = formData.profileDetailsFormGroup.benefits;
    result.experience = formData.profileDetailsFormGroup.experience;
    result.salary_min = formData.profileDetailsFormGroup.salary_min;
    result.salary_max = formData.profileDetailsFormGroup.salary_max;
    result.salary_negotiable = formData.profileDetailsFormGroup.salary_negotiable;
    result.travel = formData.profileDetailsFormGroup.travel;
    result.skills = formData.skillsFormGroup.skills;
    return result;
  }

  toFormValue(): object {
    const result = Object.assign({}, this);
    const compiledResult = Object.assign({}, {
      mainInfoFormGroup: Object.assign(result.user.toFormValue(), {address: result.address}),
      currentJobFormGroup: Object.assign({}, {
        job_title: result.job_title,
        company: result.company,
      }),
      aboutFormGroup: Object.assign({}, {about: result.about}),
      profileDetailsFormGroup: Object.assign({}, {
        position_type: result.position_type,
        education: result.education,
        clearance: result.clearance,
        benefits: result.benefits,
        experience: result.experience,
        salary_min: result.salary_min,
        salary_max: result.salary_max,
        salary_negotiable: result.salary_negotiable,
        travel: result.travel,
      }),
      photo: result.photo.toFormValue(),
    });
    return compiledResult;
  }

  private validateField(validationField: RequiredFieldToPublishProfile) {
    const value = this.getObjectValue(this, validationField.value);
    if (value) {
      switch (validationField.type) {
        case (RequiredFieldToPublishProfileType.string):
          return this.validateString(value);
        case (RequiredFieldToPublishProfileType.array):
          return this.validateArray(value, validationField.validLength);
        case (RequiredFieldToPublishProfileType.object):
          return this.validateObject(value);
      }
    }
    return false;
  }

  private validateString(value: string) {
    return value.length > 0;
  }

  private validateArray(value: any[], validLength) {
    return value.length >= validLength;
  }

  private validateObject(value: object) {
    return value.hasOwnProperty('id');
  }

  /**
   * Return object property value by property name. Support nested object's with access by '__' (double underscore)
   * separator.
   */
  private getObjectValue(obj: object, propertyName: string) {
    const delimiter = '__';
    const delimiterLength = delimiter.length;
    const keys = propertyName.split(delimiter);
    // added obj check for newly created job seekers
    if (obj) {
      if (keys.length > 1 && obj.hasOwnProperty(keys[0])) {
        return this.getObjectValue(obj[keys[0]], propertyName.slice(keys[0].length + delimiterLength));
      } else if (keys.length === 1 && obj.hasOwnProperty(keys[0])) {
        return obj[keys[0]];
      } else {
        try {
          throw new Error(`Invalid value name '${propertyName}' for ${this.constructor.name} model.`);
        } catch (e) {
          console.log(e.name + ': ' + e.message);
        }
      }
    }
  }
}


export class JobSeekerProfileForCompany extends JobSeekerProfile {
  job_title: string;
  company: string;
  about: string;
  is_public: boolean;
  skills: Array<SkillItem>;
  educations: Array<EducationItem>;
  certifications: Array<CertificationItem>;
  job_experience: Array<JobItem>;
}
