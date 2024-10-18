import { Component, TemplateRef, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import {
  CalendarView,
  collapseAnimation
} from 'angular-calendar';
import { Observable } from 'rxjs';

import { CalendarActions } from '../../actions';
import { ExtendedCalendarEvent } from '../../models/company-event.model';
import {
  CalendarFilterValue,
  CalendarState,
  DateAsTitleFormat,
  ViewDateSwitchDirection
} from '../../states/calendar.state';

import { EventFormDialogComponent } from '../event-form-dialog/event-form-dialog.component';

import { EventAttendeeStatus } from '../../states/event-form-dialog.state';

import { defaultDialogConfig } from '../../containers/event-creator/event-creator.component';

const anonimusName = 'anonimus';


@Component({
  selector: 'cc-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.scss'],
  animations: [collapseAnimation]
})
export class CalendarComponent {
  public readonly attendeeStatuses = EventAttendeeStatus;
  public readonly CalendarView = CalendarView;
  public readonly ViewDateSwitchDirection = ViewDateSwitchDirection;

  @ViewChild('monthOpenDayTemplate') monthOpenDayTemplate: TemplateRef<any>;
  @ViewChild('eventTitleTemplate') eventTitleTemplate: TemplateRef<any>;
  @ViewChild('dayViewEventTitleTemplate') dayViewEventTitleTemplate: TemplateRef<any>;

  @Select(CalendarState.settings) settings$: Observable<object>;
  @Select(CalendarState.view) view$: Observable<CalendarView>;
  @Select(CalendarState.viewDate) viewDate$: Observable<Date>;
  @Select(CalendarState.viewDateAsTitleFormat) viewDateAsTitleFormat$: Observable<DateAsTitleFormat>;
  @Select(CalendarState.activeDayIsOpen) activeDayIsOpen$: Observable<boolean>;
  @Select(CalendarState.events) events$: Observable<ExtendedCalendarEvent[]>;
  @Select(CalendarState.filter) filter$: Observable<CalendarFilterValue>;

  constructor(private store: Store, public dialog: MatDialog) {}

  changeCalendarView(view: CalendarView) {
    this.store.dispatch(new CalendarActions.ChangeView(view));
  }

  switchViewDate(direction: ViewDateSwitchDirection) {
    this.store.dispatch(new CalendarActions.SwitchViewDate(direction));
  }

  onDayClicked({ date, events }: { date: Date; events: ExtendedCalendarEvent[] }) {
    if (events.length) {
      this.store.dispatch(new CalendarActions.ChangeViewDate(date));
    }
  }

  onFilterChanged(filterValue: CalendarFilterValue) {
    this.store.dispatch(new CalendarActions.ChangeFilterValue(filterValue));
  }

  handleEventClick(event: ExtendedCalendarEvent) {
    const dialogRef = this.openFormDialog(event);
    dialogRef.afterClosed().subscribe(eventsWasUpdated => {
      if (eventsWasUpdated) {
        this.store.dispatch(new CalendarActions.LoadCalendarEvents());
      }
    });
  }

  onCreateEvent() {
    this.store.dispatch(new CalendarActions.LoadCalendarEvents());
  }

  openFormDialog(forEvent = {}) {
    return this.dialog.open(EventFormDialogComponent, {
      ...defaultDialogConfig,
      data: {forEvent},
    });
  }

  getShortName(fullname: string) {
    if (fullname) {
      return fullname.split(' ')[0];
    }
    return anonimusName;
  }
}
