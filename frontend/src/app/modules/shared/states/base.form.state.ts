import {Selector} from '@ngxs/store';

export const DEFAULT_FORM_STATE = {
  form: {
    model: undefined,
    dirty: false,
    status: '',
    errors: {},
  },
};

export class BaseBlockablePageState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }
}
