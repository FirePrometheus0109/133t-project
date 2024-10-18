import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { AnswersActions } from '../actions';
import { AnswerData } from '../models/answer.model';


class AnswersStateModel {
  status: string;
  errors: object;
  answersList: Array<AnswerData>;
}


export const DEFAULT_ANSWERS_STATE = {
  status: '',
  errors: null,
  answersList: [],
};


@State<AnswersStateModel>({
  name: 'AnswersState',
  defaults: DEFAULT_ANSWERS_STATE
})
export class AnswersState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static answersList(state: any) {
    return state.answersList;
  }

  constructor(private jobService: JobService) {
  }

  @Action(AnswersActions.SetAnswerToAnswersList)
  setAnswerToAnswersList(ctx, {answerData}: AnswersActions.SetAnswerToAnswersList) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    state = ctx.getState();
    const answersList = state.answersList;
    const indexById = answersList.findIndex(item => item.question === answerData.question);
    if (indexById < 0) {
      answersList.push(answerData);
    } else {
      answersList[indexById] = answerData;
    }
    return ctx.setState({
      ...state,
      status: 'done',
      errors: null,
      answersList: answersList,
    });
  }

  @Action(AnswersActions.ResetAnswerList)
  resetAnswerList(ctx) {
    const state = ctx.getState();
    return ctx.setState({
      ...state,
      answersList: [],
    });
  }

  @Action(AnswersActions.SendAnswersList)
  sendAnswersList(ctx, {jobId}: AnswersActions.SendAnswersList) {
    let state = ctx.getState();
    const answerDataList = state.answersList;
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.jobService.postAnswersForJob(jobId, answerDataList).pipe(
      tap(() => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          answersList: [],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
        }));
      })
    );
  }
}
