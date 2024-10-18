import { Injectable } from '@angular/core';
import { Params } from '@angular/router';
import { Address } from '../models/address.model';
import { RenamePropertyModel } from '../models/rename-property.model';

function _window(): any {
  // return the global native browser window object
  return window;
}


@Injectable({
  providedIn: 'root',
})
export class UtilsService {

  /* tslint:disable */
  public static generateUniqueId() {
    return Math.floor((1 + Math.random()) * 0x10000) + Math.random().toString(36).substring(2, 16);
  }

  /* tslint:enable */

  static get nativeWindow(): any {
    return _window();
  }

  public static getQueryParamsString(queryParams: Params): string {
    return '?' + new URLSearchParams(queryParams).toString();
  }

  public static isString(obj): boolean {
    return (Object.prototype.toString.call(obj) === '[object String]');
  }

  public static isObject(obj): boolean {
    return typeof obj === 'object' && obj !== null;
  }

  public static isEmptyString(string) {
    return UtilsService.isString(string) && string.length === 0;
  }

  public static isEmptyObject(object: object) {
    return (object && (Object.keys(object).length === 0));
  }

  public static isArray(object) {
    return object instanceof Array;
  }

  public static prepareAddressData(addressFormData: Address) {
    return {
      country: addressFormData.country && addressFormData.country.id ? addressFormData.country.id : null,
      address: addressFormData.address ? addressFormData.address : null,
      city: addressFormData.city && addressFormData.city.id ? addressFormData.city.id : null,
      zip: addressFormData.zip && addressFormData.zip.id ? addressFormData.zip.id : addressFormData.zip ? addressFormData.zip : null,
    };
  }

  public static renameProp(valuesToChange: RenamePropertyModel[], obj) {
    let result = {...obj};
    valuesToChange.forEach(item => {
      const {
        [item.oldProp]: oldPropValue,
        ...restObj
      } = result;

      result = {
        ...restObj,
        [item.newProp]: oldPropValue
      };
    });
    return result;
  }

  public static prepareSalaryData(detailsFormData: any) {
    const {
      salary_negotiable,
      salary_max,
      salary_min,
      ...adjustedFormData
    } = detailsFormData;

    return {
      ...adjustedFormData,
      salary_max: salary_max || null,
      salary_min: salary_min || null,
      salary_public: salary_negotiable,
    };
  }
}
