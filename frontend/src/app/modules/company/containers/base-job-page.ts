import { FormGroup } from '@angular/forms';
import * as moment from 'moment';
import { JobStatus } from '../../shared/enums/job-statuses';


export abstract class BaseJobPage {
  protected requiredFieldsForPublishJob: string[] = [];

  abstract getBaseJobData(): {};

  protected get getPublishJobRequiredFieldsErrorMessage(): string {
    return `You can\'t publish job without required fields: ${this.requiredFieldsForPublishJob}`;
  }

  protected getFormSkills(form: FormGroup, propertyName: string): number[] {
    const skillsId = [];
    if (form.value[propertyName]) {
      form.value[propertyName].forEach((skill) => {
        skillsId.push(skill.id);
      });
    }
    return skillsId;
  }

  protected isJobValidForPublish(data: {}): boolean {
    this.requiredFieldsForPublishJob = this.getValidationFields(data['education_strict']);
    return this.requiredFieldsForPublishJob.every((field) => {
      return data.hasOwnProperty(field) && data[field].toString().length > 0;
    });
  }

  /**
   * Essentially general method to collect all needed data to save job.
   */
  protected getJobData(publishDateForm: FormGroup, isPublish: boolean, jobStatusForm: FormGroup = null): object {
    return Object.assign(
      this.getBaseJobData(),
      this.getJobPublishDate(publishDateForm, isPublish),
      this.getJobDeleteDate(publishDateForm),
      this.getJobStatus(publishDateForm, isPublish, jobStatusForm),
    );
  }

  /**
   * Return object with publish date, value depends on selected date in form and with what method saved.
   */
  protected getJobPublishDate(publishDateForm: FormGroup, isPublish: boolean): object {
    const formDate = publishDateForm.value.publish_date;
    if (!formDate && !isPublish) {
      return {};
    } else if (!formDate && isPublish) {
      const currentDate = moment();
      publishDateForm.patchValue({publish_date: currentDate});
      return {
        publish_date: this.getUtcDateWithoutTime(currentDate),
      };
    } else {
      return {
        publish_date: this.getUtcDateWithoutTime(formDate),
      };
    }
  }

  /**
   * Return object with delete date, value depends on selected date in form and with what method saved.
   */
  protected getJobDeleteDate(publishDateForm: FormGroup): object {
    const date = publishDateForm.value.closing_date;
    const closing_date = date ? this.getUtcDateWithoutTime(date) : null;
    return {
      closing_date,
    };
  }

  /**
   * Return object with job status, value depends on predefined publish date, what method was caused and current job
   * status form value.
   */
  protected getJobStatus(publishDateForm: FormGroup, isPublish: boolean, jobStatusForm: FormGroup): object {
    const dateFormat = 'L';
    const formDate = publishDateForm.value.publish_date;
    const currentDate: Date = new Date();
    let status: string;
    if (!jobStatusForm) {
      if (!formDate) {
        status = JobStatus.DRAFT;
      } else if (moment(formDate).format(dateFormat) === moment(currentDate).format(dateFormat)) {
        status = JobStatus.ACTIVE;
      } else {
        status = JobStatus.DELAYED;
      }
    } else {
      status = jobStatusForm.value.status;
    }
    return {status: status};
  }

  protected getValidationFields(isEducationStrict: boolean): string[] {
    const requiredFieldsForPublishJob = [
      'title',
      'location',
      'industry',
      'position_type',
      'description',
    ];
    if (isEducationStrict) {
      requiredFieldsForPublishJob.push('education');
    }
    return requiredFieldsForPublishJob;
  }

  getUtcDateWithoutTime(date) {
    const utcDateWithTime = this.getUtcDateWithTime(date);
    return moment.utc([
      utcDateWithTime.year(),
      utcDateWithTime.month(),
      utcDateWithTime.date(),
    ]);
  }

  getUtcDateWithTime(date) {
    const utcDate = moment.utc(date);
    return moment().set({
      year: utcDate.year(),
      month: utcDate.month(),
      date: utcDate.date(),
    }).utc();
  }
}
