import { Component, EventEmitter, Input, Output } from '@angular/core';
import { AnswerData } from '../../../survey/models/answer.model';
import { Question } from '../../../survey/models/question.model';
import { AnswerVariants } from '../../enums/answer-variants';


@Component({
  selector: 'app-yes-no-answer-form',
  template: `
    <mat-card>
      <mat-card-content>
        <div class="question-body">
          <div>{{questionItem.body}}</div>
          <div *ngIf="questionItem.is_answer_required">*Answer required</div>
          <div>
            <mat-radio-group (change)="answerChanged($event)">
              <mat-radio-button [value]="AnswerVariants.YES">{{AnswerVariants.YES}}</mat-radio-button>
              <mat-radio-button [value]="AnswerVariants.NO">{{AnswerVariants.NO}}</mat-radio-button>
            </mat-radio-group>
          </div>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class YesNoAnswerComponent {
  @Input() questionItem: Question;
  @Output() change = new EventEmitter<AnswerData>();

  public AnswerVariants = AnswerVariants;

  answerChanged(event) {
    this.change.emit({
      question: this.questionItem.id,
      answer: {
        yes_no_value: event.value.toUpperCase()
      }
    });
  }
}
