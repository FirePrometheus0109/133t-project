import { Component, Input } from '@angular/core';
import { JobSeekerAutoApplyProgressItem } from '../../models/job-seeker-auto-apply-progress.model';


@Component({
  selector: 'app-job-seeker-auto-apply-progress-item',
  templateUrl: './job-seeker-auto-apply-progress-item.component.html',
  styleUrls: ['./job-seeker-auto-apply-progress-item.component.scss']
})
export class JobSeekerAutoApplyProgressItemComponent {
  @Input() autoApplyProgressItem: JobSeekerAutoApplyProgressItem;
}
