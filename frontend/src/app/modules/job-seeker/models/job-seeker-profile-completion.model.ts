export interface JobSeekerProfileCompletionModel {
  total_complete: number;
  need_complete: TooltipCompletionItemModel[];
}


export interface TooltipCompletionItemModel {
  add_percents: number;
  field: string;
}
