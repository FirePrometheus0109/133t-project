import { CandidateStatus } from '../../candidate/models/candidate-item.model';


export class SortingFilter {
  value: string;
  viewValue: string;

  constructor(value: string, viewValue: string) {
    this.value = value;
    this.viewValue = viewValue;
  }
}


export enum FilterMode {
  SINGLE,
  MULTIPLE,
  SEARCH
}


export class Filter {
  data: FilterData;
  value: FilterResult;

  constructor(data: FilterData, value?: FilterResult) {
    this.data = data;
    this.value = value;
  }
}


export class FilterResult {
  key: any;
  value: string | string[];

  constructor(item: CandidateStatus) {
    if (item) {
      this.key = item.id.toString();
      this.value = item.name;
    }
  }
}


export class FilterData {
  title: string;
  param: string;
  filterEnum: object | Array<any>;
  filterMode: FilterMode;

  constructor(title: string, param: string, filterEnum?: object, isMultiple?: FilterMode) {
    this.title = title;
    this.param = param;
    this.filterEnum = filterEnum;
    this.filterMode = isMultiple ? isMultiple : FilterMode.SINGLE;
  }
}


export enum UpdateParamTypes {
  PAGINATION = 'pagination',
  SORTING = 'sorting',
  COMMON = 'common',
  STATUS = 'status',
  OWNER = 'owner'
}

export enum JobSortingTypes {
  DATE = '-publish_date',
  TITLE = 'title',
  AUTHOR = 'owner__user__first_name',
  STATUS = 'status'
}
