import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import * as CoreActions from '../../../core/actions/core.actions';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';
import { InputLengths } from '../../../shared/constants/validators/input-length';
import { JobStatus } from '../../../shared/enums/job-statuses';
import { Enums } from '../../../shared/models/enums.model';
import { SnackBarMessageType } from '../../../shared/models/snack-bar-message';
import { ConfirmationDialogService } from '../../../shared/services/confirmation-dialog.service';
import { UtilsService } from '../../../shared/services/utils.service';
import { ValidationService } from '../../../shared/services/validation.service';
import { SurveyListActions } from '../../../survey/actions';
import { SurveyState } from '../../../survey/states/survey.state';
import { EditJobPageActions } from '../../actions';
import { ViewJobPreviewComponent } from '../../components/view-job-preview.component';
import { EditJobPageState } from '../../states/edit-job-page.state';
import { BaseJobPage } from '../base-job-page';


@Component({
  selector: 'app-edit-job-page',
  templateUrl: './edit-job-page.component.html',
  styleUrls: ['./edit-job-page.component.css']
})
export class EditJobPageComponent extends BaseJobPage implements OnInit, OnDestroy {

  constructor(private route: ActivatedRoute,
              private store: Store,
              private dialog: MatDialog,
              private navigationService: NavigationService,
              private confirmationDialogService: ConfirmationDialogService) {
    super();
  }

  public get surveyForJobEdit() {
    return this.store.selectSnapshot(SurveyState.surveyForJobEdit);
  }

  public get companyId() {
    return this.store.selectSnapshot(EditJobPageState.initialData).company;
  }

  public get isSaveAndPublishAvailable(): boolean {
    return this._isSaveAndPublishAvailable;
  }

  @Select(EditJobPageState.initialData) initialData$: Observable<any>;
  @Select(EditJobPageState.pending) pending$: Observable<any>;
  @Select(EditJobPageState.errors) errors$: Observable<any>;
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CoreState.JobStatusEnum) jobStatusEnums$: Observable<object>;

  private deleteJobConfirmationText =
    'Are you sure you want to save job posting in Closed status? Note that all candidates will be moved to Rejected.';

  public jobStatusForm: FormGroup = new FormGroup({
    status: new FormControl('', Validators.required),
  });

  public jobIndustryForm: FormGroup = new FormGroup({
    industry: new FormControl('', Validators.compose([Validators.required, ValidationService.selectListObjectValidator]))
  });

  public jobInfoForm: FormGroup = new FormGroup({
    title: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
  });

  public addressForm = new FormGroup({
    city: new FormControl('', Validators.required),
    country: new FormControl('', Validators.required),
    zip: new FormControl('', Validators.maxLength(InputLengths.zip))
  });

  public jobProfileDetailsForm: FormGroup = new FormGroup({
    position_type: new FormControl('', Validators.required),
    education: new FormControl(''),
    education_strict: new FormControl(false),
    experience: new FormControl(''),
    travel: new FormControl(''),
    salary_min: new FormControl('', Validators.required),
    salary_max: new FormControl('', Validators.required),
    salary_negotiable: new FormControl(false),
    clearance: new FormControl(''),
    benefits: new FormControl(''),
  }, ValidationService.educationValidator);

  public jobDescriptionForm: FormGroup = new FormGroup({
    description: new FormControl('',
      Validators.compose([Validators.required, Validators.maxLength(InputLengths.jobDescription)])),
  });

  public jobRequiredSkillsForm: FormGroup = new FormGroup({
    required_skills: new FormControl([]),
  });

  public jobOptionalSkillsForm: FormGroup = new FormGroup({
    optional_skills: new FormControl([]),
  });

  public jobPublishDateForm: FormGroup = new FormGroup({
    publish_date: new FormControl(''),
    closing_date: new FormControl(''),
  }, ValidationService.jobDateValidator);

  public jobCoverLetterForm: FormGroup = new FormGroup({
    is_cover_letter_required: new FormControl(false),
  });

  public requiredSkillPropertyName = 'required_skills';
  public optionalSkillPropertyName = 'optional_skills';

  private _isSaveAndPublishAvailable = false;
  private jobId: number;

  private static isJobClosed(status) {
    return JobStatus.CLOSED === status;
  }

  ngOnInit() {
    this.jobId = this.route.snapshot.params['jobId'];
  }

  ngOnDestroy() {
    this.store.dispatch(new SurveyListActions.SetJobEditMode(false));
    this.store.dispatch(new SurveyListActions.SetModalMode(false));
    this.store.dispatch(new SurveyListActions.SetCurrentSurvey(null));
    this.store.dispatch(new SurveyListActions.UpdateSurveyForJobEdit([]));
  }

  public postJobData(isPublish: boolean = false) {
    const data: object = this.getJobData(this.jobPublishDateForm, isPublish, this.jobStatusForm);
    if (data['publish_date']) {
      if (!this.isJobValidForPublish(data)) {
        return this.store.dispatch(new CoreActions.SnackbarOpen({
          message: this.getPublishJobRequiredFieldsErrorMessage,
          type: SnackBarMessageType.ERROR,
          delay: 10000,
        }));
      }
    }
    if (EditJobPageComponent.isJobClosed(data['status'])) {
      return this.onMoveToClosedJobStatus(data);
    }
    return this.postJob(data);
  }

  public goToJobListPage() {
    this.navigationService.goToCompanyJobListPage();
  }

  private onMoveToClosedJobStatus(data: object) {
    return this.confirmationDialogService.openConfirmationDialog({
      message: `${this.deleteJobConfirmationText}`,
      callback: this.postJob.bind(this, data),
      confirmationText: 'Save anyway',
    });
  }

  public previewJob() {
    this.store.dispatch(new EditJobPageActions.PreviewJob()).subscribe((state) => {
      const dialogRef = this.dialog.open(ViewJobPreviewComponent, {
        width: '80%',
        data: {
          jobItem: this.getJobPreviewData(),
          enums: state.core.enums,
          isEditable: true,
        },
      });
      dialogRef.afterClosed().subscribe((result: boolean) => {
        if (result) {
          this.postJobData();
          this.goToJobListPage();
        }
        dialogRef.close();
      });
    });
  }

  public onStatusChanged(formData: any) {
    const previousStatusDraftOrClosed: boolean = [JobStatus.DRAFT, JobStatus.CLOSED].includes(
      this.store.selectSnapshot(EditJobPageState.initialData).status);
    const newStatusIsActive = formData.value === JobStatus.ACTIVE;
    this._isSaveAndPublishAvailable = (previousStatusDraftOrClosed && newStatusIsActive);
  }

  public getBaseJobData(): object {
    return {
      industry: this.jobIndustryForm.value.industry.id,
      title: this.jobInfoForm.value.title,
      location: UtilsService.prepareAddressData(this.addressForm.value),
      position_type: this.jobProfileDetailsForm.value.position_type,
      education: this.jobProfileDetailsForm.value.education,
      education_strict: this.jobProfileDetailsForm.value.education_strict,
      experience: this.jobProfileDetailsForm.value.experience,
      travel: this.jobProfileDetailsForm.value.travel,
      salary_min: this.jobProfileDetailsForm.value.salary_min,
      salary_max: this.jobProfileDetailsForm.value.salary_max,
      salary_negotiable: this.jobProfileDetailsForm.value.salary_negotiable,
      clearance: this.jobProfileDetailsForm.value.clearance,
      benefits: this.jobProfileDetailsForm.value.benefits,
      description: this.jobDescriptionForm.value.description,
      required_skills: this.getFormSkills(this.jobRequiredSkillsForm, this.requiredSkillPropertyName),
      optional_skills: this.getFormSkills(this.jobOptionalSkillsForm, this.optionalSkillPropertyName),
      questions: this.surveyForJobEdit.questions,
      company: this.companyId,
      is_cover_letter_required: this.jobCoverLetterForm.value.is_cover_letter_required,
    };
  }

  private getJobPreviewData(): object {
    const skills = {
      required_skills: this.jobRequiredSkillsForm.value.required_skills,
      optional_skills: this.jobOptionalSkillsForm.value.optional_skills,
    };

    const locationData = {
      location: this.addressForm.value
    };
    return Object.assign(this.getJobData(this.jobPublishDateForm, false, this.jobStatusForm), skills, locationData);
  }

  private postJob(data: object) {
    return this.store.dispatch(new EditJobPageActions.UpdateJob(this.jobId, data));
  }
}
