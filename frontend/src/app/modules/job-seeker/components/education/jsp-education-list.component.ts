import { Component, EventEmitter, Input, Output } from '@angular/core';
import { BaseFormComponent } from '../../../shared/components/base-form.component';
import { EducationType } from '../../../shared/models/education.model';
import { Enums } from '../../../shared/models/enums.model';


@Component({
  selector: 'app-jsp-education-list-form',
  template: `
    <mat-card>
      <mat-card-title>
        <h4>Education list</h4>
      </mat-card-title>
      <mat-card-content>
        <div *ngFor="let item of initialData">
          <app-jsp-education-preview *ngIf="item.type === EducationType.EDUCATION" [educationItem]="item"
                                     [isJSPEdit]="true"
                                     [enums]="enums"
                                     (deleteItem)="deleteEducation($event)"
                                     (editItem)="editEducationItem.emit($event)">
          </app-jsp-education-preview>
          <app-jsp-certification-preview *ngIf="item.type === EducationType.CERTIFICATION" [certificationItem]="item"
                                         [isJSPEdit]="true"
                                         (deleteItem)="deleteCertification($event)"
                                         (editItem)="editCertificationItem.emit($event)">
          </app-jsp-certification-preview>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class JspEducationListComponent extends BaseFormComponent {
  @Input() enums: Enums;
  @Output() deletedEducationItem = new EventEmitter<number>();
  @Output() deletedCertificationItem = new EventEmitter<number>();
  @Output() editEducationItem = new EventEmitter<any>();
  @Output() editCertificationItem = new EventEmitter<any>();

  public EducationType = EducationType;

  public deleteEducation(itemId: number) {
    this.deletedEducationItem.emit(itemId);
  }

  public deleteCertification(itemId: number) {
    this.deletedCertificationItem.emit(itemId);
  }
}
