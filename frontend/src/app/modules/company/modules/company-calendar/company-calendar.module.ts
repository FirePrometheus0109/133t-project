import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule, } from '@angular/forms';
import { NgxsFormPluginModule } from '@ngxs/form-plugin';
import { NgxsModule } from '@ngxs/store';
import { CalendarModule } from 'angular-calendar';
import { MatSelectInfiniteScrollModule } from 'ng-mat-select-infinite-scroll';
import { NgxMatSelectSearchModule } from 'ngx-mat-select-search';

import { MaterialModule } from '../../../material';

import { CompanyCalendarRoutingModule } from './company-calendar-routing.module';

import { CalendarComponent } from './containers/calendar/calendar.component';
import { CompanyCalendarPageResolver } from './resolvers/calendar.resolver';
import { CalendarService } from './services/calendar.service';
import { CalendarState } from './states/calendar.state';

import { CalendarDateChangerComponent } from './components/calendar-date-changer.component';
import { CalendarEventFilterSelectComponent } from './components/calendar-event-filter-select.component';
import { CalendarViewSwitchComponent } from './components/calendar-view-switch.component';

import { AttendeesListComponent } from './components/attendees-list.component';
import { CoolDateTimePickerComponent } from './components/cool-date-time-picker.component';
import { SelectorWithSearchComponent } from './components/event-form-selector-with-search.component';
import { SelectorWithServerSearchComponent } from './components/event-form-selector-with-server-search.component';
import { EventFormDialogComponent } from './containers/event-form-dialog/event-form-dialog.component';
import { EventFormService } from './services/event-form.service';
import { EventFormState } from './states/event-form-dialog.state';

import { EventCreatorComponent } from './containers/event-creator/event-creator.component';
import { EventCreatorService } from './services/event-creator.service';
import { EventCreatorState } from './states/event-creator.state';

@NgModule({
  imports: [
    FormsModule,
    ReactiveFormsModule,
    CompanyCalendarRoutingModule,
    CommonModule,
    NgxsModule.forFeature([
      CalendarState,
      EventFormState,
      EventCreatorState
    ]),
    NgxsFormPluginModule,
    MaterialModule,
    CalendarModule,
    FlexLayoutModule,
    NgxMatSelectSearchModule,
    MatSelectInfiniteScrollModule
  ],
  providers: [
    CalendarService,
    EventFormService,
    EventCreatorService,
    CompanyCalendarPageResolver
  ],
  declarations: [
    CalendarComponent,
    CalendarEventFilterSelectComponent,
    CalendarDateChangerComponent,
    CalendarViewSwitchComponent,
    EventFormDialogComponent,
    SelectorWithSearchComponent,
    SelectorWithServerSearchComponent,
    CoolDateTimePickerComponent,
    AttendeesListComponent,
    EventCreatorComponent
  ],
  exports: [
    CalendarComponent,
    CalendarEventFilterSelectComponent,
    CalendarDateChangerComponent,
    CalendarViewSwitchComponent,
    EventFormDialogComponent,
    SelectorWithSearchComponent,
    SelectorWithServerSearchComponent,
    CoolDateTimePickerComponent,
    AttendeesListComponent,
    EventCreatorComponent
  ],
  entryComponents: [EventFormDialogComponent],
})
export class CompanyCalendarModule {}
