import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-candidate-answer',
  template: `
    <mat-card>
      <mat-card-title><p>{{answer.question.body}}</p></mat-card-title>
      <mat-card-content>
        <mat-radio-button disabled="true" checked="{{answer.answer === 'YES'}}">{{answer.answer}}</mat-radio-button>
        <span class="disc-answer" *ngIf="answer.is_disqualify">Disqualifying answer</span></mat-card-content>
    </mat-card>`,
  styles: [`
    .disc-answer {
      color: red;
    }
  `]
})
export class ViewCandidateAnswerComponent {
  @Input() answer;
}
