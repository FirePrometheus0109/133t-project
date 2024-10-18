import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';
import * as moment from 'moment';
import { UtilsService } from './utils.service';

export const SERVER_ERROR_STR = 'server_error';


@Injectable({
  providedIn: 'root',
})
export class ValidationService {
  static getValidatorErrorMessage(validatorName: string, validatorValue?: any) {
    const config = {
      'required': 'Required',
      'invalidEmailAddress': 'Invalid email address',
      'invalidPassword': `
              Invalid password. Password must be at least 8 characters long,
              must contain at least one uppercase, one lowercase, and one number
            `,
      'minlength': `Minimum length ${validatorValue.requiredLength}`,
      'maxlength': `Maximal length ${validatorValue.requiredLength}`,
      'doesMatchPassword': 'Password does not match',
      'onlyNumericAvailable': 'Only numeric value available',
      'dates': 'To publish job posting select closing date later than publishing date',
      'publish_future': 'You can\'t post the job with past date. To schedule the job select date in the future.',
      'closing_future': 'You can\'t publish the job posting with past closing date. ' +
      'To publish the job posting select closing date in the future.',
      'incorrectSalaryMin': 'Salary min more than Salary max',
      'valueNotSelected': 'Select value from list',
    };
    if (validatorName.includes(`${SERVER_ERROR_STR}_`)) {
      return validatorValue;
    }
    return config[validatorName];
  }

  // TODO: For email validation need use regexp received from backend
  static emailValidator(control) {
    // RFC 2822 compliant regex
    /* tslint:disable */
    if (control.value && control.value.match(
        /[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?/)) {
      /* tslint:enable */
      return null;
    } else if (UtilsService.isEmptyString(control.value)) {
      return null;
    } else {
      return {'invalidEmailAddress': true};
    }
  }

  static passwordValidator(control) {
    // TODO: get it from state
    const passwordPattern = JSON.parse(localStorage.getItem('core.settings.validators')).password_validator;
    if (control.value && control.value.match(passwordPattern)) {
      return null;
    } else {
      return {'invalidPassword': true};
    }
  }

  static passwordMatchValidator(group: FormGroup) {
    let password;
    let repeatPassword;
    if (group.controls.password1 && group.controls.password2) {
      password = group.controls.password1.value;
      repeatPassword = group.controls.password2.value;
    } else if (group.controls.new_password && group.controls.new_password_confirm) {
      password = group.controls.new_password.value;
      repeatPassword = group.controls.new_password_confirm.value;
    }
    if (!password || !repeatPassword) {
      return null;
    }
    if (repeatPassword.length <= 0) {
      return null;
    }
    if (repeatPassword !== password) {
      return {
        doesMatchPassword: true,
      };
    }
    return null;
  }

  static numericValidator(control) {
    /* tslint:disable */
    if (control.value && control.value.toString().match(
        /[^0-9]/g)) {
      /* tslint:enable */
      return {'onlyNumericAvailable': true};
    } else {
      return null;
    }
  }

  static educationValidator(group: FormGroup) {
    if (group.controls.education_strict.value) {
      if (!group.controls.education.value) {
        group.controls.education.markAsTouched();
        group.controls.education.setErrors({required: true});
        return null;
      } else {
        group.controls.education.setErrors(null);
        return null;
      }
    } else {
      group.controls.education.setErrors(null);
      return null;
    }
  }

  static jobDateValidator(group: FormGroup) {
    const publish_date = moment(group.controls.publish_date.value);
    const closing_date = moment(group.controls.closing_date.value);

    if (closing_date < publish_date) {
      group.controls.closing_date.setErrors(
        {dates: true}
      );
      return null;
    }

    if (publish_date.isBefore(moment().add(-1, 'd'), 'day')) {
      group.controls.publish_date.setErrors(
        {publish_future: true}
      );
      return null;
    }

    if (closing_date.isBefore(moment(), 'day')) {
      group.controls.closing_date.setErrors(
        {closing_future: true}
      );
      return null;
    }
    group.controls.publish_date.setErrors(null);
    group.controls.closing_date.setErrors(null);
  }

  static salaryValidator(group: FormGroup) {
    const salaryMin = group.controls.salary_min;
    const salaryMax = group.controls.salary_max;
    if (salaryMin.value && salaryMax.value && salaryMin.value > salaryMax.value) {
      salaryMin.markAsTouched();
      salaryMin.setErrors({incorrectSalaryMin: true});
      return {incorrectSalaryMin: true};
    } else {
      salaryMin.setErrors(null);
      return null;
    }
  }

  static isCurrentAndDateToValidator(group: FormGroup) {
    if (group.controls.is_current.value) {
      group.controls.date_to.setErrors(null);
      return null;
    } else {
      if (!group.controls.date_to.value) {
        group.controls.date_to.setErrors({required: true});
        return null;
      }
      return null;
    }
  }

  static addressValidator(group: FormGroup) {
    if (group.controls.city.value && !group.controls.city.value.hasOwnProperty('id')) {
      group.controls.city.setErrors({valueNotSelected: true});
      return null;
    }
    if (group.controls.zip.value && !group.controls.zip.value.hasOwnProperty('id') &&
      !group.controls.zip.value.hasOwnProperty('code')) {
      group.controls.zip.setErrors({valueNotSelected: true});
      return null;
    }
    return null;
  }

  static selectListObjectValidator(control) {
    if (control.value && !control.value.hasOwnProperty('id')) {
      return {valueNotSelected: true};
    }
    return null;
  }
}
