export interface PaginatedData {
  count: number;
  next: string;
  previous: string;
  results: any[];
}

export interface CommentsPaginatedData extends PaginatedData {
  new_comments: number;
}


export const DEFAULT_PAGINATED_OPTIONS = {limit: 10, offset: 0};
