import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { QuestionAnswer } from '../models/question-answer.model';
import { ViewAnsweredQuestionnaireState } from '../states/view-answered-questionnaire.state';


@Component({
  selector: 'app-view-answered-questionnaire',
  template: `
    <app-candidate-answer *ngFor="let answer of answerData$ | async" [answer]="answer">
    </app-candidate-answer>
  `,
  styles: []
})
export class ViewAnsweredQuestionnaireComponent {
  @Select(ViewAnsweredQuestionnaireState.answerData) answerData$: Observable<Array<QuestionAnswer>>;
}
