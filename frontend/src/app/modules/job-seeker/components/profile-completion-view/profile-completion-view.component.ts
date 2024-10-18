import { Component, Input } from '@angular/core';
import { JobSeekerProfileCompletionModel, TooltipCompletionItemModel } from '../../models/job-seeker-profile-completion.model';


@Component({
  selector: 'app-profile-completion-view',
  templateUrl: './profile-completion-view.component.html',
  styleUrls: ['./profile-completion-view.component.scss']
})
export class ProfileCompletionViewComponent {
  @Input() profileCompletion: JobSeekerProfileCompletionModel;

  private fullCompletion = 100;
  private regexToFieldReplace = /_+/g;

  public checkIsProfileCompleted() {
    return this.profileCompletion && this.profileCompletion.total_complete === this.fullCompletion;
  }

  public get getTooltipText(): string {
    if (this.profileCompletion && this.profileCompletion.need_complete.length !== 0) {
      return this.profileCompletion.need_complete.map((item: TooltipCompletionItemModel) => {
        return `Add ${this.transformFieldString(item.field)} +${item.add_percents}%`;
      }).join(`\n`);
    } else {
      return '';
    }
  }

  private transformFieldString(field: string) {
    return field.replace(this.regexToFieldReplace, ' ');
  }
}
