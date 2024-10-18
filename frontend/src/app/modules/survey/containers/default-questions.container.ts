import { Component } from '@angular/core';
import { Select } from '@ngxs/store';
import { Observable } from 'rxjs';
import { Question } from '../models/question.model';
import { DefaultQuestionsState } from '../states/default-questions.state';


@Component({
  selector: 'app-default-questions',
  template: `
    <div>
      <mat-card>
        <mat-card-header>
          <mat-card-title>
            <h3>Default questions</h3>
          </mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div *ngFor="let defaultQuestion of (defaultQuestionList$ | async); index as i">
            <p>{{i + 1}}.&nbsp;{{defaultQuestion.body}}</p>
          </div>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [],
})
export class DefaultQuestionsComponent {
  @Select(DefaultQuestionsState.defaultQuestionList) defaultQuestionList$: Observable<Array<Question>>;
}
