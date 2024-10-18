import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';

import { EventFormDialogComponent } from '../event-form-dialog/event-form-dialog.component';

import { EventCreatorActions } from '../../actions';
import { EventCreatorState } from '../../states/event-creator.state';

export const defaultDialogConfig: Partial<MatDialogConfig> = {
  width: EventFormDialogComponent.defaultWidth,
  closeOnNavigation: true, // only if its not a target="_blank" etc.
};

@Component({
  selector: 'cc-event-creator',
  templateUrl: './event-creator.component.html',
  styleUrls: ['./event-creator.component.scss']
})
export class EventCreatorComponent implements OnInit {

  @Input() withLabel = true;
  @Output() eventCreated = new EventEmitter<void>();

  @Select(EventCreatorState.eventTypesState) eventTypesState$: Observable<any>;

  constructor(public dialog: MatDialog, private store: Store) { }

  ngOnInit() {
    this.store.dispatch(new EventCreatorActions.LoadCalendarEventTypes());
  }

  handleTypeSelect(eventTypeObj) {
    const dialogRef = this.openFormDialog({type: eventTypeObj});
    dialogRef.afterClosed().subscribe(eventsWasUpdated => {
      if (eventsWasUpdated) {
        this.eventCreated.emit();
      }
    });
  }

  openFormDialog(forEvent = {}) {
    return this.dialog.open(EventFormDialogComponent, {
      ...defaultDialogConfig,
      data: {forEvent}
    });
  }

}
