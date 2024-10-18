import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-candidate',
  template: `
    <mat-card>
      <span> {{userData?.candidate.name}}</span>
      <span> Applied on  {{userData.created_at}}</span>
      <span (click)="viewQuestionnaire(userData?.candidate.id)">View Questionnaire</span>
    </mat-card>
  `,
  styles: [`
    mat-card :last-child {
      float: right;
      margin-right: 100px;
    }
  `],
})
export class AppliedUserComponent {
  @Input() userData: any;
  @Input() viewQuestionnaire: Function;
}
