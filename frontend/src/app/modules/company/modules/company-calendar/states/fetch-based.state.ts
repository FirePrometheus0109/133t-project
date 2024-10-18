import { StateContext } from '@ngxs/store';
import { of } from 'rxjs';

export abstract class FetchBasedState {
  abstract defaultState;

  setEntityPending<T>(ctx: StateContext<T>, entity: string, value = true) {
    const state = ctx.getState();
    return ctx.patchState({
      [entity]: {
        ...state[entity],
        pending: value,
      }
    } as T);
  }

  setEntityLoadSuccess<T>(ctx: StateContext<T>, entity: string, data) {
    return ctx.patchState({
      [entity]: {
        ...this.defaultState[entity],
        data: data
      }
    } as T);
  }

  setEntityLoadFailure<T>(ctx: StateContext<T>, entity: string, error) {
    ctx.patchState({
      [entity]: {
        ...this.defaultState[entity],
        errors: error.error || error
      }
    } as T);
    return of(error);
  }
}
