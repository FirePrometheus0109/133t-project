import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Question } from '../models/question.model';


@Component({
  selector: 'app-question-preview',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>{{index}}. {{questionItem.body}}</h4>
      </mat-card-title>
      <mat-card-content>
        <div class="answer-variants">
          <div>
            <span>Yes</span><span *ngIf="questionItem.disqualifying_answer === 'YES'">- Disqualifying answer</span>
          </div>
          <div>
            <span>No</span><span *ngIf="questionItem.disqualifying_answer === 'NO'">- Disqualifying answer</span>
          </div>
        </div>
        <div *ngIf="questionItem.is_answer_required">
          <span>Answer required</span>
        </div>
      </mat-card-content>
      <mat-card-actions *ngIf="!modalMode">
        <button type="button" mat-raised-button color="primary"
                (click)="editQuestion.emit(questionItem)"
                [disabled]="questionItem.is_default">
          <mat-icon matSuffix>edit</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary" (click)="deleteQuestion.emit(questionItem.id)">
          <mat-icon matSuffix>delete</mat-icon>
        </button>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [],
})
export class QuestionPreviewComponent {
  @Input() questionItem: Question;
  @Input() index: number;
  @Input() modalMode: boolean;
  @Output() editQuestion = new EventEmitter<Question>();
  @Output() deleteQuestion = new EventEmitter<number>();
}
