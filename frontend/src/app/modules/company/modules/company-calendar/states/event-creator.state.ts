import { Action, Selector, State, StateContext } from '@ngxs/store';
import { catchError, tap } from 'rxjs/operators';

import { FetchBasedState } from './fetch-based.state';

import { EventCreatorActions } from '../actions';
import { EventCreatorService } from '../services/event-creator.service';

const eventStatusesStateKey = 'eventStatuses';

export class EventCreatorStateModel {
  [eventStatusesStateKey]: {
    pending: boolean,
    data: any[],
    errors: any
  };
}

export const defaultEventCreatorState = {
  [eventStatusesStateKey]: {
    pending: false,
    data: undefined,
    errors: {}
  },
};

@State<EventCreatorStateModel>({
  name: 'eventcreator',
  defaults: defaultEventCreatorState
})
export class EventCreatorState extends FetchBasedState {
  defaultState = defaultEventCreatorState;

  constructor(private eventCreatorService: EventCreatorService) {
    super();
  }

  @Selector()
  static eventTypesState(state: EventCreatorStateModel) {
    return state[eventStatusesStateKey];
  }

  @Action(EventCreatorActions.LoadCalendarEventTypes)
  loadCalendarEventTypes(ctx: StateContext<EventCreatorStateModel>) {
    this.setEntityPending(ctx, eventStatusesStateKey);
    return this.eventCreatorService.getCalendarEventTypes()
      .pipe(
        tap(result => {
          this.setEntityLoadSuccess(ctx, eventStatusesStateKey, result);
        }),
        catchError(error => {
          return this.setEntityLoadFailure(ctx, eventStatusesStateKey, error);
        })
      );
  }

}
