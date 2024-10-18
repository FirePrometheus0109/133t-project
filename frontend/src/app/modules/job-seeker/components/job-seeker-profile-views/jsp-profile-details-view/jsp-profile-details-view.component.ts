import { Component, EventEmitter, Input, Output } from '@angular/core';
import { JobSeekerProfileDetailsEnum } from '../../../../shared/enums/job-seeker-profile.enums';
import { Enums } from '../../../../shared/models/enums.model';


@Component({
  selector: 'app-jsp-profile-details-view',
  templateUrl: './jsp-profile-details-view.component.html',
  styleUrls: ['./jsp-profile-details-view.component.scss']
})
export class JspProfileDetailsViewComponent {
  @Input() initialData: any;
  @Input() enums: Enums;
  @Output() changeToEditMode = new EventEmitter<boolean>();

  public JobSeekerProfileDetailsEnum = JobSeekerProfileDetailsEnum;
}
