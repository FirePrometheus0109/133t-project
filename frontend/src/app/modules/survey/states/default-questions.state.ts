import { Action, Selector, State } from '@ngxs/store';
import { of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { DefaultQuestionsActions } from '../actions';
import { Question } from '../models/question.model';
import { DefaultQuestionsService } from '../services/default-questions.service';


class DefaultQuestionsStateModel {
  status: string;
  errors: object;
  defaultQuestionList: Array<Question>;
}


export const PREVENTED_DEFAULT_QUESTIONS_STATE = {
  status: '',
  errors: null,
  defaultQuestionList: [],
};


@State<DefaultQuestionsStateModel>({
  name: 'DefaultQuestions',
  defaults: PREVENTED_DEFAULT_QUESTIONS_STATE
})
export class DefaultQuestionsState {
  @Selector()
  static pending(state: any) {
    return state.status === 'pending';
  }

  @Selector()
  static errors(state: any) {
    return state.errors;
  }

  @Selector()
  static defaultQuestionList(state: any) {
    return state.defaultQuestionList;
  }

  constructor(private defaultQuestionsService: DefaultQuestionsService) {
  }

  @Action(DefaultQuestionsActions.LoadDefaultQuestionList)
  loadDefaultQuestionList(ctx) {
    let state = ctx.getState();
    ctx.setState({
      ...state,
      status: 'pending'
    });
    return this.defaultQuestionsService.getDefaultQuestionsList().pipe(
      tap((result) => {
        state = ctx.getState();
        return ctx.setState({
          ...state,
          status: 'done',
          errors: null,
          defaultQuestionList: result['results'],
        });
      }),
      catchError(error => {
        state = ctx.getState();
        return of(ctx.setState({
          ...state,
          status: 'error',
          errors: error.error,
          defaultQuestionList: [],
        }));
      })
    );
  }
}
