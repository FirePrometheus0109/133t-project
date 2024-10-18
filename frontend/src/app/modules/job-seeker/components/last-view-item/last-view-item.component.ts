import { Component, EventEmitter, Input, Output } from '@angular/core';
import { JobSeekerLastViewsItemModel } from '../../models/job-seeker-last-views.model';


@Component({
  selector: 'app-last-view-item',
  templateUrl: './last-view-item.component.html',
  styleUrls: ['./last-view-item.component.scss']
})
export class LastViewItemComponent {
  @Input() lastViewItem: JobSeekerLastViewsItemModel;
  @Output() goToCompanyProfile = new EventEmitter<number>();
}
