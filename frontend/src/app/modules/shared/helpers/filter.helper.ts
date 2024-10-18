import { Store } from '@ngxs/store';
import { CoreActions } from '../../core/actions';
import { Filter, FilterMode } from '../models/filters.model';
import { SnackBarMessageType } from '../models/snack-bar-message';


export class FilterHelper {

  public static getUpdatedFilterValue(oldFilters, newFilter: Filter) {
    const newFilterIndex = oldFilters.findIndex(element =>
      element.data.param === newFilter.data.param);
    if (newFilterIndex === -1 || newFilter.data.filterMode !== FilterMode.SINGLE) {
      oldFilters.push(newFilter);
    } else {
      newFilter.value.key ? oldFilters.splice(newFilterIndex, 1, newFilter) :
        oldFilters.splice(newFilterIndex, 1);
    }
    return oldFilters;
  }

  public static removeFilter(oldFilters, removedFilter) {
    return oldFilters.filter((item) => item.value.key !== removedFilter.value.key);
  }

  public static isFilterAlreadyAdded(filter: Filter, selectedFilters: Filter[], store: Store, preventNotification?: boolean) {
    const isAdded = selectedFilters.some(item => item.data === filter.data &&
      item.value.key === filter.value.key);
    if (isAdded && !preventNotification) {
      store.dispatch(new CoreActions.SnackbarOpen({
        message: 'Filter is already added',
        type: SnackBarMessageType.ERROR,
      }));
    }
    return isAdded;
  }
}
