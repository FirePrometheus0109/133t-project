import { PageEvent } from '@angular/material';
import { Filter, UpdateParamTypes } from '../models/filters.model';
import { UtilsService } from '../services/utils.service';


export class GridViewHelper {
  public static getParamsWitFilterValue(params: Object, selectedFilters: Filter[], removedFilter?: Filter) {
    const filterParam = {};
    selectedFilters.forEach((item) => {
      if (filterParam.hasOwnProperty(item.data.param)) {
        filterParam[item.data.param].push(item.value.key);
      } else {
        filterParam[item.data.param] = [item.value.key];
      }
    });
    if (removedFilter && params.hasOwnProperty(removedFilter.data.param)) {
      delete params[removedFilter.data.param];
    }
    return {...params, ...filterParam};
  }

  public static getPaginationParams(paginatedData: PageEvent): object {
    const limit = paginatedData.pageSize;
    const offset = paginatedData.pageIndex * paginatedData.pageSize;
    return {
      limit: limit,
      offset: offset,
    };
  }

  public static updateWithSortingParams(params: Object, value: string) {
    return Object.assign(params, {'ordering': value});
  }

  public static updateWithOwnerParams(params: Object, value: string) {
    return Object.assign(params, {owner: value});
  }

  public static updateWithStatusFilterParams(params: Object, value: any) {
    if (UtilsService.isObject(value)) {
      return Object.assign(params, value);
    }
    return Object.assign(params, {'status': value});
  }

  public static updateParams(params: object, additionalParams: object) {
    return Object.assign(params, additionalParams);
  }

  public static updatePageParams(params: object, paginatedData: PageEvent) {
    return Object.assign(params, GridViewHelper.getPaginationParams(paginatedData));
  }

  public static updateParamsWithEmptyFilter(params: object, filter: Filter) {
    const updatedParams = {...params};
    if (UtilsService.isEmptyObject(filter.value) && Object.keys(updatedParams).includes(filter.data.param)) {
      delete updatedParams[filter.data.param];
    }
    return updatedParams;
  }

  public static clearStateParams(params: object, paramsToDelete: string[]) {
    const resultParams = {...params};
    Object.keys(resultParams).forEach((prop) => {
      if (paramsToDelete.includes(prop)) {
        delete resultParams[prop];
      }
    });
    return resultParams;
  }

  public static prepareNewParams(params: any, changeType: string) {
    switch (changeType) {
      case (UpdateParamTypes.PAGINATION):
        return GridViewHelper.updatePageParams({}, params);
      case (UpdateParamTypes.SORTING):
        return GridViewHelper.updateWithSortingParams({}, params);
      case (UpdateParamTypes.COMMON):
        return GridViewHelper.updateParams({}, params);
      case (UpdateParamTypes.STATUS):
        return GridViewHelper.updateWithStatusFilterParams({}, params);
      case (UpdateParamTypes.OWNER):
        return GridViewHelper.updateWithOwnerParams({}, params);
      default:
        return GridViewHelper.updateParams({}, params);
    }
  }
}
