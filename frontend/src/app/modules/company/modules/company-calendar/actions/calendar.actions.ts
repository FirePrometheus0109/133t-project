import { CalendarView } from 'angular-calendar';
import { CalendarFilterValue, CalendarRelatedErrors, ViewDateSwitchDirection } from '../states/calendar.state';

export enum CalendarActionTypes {
  ChangeView = '[Company Calendar] ChangeView',
  ChangeViewDate = '[Company Calendar] ChangeViewDate',
  ToggleOpenActiveDay = '[Company Calendar] ToggleOpenActiveDay',
  SwitchViewDate = '[Company Calendar] SwitchViewDate',
  LoadCalendarEvents = '[Company Calendar] LoadCalendarEvents',
  SetCalendarError = '[Company Calendar] SetCalendarError',
  ChangeFilterValue = '[Company Calendar] ChangeFilterValue'
}

export class LoadCalendarEvents {
  static readonly type = CalendarActionTypes.LoadCalendarEvents;
}

export class SetCalendarError {
  static readonly type = CalendarActionTypes.SetCalendarError;
  constructor(public relateTo: CalendarRelatedErrors, public error = null) {}
}

export class ChangeView {
  static readonly type = CalendarActionTypes.ChangeView;
  constructor(public view: CalendarView) {}
}

export class SwitchViewDate {
  static readonly type = CalendarActionTypes.SwitchViewDate;
  constructor(public direction: ViewDateSwitchDirection) {}
}

export class ChangeViewDate {
  static readonly type = CalendarActionTypes.ChangeViewDate;
  constructor(public date: Date) {}
}

export class ToggleOpenActiveDay {
  static readonly type = CalendarActionTypes.ToggleOpenActiveDay;
  constructor(public open?: boolean) {}
}

export class ChangeFilterValue {
  static readonly type = CalendarActionTypes.ChangeFilterValue;
  constructor(public filterValue?: CalendarFilterValue) {}
}

export type CompanyCalendarActionsUnion =
  | LoadCalendarEvents
  | ChangeView
  | ChangeViewDate
  | SwitchViewDate;
