import { Component, Input } from '@angular/core';
import { EducationType } from '../../../shared/models/education.model';
import { Enums } from '../../../shared/models/enums.model';


@Component({
  selector: 'app-vjsp-education-detail',
  template: `
    <div *ngFor="let education of educationAndCertificationData">
      <app-jsp-education-preview *ngIf="education.type === EducationType.EDUCATION"
                                 [educationItem]="education"
                                 [enums]="enums">
      </app-jsp-education-preview>
      <app-jsp-certification-preview *ngIf="education.type === EducationType.CERTIFICATION"
                                     [certificationItem]="education">
      </app-jsp-certification-preview>
    </div>
  `,
  styles: [],
})
export class VjspEducationDetailComponent {
  @Input() educationAndCertificationData: Array<any>;
  @Input() enums: Enums;

  public EducationType = EducationType;
}
