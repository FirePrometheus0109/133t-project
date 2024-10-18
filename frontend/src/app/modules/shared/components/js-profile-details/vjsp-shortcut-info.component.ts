import { Component, Input } from '@angular/core';
import { AddressFull } from '../../models';
import { JobItem } from '../../models/experience.model';


@Component({
  selector: 'app-vjsp-shortcut-info',
  template: `
    <div class="profile-shortcut">
      <div>
        {{addressData?.city?.name}}
        ({{addressData?.city?.state?.abbreviation}})
      </div>
      <div *ngFor="let job of getIsCurrentJobs()">
        {{job?.job_title}} at {{job?.company}}
      </div>
    </div>
  `,
  styles: [`
    .profile-shortcut {
      margin-bottom: 20px;
    }
  `],
})
export class VjspShortcutInfoComponent {
  @Input() addressData: AddressFull;
  @Input() experience: Array<JobItem>;

  getIsCurrentJobs() {
    return this.experience.filter(job => job.is_current);
  }
}
