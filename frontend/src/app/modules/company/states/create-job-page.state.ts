import { Action, State, StateContext } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { CoreActions } from '../../core/actions';
import { NavigationService } from '../../core/services/navigation.service';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { BaseBlockablePageState } from '../../shared/states/base.form.state';
import { CreateJobPageActions } from '../actions';
import { CompanyService } from '../services/company.service';


class CreateJobPageStateModel {
  status: string;
  errors: object;
}


export const DEFAULT_COMPANY_PROFILE_PAGE_STATE = {
  status: '',
  errors: null,
};


@State<CreateJobPageStateModel>({
  name: 'CreateJobPage',
  defaults: DEFAULT_COMPANY_PROFILE_PAGE_STATE,
})
export class CreateJobPageState extends BaseBlockablePageState {
  constructor(private companyService: CompanyService,
              private navigationService: NavigationService) {
    super();
  }

  @Action(CreateJobPageActions.LoadInitialData)
  loadInitialData(ctx: StateContext<CreateJobPageStateModel>) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      status: 'pending',
    });
  }

  @Action(CreateJobPageActions.CreateNewJob)
  createNewJob(ctx: StateContext<CreateJobPageStateModel>,
               {data, successPostMessage}: CreateJobPageActions.CreateNewJob) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.companyService.createNewJob(data).pipe(
      tap(() => {
        state = ctx.getState();
        ctx.setState({
          ...state,
          status: 'done',
          errors: null,
        });
        ctx.dispatch(new CoreActions.SnackbarOpen({
          message: successPostMessage,
          delay: 5000,
          type: SnackBarMessageType.SUCCESS,
        }));
        return this.navigationService.goToCompanyJobListPage();
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      }),
    );
  }
}

