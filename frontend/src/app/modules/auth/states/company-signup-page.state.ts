import { SetFormDisabled, SetFormEnabled, UpdateFormErrors, UpdateFormStatus } from '@ngxs/form-plugin';
import { Action, Selector, State } from '@ngxs/store';
import { NavigationService } from '../../core/services/navigation.service';
import { DEFAULT_FORM_STATE } from '../../shared/states/base.form.state';
import { AuthActions, CompanySignupPageActions } from '../actions';


@State({
  name: 'companysignup',
  defaults: DEFAULT_FORM_STATE,
})
export class CompanySignupFormState {
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

  @Action(CompanySignupPageActions.Signup)
  companysignup(ctx, action: CompanySignupPageActions.Signup) {
    ctx.dispatch(new SetFormDisabled('companysignup.form'));
    ctx.dispatch(new UpdateFormStatus({status: 'pending', path: 'companysignup.form'}));
    ctx.dispatch(new AuthActions.CompanySignup(action.credentials)).subscribe(
      () => {
        const state = ctx.getState();
        ctx.setState({
          ...state,
          ...DEFAULT_FORM_STATE,
        });
        return this.navigationService.goToLoginPage();
      },
      httpError => {
        ctx.dispatch(new UpdateFormErrors({errors: httpError.error, path: 'companysignup.form'}));
        ctx.dispatch(new UpdateFormStatus({status: 'invalid', path: 'companysignup.form'}));
        return ctx.dispatch(new SetFormEnabled('companysignup.form'));
      },
    );
  }
}
