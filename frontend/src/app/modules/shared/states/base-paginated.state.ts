export class BasePaginatedPageStateModel {
  status: string;
  errors: object;
  count: number;
  next: string;
  previous: string;
  results: Array<any>;
  pageSize: number;
  pageIndex: number;
  pageSizeOptions: Array<number>;
  limit: number;
  offset: number;
}

export const pageSizeSmall = 5;
export const pageSizeMinMedium = 10;
export const pageSizeMaxMedium = 25;
export const pageSizeLarge = 100;

export const DEFAULT_PAGINATED_STATE = {
  status: 'ready',
  errors: null,
  count: 0,
  next: null,
  previous: null,
  results: null,
  pageSize: 10,
  pageIndex: 0,
  pageSizeOptions: [pageSizeSmall, pageSizeMinMedium, pageSizeMaxMedium, pageSizeLarge],
  limit: 10,
  offset: 0,
};
