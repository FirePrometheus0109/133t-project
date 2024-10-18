export enum EventCreatorActionTypes {
  LoadCalendarEventTypes = '[Event Creator] LoadCalendarEventTypes',
}

export class LoadCalendarEventTypes {
  static readonly type = EventCreatorActionTypes.LoadCalendarEventTypes;
}


export type CompanyCalendarActionsUnion =
  | LoadCalendarEventTypes;
