import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DateTimeHelper } from '../../../shared/helpers/date-time.helper';
import { CandidateActivityModel } from '../../models/candidate-activity.model';


@Component({
  selector: 'app-candidate-activity-item',
  templateUrl: './candidate-activity-item.component.html',
  styleUrls: ['./candidate-activity-item.component.scss']
})
export class CandidateActivityItemComponent {
  @Input() activityItem: CandidateActivityModel;
  @Output() navigateToCandidate = new EventEmitter<number>();
  @Output() navigateToJob = new EventEmitter<number>();

  public get activityBody() {
    if (this.activityItem.activity === 'Applied') {
      return `${this.activityItem.activity} to the `;
    } else {
      return `Was ${this.activityItem.activity.toLowerCase()} to the `;
    }
  }

  public get formattedTime() {
    return DateTimeHelper.getDateWithTime(this.activityItem.created_at);
  }
}
