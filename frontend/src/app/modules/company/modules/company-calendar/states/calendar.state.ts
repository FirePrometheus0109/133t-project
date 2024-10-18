import { Action, Selector, State, StateContext } from '@ngxs/store';
import { CalendarView } from 'angular-calendar';
import * as moment from 'moment-timezone';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { ExtendedCalendarEventModel, ShortCalendarEvent } from '../models/company-event.model';
import { CalendarService } from '../services/calendar.service';

import { CalendarActions } from '../actions';

export enum ViewDateSwitchDirection {
  Today,
  Previous,
  Next
}

export enum DateAsTitleFormat {
  Month = 'MMMM yyyy',
  Day = 'EEEE, MMMM d, yyyy'
}

export enum CalendarRelatedErrors {
  eventsLoadingError = 'eventsLoadingError'
}

export enum EventFilterParamKey {
  day = 'day',
  month = 'month'
}

export enum CalendarFilterValue {
  All = 'Show all events',
  OnlyMy = 'Show only my events'
}

export enum MomentActions {
  add = 'add',
  subtract = 'subtract'
}

export class CalendarStateModel {
  view: CalendarView;
  viewDate: Date;
  viewDateAsTitleFormat: DateAsTitleFormat;
  activeDayIsOpen: boolean;
  timezone: string;
  events: ShortCalendarEvent[];
  filter: CalendarFilterValue;

  /**
   * "angular-calendar" setup values
   */
  settings: {
    locale?: string;
    // day view options
    dayStartHour: number;
    dayEndHour: number;
    eventSnapSize?: number;
    eventWidth?: number;
    hourSegmentHeight?: number;
    // month view options
    excludeDays?: number[];
    weekendDays?: number[];
  };
  errors: {
    [key in keyof typeof CalendarRelatedErrors]: any
  };
}

export const defaultCalendarState: CalendarStateModel = {
  view: CalendarView.Month,
  viewDate: moment().toDate(),
  viewDateAsTitleFormat: DateAsTitleFormat.Month, // Depends on "view" state
  activeDayIsOpen: false,
  timezone: moment.tz.guess(),
  events: [],
  filter: CalendarFilterValue.All,
  settings: {
    locale: navigator ? navigator.language : 'en-US', // TODO: move to constant or remove
    dayStartHour: 0,
    dayEndHour: 23,
    eventWidth: 150,
    hourSegmentHeight: 30
  },
  errors: {
    [CalendarRelatedErrors.eventsLoadingError]: null
  }
};

@State<CalendarStateModel>({
  name: 'companycalendar',
  defaults: defaultCalendarState
})
export class CalendarState {
  @Selector()
  static settings(state: CalendarStateModel) {
    return state.settings;
  }

  @Selector()
  static view(state: CalendarStateModel) {
    return state.view;
  }

  @Selector()
  static viewDate(state: CalendarStateModel) {
    return state.viewDate;
  }

  @Selector()
  static viewDateAsTitleFormat(state: CalendarStateModel) {
    return state.viewDateAsTitleFormat;
  }

  @Selector()
  static activeDayIsOpen(state: CalendarStateModel) {
    return state.activeDayIsOpen;
  }

  @Selector()
  static timezone(state: CalendarStateModel) {
    return state.timezone;
  }

  @Selector()
  static events(state: CalendarStateModel) {
    return state.events;
  }

  @Selector()
  static filter(state: CalendarStateModel) {
    return state.filter;
  }

  constructor(private calendarService: CalendarService) {}

  private getDateAsTitleFormatByView(view: CalendarView): DateAsTitleFormat {
    if (view === CalendarView.Month) {
      return DateAsTitleFormat.Month;
    }
    else if (view === CalendarView.Day) {
      return DateAsTitleFormat.Day;
    }
  }

  @Action(CalendarActions.ChangeFilterValue)
  changeFilterValue(ctx: StateContext<CalendarStateModel>, {filterValue}: CalendarActions.ChangeFilterValue) {
    ctx.patchState({filter: filterValue || defaultCalendarState.filter});
    return ctx.dispatch(new CalendarActions.LoadCalendarEvents());
  }

  @Action(CalendarActions.ChangeView)
  changeView(
    ctx: StateContext<CalendarStateModel>,
    { view }: CalendarActions.ChangeView
  ) {
    ctx.patchState({ view, viewDateAsTitleFormat: this.getDateAsTitleFormatByView(view)});
    ctx.dispatch(new CalendarActions.LoadCalendarEvents());
  }

  private getMomentActionByDirection(direction: ViewDateSwitchDirection): string | null {
    if (direction === ViewDateSwitchDirection.Next) {
      return MomentActions.add;
    } else if (direction === ViewDateSwitchDirection.Previous) {
      return MomentActions.subtract;
    } else {
      return null;
    }
  }

  @Action(CalendarActions.SwitchViewDate)
  switchViewDate(
    ctx: StateContext<CalendarStateModel>,
    { direction }: CalendarActions.SwitchViewDate
  ) {
    const state = ctx.getState();
    const workUnit = CalendarState.view(state);
    const viewDate = CalendarState.viewDate(state);
    const momentAction = this.getMomentActionByDirection(direction);
    const delta = 1;
    if (momentAction) {
      ctx.patchState({viewDate: moment(viewDate)[momentAction](delta, workUnit).toDate()});
    }
    else {
      ctx.patchState({viewDate: moment().toDate()});
    }
    ctx.dispatch(new CalendarActions.ToggleOpenActiveDay(false));
    ctx.dispatch(new CalendarActions.LoadCalendarEvents());
  }

  @Action(CalendarActions.ChangeViewDate)
  changeViewDate(
    ctx: StateContext<CalendarStateModel>,
    { date }: CalendarActions.ChangeViewDate
  ) {
    const state = ctx.getState();
    ctx.patchState({viewDate: date});
    const shouldForceSwitch = !moment(CalendarState.viewDate(state)).isSame(moment(date), 'day');
    ctx.dispatch(new CalendarActions.ToggleOpenActiveDay(shouldForceSwitch || null));
  }

  @Action(CalendarActions.ToggleOpenActiveDay)
  toggleOpenActiveDay(
    ctx: StateContext<CalendarStateModel>,
    { open }: CalendarActions.ToggleOpenActiveDay
  ) {
    const state = ctx.getState();
    const activeDayIsOpen = typeof open === 'boolean' ? open : !CalendarState.activeDayIsOpen(state);
    ctx.patchState({ activeDayIsOpen });
  }

  @Action(CalendarActions.SetCalendarError)
  setCalendarError(ctx: StateContext<CalendarStateModel>, {relateTo, error}: CalendarActions.SetCalendarError) {
    const state = ctx.getState();
    ctx.patchState({
      errors: {
        ...state.errors,
        [relateTo]: error
      }
    });
  }

  private getEventFilterParams(ctx: StateContext<CalendarStateModel>) {
    const state = ctx.getState();
    const viewDate = CalendarState.viewDate(state);
    const view = CalendarState.view(state);
    const filterOwnEvents = CalendarState.filter(state) === CalendarFilterValue.OnlyMy;
    const tz = CalendarState.timezone(state);
    return {
      [view]: moment(viewDate).format('YYYY-MM-DD'),
      tz,
      is_owner: filterOwnEvents
    };
  }

  @Action(CalendarActions.LoadCalendarEvents)
  loadCalendarEvents(
    ctx: StateContext<CalendarStateModel>
  ) {
    const eventFilterParams = this.getEventFilterParams(ctx);
    return this.calendarService.getCalendarEvents(eventFilterParams).pipe(
      tap(result => {
        ctx.patchState({
          events: ExtendedCalendarEventModel.formatMultiple(result)
        });
        ctx.dispatch(new CalendarActions.SetCalendarError(CalendarRelatedErrors.eventsLoadingError, null));
      }),
      catchError(error => {
        ctx.dispatch(new CalendarActions.SetCalendarError(CalendarRelatedErrors.eventsLoadingError, error.error));
        return of(error);
      })
    );
  }
}
