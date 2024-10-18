import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import * as moment from 'moment';
import { NavigationService } from 'src/app/modules/core/services/navigation.service';
import { Enums } from 'src/app/modules/shared/models/enums.model';
import { DateTimeHelper } from '../../../shared/helpers/date-time.helper';
import { JobSeekerListMode } from '../../models/job-seeker-list-fitlers.model';


@Component({
  selector: 'app-job-seeker-item',
  templateUrl: './job-seeker-item.component.html',
  styleUrls: ['./job-seeker-item.component.scss']
})
export class JobSeekerItemComponent implements OnInit {
  @Input() jobSeekerItem: any;
  @Input() checkBoxName: string;
  @Input() editable = true;
  @Input() enums: Enums;
  @Input() listMode: number;
  @Output() commentJobSeeker = new EventEmitter<number>();

  public currentJob;

  constructor(private navigationService: NavigationService) {
  }

  ngOnInit() {
    this.currentJob = this.lastCurrentJob;
  }

  public get isCommentsAvailable() {
    return this.listMode !== JobSeekerListMode.ALL;
  }

  goToJobSeekerProfilePage(id: string) {
    this.navigationService.goToJobSeekerProfileViewPage(id);
  }

  getDateFormatted(date: string) {
    return DateTimeHelper.getDate(date);
  }

  get lastCurrentJob() {
    const currentJobs = this.jobSeekerItem.job_experience.filter(job => job.is_current).sort((jobA, jobB) => {
      return moment(jobA.date_from).isAfter(jobB.date_from) ? -1 : 1;
    });
    return currentJobs[0];
  }
}
