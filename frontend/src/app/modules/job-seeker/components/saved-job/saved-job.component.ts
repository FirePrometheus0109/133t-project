import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Enums } from '../../../shared/models/enums.model';


@Component({
  selector: 'app-saved-job',
  templateUrl: './saved-job.component.html',
  styleUrls: ['./saved-job.component.css']
})
export class SavedJobComponent {
  @Input() jobItem: any;
  @Input() enums: Enums;
  @Input() isDashboard: boolean;
  @Output() goToCompanyProfile = new EventEmitter<number>();
  @Output() goToJobPage = new EventEmitter<number>();

  public navigateToJob() {
    this.goToJobPage.emit(this.jobItem.id);
  }

  public navigateToCompany() {
    if (!this.isDashboard) {
      this.goToCompanyProfile.emit(this.jobItem.company.id);
    }
  }
}
