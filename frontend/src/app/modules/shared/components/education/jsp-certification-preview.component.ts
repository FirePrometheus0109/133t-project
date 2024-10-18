import {Component, EventEmitter, Input, Output} from '@angular/core';
import {CertificationItem, EducationType} from '../../models/education.model';

@Component({
  selector: 'app-jsp-certification-preview',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>{{certificationItem.institution}}</h4>
      </mat-card-title>
      <mat-card-content>
        <div class="type">{{certificationItem.type || EducationType.CERTIFICATION}}</div>
        <div class="field_of_study">{{certificationItem.field_of_study}}</div>
        <div class="location">{{certificationItem.location}}</div>
        <div class="graduation">{{certificationItem.graduated | date}}</div>
        <div class="action" *ngIf="isJSPEdit">
          <button mat-button (click)="editCertification()">
            <mat-icon matSuffix>edit</mat-icon>
          </button>
          <button mat-button (click)="deleteCertification()">
            <mat-icon matSuffix>delete</mat-icon>
          </button>
        </div>
      </mat-card-content>

    </mat-card>
  `,
  styles: [],
})
export class JspCertificationPreviewComponent {
  @Input() certificationItem: any;
  @Input() isJSPEdit: boolean;
  @Output() deleteItem = new EventEmitter<number>();
  @Output() editItem = new EventEmitter<CertificationItem>();

  public EducationType = EducationType;

  public deleteCertification() {
    this.deleteItem.emit(this.certificationItem.id);
  }

  public editCertification() {
    this.editItem.emit(this.certificationItem);
  }
}
