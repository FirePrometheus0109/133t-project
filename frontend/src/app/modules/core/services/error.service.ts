import { HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Store } from '@ngxs/store';
import { ResponseErrorTypes } from '../../shared/enums/response-error-types';


@Injectable({
  providedIn: 'root',
})
export class ErrorService {
  constructor(private store: Store) {
  }

  public handleErrorMessage(httpError: HttpErrorResponse) {
    let errorsMessagesArray = [];
    if (httpError.error.hasOwnProperty(ResponseErrorTypes.ERRORS)) {
      errorsMessagesArray = errorsMessagesArray.concat(httpError.error[ResponseErrorTypes.ERRORS]);
    }
    if (httpError.error.hasOwnProperty(ResponseErrorTypes.FIELD_ERRORS)) {
      errorsMessagesArray = errorsMessagesArray.concat(this.buildFieldErrorMessage(httpError.error[ResponseErrorTypes.FIELD_ERRORS]));
    }
    return errorsMessagesArray.join(`\n`);
  }

  private buildFieldErrorMessage(error) {
    const fieldErrorsArray = [];
    for (const key in error) {
      if (error.hasOwnProperty(key)) {
        fieldErrorsArray.push(`${key}: ${error[key].join()}`);
      }
    }
    return fieldErrorsArray;
  }
}
