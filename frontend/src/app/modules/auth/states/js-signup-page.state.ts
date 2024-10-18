import { SetFormDisabled, SetFormEnabled, UpdateFormErrors, UpdateFormStatus } from '@ngxs/form-plugin';
import { Action, Selector, State } from '@ngxs/store';
import { NavigationService } from '../../core/services/navigation.service';
import { DEFAULT_FORM_STATE } from '../../shared/states/base.form.state';
import { AuthActions, JobSeekerSignupPageActions } from '../actions';


@State({
  name: 'jssignup',
  defaults: DEFAULT_FORM_STATE,
})
export class JobSeekerSignupFormState {
  @Selector()
  static pending(state: any) {
    return state.form.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.form.errors;
  }

  constructor(private navigationService: NavigationService) {
  }

  @Action(JobSeekerSignupPageActions.Signup)
  jssignup(ctx, action: JobSeekerSignupPageActions.Signup) {
    ctx.dispatch(new SetFormDisabled('jssignup.form'));
    ctx.dispatch(new UpdateFormStatus({status: 'pending', path: 'jssignup.form'}));
    ctx.dispatch(new AuthActions.JobSeekerSignup(action.credentials)).subscribe(() => {
        const state = ctx.getState();
        ctx.setState({
          ...state,
          ...DEFAULT_FORM_STATE,
        });
        return this.navigationService.goToLoginPage();
      },
      httpError => {
        ctx.dispatch(new UpdateFormErrors({errors: httpError.error, path: 'jssignup.form'}));
        ctx.dispatch(new UpdateFormStatus({status: 'invalid', path: 'jssignup.form'}));
        return ctx.dispatch(new SetFormEnabled('jssignup.form'));
      },
    );
  }
}
