import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { JobService } from '../../company/services/job.service';
import { ViewAnsweredQuestionnaireActions } from '../actions';
import { QuestionAnswer } from '../models/question-answer.model';


class ViewAnsweredQuestionnaireStateModel {
  status: string;
  errors: object;
  answerData: Array<QuestionAnswer>;
}


export const DEFAULT_ANSWERED_QUESTIONNAIRE_STATE = {
  status: '',
  errors: null,
  answerData: null,
};


@State<ViewAnsweredQuestionnaireStateModel>({
  name: 'ViewAnsweredQuestionnaireState',
  defaults: DEFAULT_ANSWERED_QUESTIONNAIRE_STATE
})
export class ViewAnsweredQuestionnaireState {
  @Selector()
  static answerData(state: any) {
    return state.answerData;
  }

  constructor(private service: JobService) {
  }

  @Action(ViewAnsweredQuestionnaireActions.LoadAnswers)
  loadAnswers(ctx, {jobId, jobSeekerId}: ViewAnsweredQuestionnaireActions.LoadAnswers) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending',
    });
    return this.service.getCandidateAnswer(jobId, jobSeekerId).pipe(
      tap((data) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          answerData: data,
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          answerData: null,
        }));
      }),
    );
  }
}
