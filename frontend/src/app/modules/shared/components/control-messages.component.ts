import { Component, Input } from '@angular/core';
import { AbstractControl, FormControl, FormGroup } from '@angular/forms';
import { ValidationService } from '../services/validation.service';

const SERVER_ERROR_STR = 'server_error';


@Component({
  selector: 'app-control-messages',
  template: `
    <mat-error *ngIf="errorMessage !== null">{{errorMessage}}</mat-error>
  `,
  styles: [],
})
export class ControlMessagesComponent {
  @Input() public form: FormGroup;
  @Input() public control: FormControl;
  @Input() public submitted: boolean;

  // errors <--
  private _errors: any = null;
  @Input()
  set errors(errors: any) {
    if (errors && errors.field_errors) {
      this.handleInputErrors(errors.field_errors);
    }
    this._errors = errors;
  }

  get errors(): any {
    return this._errors;
  }

  // errors -->

  get errorMessage() {
    if (this.control) {
      for (const propertyName in this.control.errors) {
        if (this.control.touched && this.control.errors.hasOwnProperty(propertyName)) {
          return ValidationService.getValidatorErrorMessage(propertyName, this.control.errors[propertyName]);
        }
      }
    }
    return null;
  }

  recursiveHandleInputErrors(rootErrors, rootFG: FormGroup) {
    const fields = Object.keys(rootErrors || {});
    fields.forEach((field) => {
      const control = this.findFieldControl(rootFG, field);
      if (control instanceof FormGroup && control !== rootFG) {
        this.recursiveHandleInputErrors(rootErrors[field], control);
      } else {
        const errors = this.fetchFieldErrors(rootErrors, field);
        control.setErrors(errors);
        control.markAsTouched();
      }
    });
  }

  handleInputErrors(errors: any) {
    this.recursiveHandleInputErrors(errors, this.form);
  }

  protected findFieldControl(parent: FormGroup, field: string): AbstractControl {
    let control: AbstractControl;
    if (parent.contains(field)) {
      control = parent.get(field);
    } else {
      // Field is not defined in form but there is a validation error for it, set it globally
      control = parent;
    }
    return control;
  }

  private fetchFieldErrors(data: any, field: string): any {
    const errors = {};
    let arrayErr = [];
    if (Array.isArray(data[field])) {
      arrayErr = data[field];
    } else {
      for (const key of Object.keys(data[field])) {
        let subArrayErr;
        if (Array.isArray(data[field][key])) {
          subArrayErr = data[field][key];
        } else {
          subArrayErr = this.fetchFieldErrors(data[field], key);
        }
        subArrayErr.forEach(e => arrayErr.push(e));
      }
    }
    arrayErr.forEach((e, index) => {
      const name = `${SERVER_ERROR_STR}_${index + 1}`;
      errors[name] = e;
    });
    return errors;
  }
}
