import {Component, EventEmitter, Input, Output} from '@angular/core';
import {EducationItem, EducationType} from '../../models/education.model';
import {Enums} from '../../models/enums.model';

@Component({
  selector: 'app-jsp-education-preview',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>{{educationItem.institution}}</h4>
      </mat-card-title>
      <mat-card-content>
        <div class="type">{{educationItem.type || EducationType.EDUCATION}}</div>
        <div class="field_of_study">{{educationItem.field_of_study}}</div>
        <div class="degree">{{enums.EducationTypes[educationItem.degree]}}</div>
        <div class="location">{{educationItem.location}}</div>
        <div class="date_from">{{educationItem.date_from | date}}</div>
        <div class="date_to">{{educationItem.date_to | date}}</div>
        <div class="action" *ngIf="isJSPEdit">
          <button mat-button (click)="editEducation()">
            <mat-icon matSuffix>edit</mat-icon>
          </button>
          <button mat-button (click)="deleteEducation()">
            <mat-icon matSuffix>delete</mat-icon>
          </button>
        </div>
      </mat-card-content>

    </mat-card>
  `,
  styles: [],
})
export class JspEducationPreviewComponent {
  @Input() educationItem: any;
  @Input() isJSPEdit: boolean;
  @Input() enums: Enums;
  @Output() deleteItem = new EventEmitter<number>();
  @Output() editItem = new EventEmitter<EducationItem>();

  public EducationType = EducationType;

  public deleteEducation() {
    this.deleteItem.emit(this.educationItem.id);
  }

  public editEducation() {
    this.editItem.emit(this.educationItem);
  }
}
