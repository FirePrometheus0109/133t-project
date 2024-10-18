import {Component, Input, NgModule, OnDestroy, OnInit} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {Select, Store} from '@ngxs/store';
import {Observable} from 'rxjs';
import * as CoreActions from '../../core/actions/core.actions';
import {CoreState} from '../../core/states/core.state';
import {InputLengths} from '../../shared/constants/validators/input-length';
import {SnackBarMessageType} from '../../shared/models/snack-bar-message';
import {UtilsService} from '../../shared/services/utils.service';
import {ValidationService} from '../../shared/services/validation.service';
import {SurveyListActions} from '../../survey/actions';
import {SurveyState} from '../../survey/states/survey.state';
import {CreateJobPageActions} from '../actions';
import {CreateJobPageState} from '../states/create-job-page.state';
import {BaseJobPage} from './base-job-page';


@Component({
  selector: 'app-create-job-page',
  template: `
      <mat-horizontal-stepper linear="true" #stepper class="stepper-main">
          <mat-step [stepControl]="industryFormGroup">
              <ng-template matStepLabel>Fill your industry</ng-template>
              <app-industry-select-form
                      [pending]="pending$ | async"
                      [errors]="errors$ | async"
                      [form]="industryFormGroup">
                  <ng-container ngProjectAs="body">
                      <div>
                          <button mat-raised-button color="primary" matStepperNext>
                              Proceed
                              <mat-icon matSuffix>navigate_next</mat-icon>
                          </button>
                          <button mat-button (click)="stepper.reset()">Cancel</button>
                      </div>
                  </ng-container>
              </app-industry-select-form>
          </mat-step>

          <mat-step [stepControl]="addressForm">
              <ng-template matStepLabel>Job Title/Location</ng-template>
              <mat-card>
                  <mat-card-content>
                      <form [formGroup]="addressForm">
                          <mat-form-field>
                              <input matInput formControlName="title" placeholder="Title" required>
                          </mat-form-field>
                          <app-address-component [form]="addressForm" [initialData]="{}"></app-address-component>
                      </form>
                  </mat-card-content>
                  <div>
                      <button mat-raised-button color="primary" matStepperPrevious>
                          <mat-icon matSuffix>navigate_before</mat-icon>
                          Back
                      </button>
                      <button mat-raised-button color="primary" matStepperNext>
                          Proceed
                          <mat-icon matSuffix>navigate_next</mat-icon>
                      </button>
                      <button mat-button (click)="stepper.reset()">Cancel</button>
                  </div>
              </mat-card>
          </mat-step>

          <mat-step [stepControl]="profileDetailsForm">
              <ng-template matStepLabel>Job Details</ng-template>
              <app-profile-details-ext-form [pending]="pending$ | async" [errors]="errors$ | async"
                                            [form]="profileDetailsForm">
                  <ng-container ngProjectAs="body">
                      <div>
                          <button mat-raised-button color="primary" matStepperPrevious>
                              <mat-icon matSuffix>navigate_before</mat-icon>
                              Back
                          </button>
                          <button mat-raised-button color="primary" matStepperNext>
                              Proceed
                              <mat-icon matSuffix>navigate_next</mat-icon>
                          </button>
                          <button mat-button (click)="stepper.reset()">Cancel</button>
                      </div>
                  </ng-container>
              </app-profile-details-ext-form>
          </mat-step>

          <mat-step [stepControl]="descriptionFormGroup">
              <ng-template matStepLabel>Description</ng-template>
              <mat-card>
                  <mat-card-content>
                      <form [formGroup]="descriptionFormGroup">
                          <mat-form-field>
                <textarea matInput formControlName="description" cdkTextareaAutosize placeholder="Description"
                          #autosize="cdkTextareaAutosize"
                          cdkAutosizeMinRows="10"
                          cdkAutosizeMaxRows="20"
                          required></textarea>
                          </mat-form-field>
                      </form>
                  </mat-card-content>
                  <div>
                      <button mat-raised-button color="primary" matStepperPrevious>
                          <mat-icon matSuffix>navigate_before</mat-icon>
                          Back
                      </button>
                      <button mat-raised-button color="primary" matStepperNext>
                          Proceed
                          <mat-icon matSuffix>navigate_next</mat-icon>
                      </button>
                      <button mat-button (click)="stepper.reset()">Cancel</button>
                  </div>
              </mat-card>
          </mat-step>

          <mat-step [stepControl]="mustHaveSkillsForm">
              <ng-template matStepLabel>Must Have Skills</ng-template>
              <app-skills-select-component [form]="mustHaveSkillsForm" [skillPropertyName]="'skills'"
                                           [excludedSkills]="niceToHaveSkillsForm.value['skills']">
                  <ng-container ngProjectAs="body">
                      <div>
                          <button mat-raised-button color="primary" matStepperPrevious>
                              <mat-icon matSuffix>navigate_before</mat-icon>
                              Back
                          </button>
                          <button mat-raised-button color="primary" matStepperNext>
                              Proceed
                              <mat-icon matSuffix>navigate_next</mat-icon>
                          </button>
                          <button mat-button (click)="stepper.reset()">Cancel</button>
                      </div>
                  </ng-container>
              </app-skills-select-component>
          </mat-step>

          <mat-step [stepControl]="minimalSkillPercent">

              <ng-template matStepLabel>Matching Controls</ng-template>
              <h4>Auto Apply Skill Matching Controls</h4>
              <p class="toggler-description">
                  Set your desired skill matching for Auto Apply:
              </p>

              <div class="supportive-wrapper">
                  <mat-button-toggle-group #group="matButtonToggleGroup" [(ngModel)]="minimalSkillPercent" value="0">
                      <mat-button-toggle value="0" ngDefaultControl>
                          <p>0%</p>
                      </mat-button-toggle>
                      <mat-button-toggle value="25" ngDefaultControl>
                          <p>25%</p>
                      </mat-button-toggle>
                      <mat-button-toggle value="50" ngDefaultControl>
                          <p>50%</p>
                      </mat-button-toggle>
                      <mat-button-toggle value="75" ngDefaultControl>
                          <p>75%</p>
                      </mat-button-toggle>
                      <mat-button-toggle value="100" ngDefaultControl>
                          <p>100%</p>
                      </mat-button-toggle>
                  </mat-button-toggle-group>

                  <button mat-icon-button color="accent"
                          matTooltipClass="jsp-profile-validation-tooltip"
                          [matTooltip]="'Using the slider brings more flexibility to your open roles via Auto Apply'">
                      <mat-icon>info</mat-icon>
                  </button>
              </div>

              <div class="manual-apply">
                  <h4>Manual Job Board Skill Match Controls</h4>
                  <mat-checkbox [(ngModel)]="manual_apply_strict_required_skills_matching">
                      Set Open Role Skill Match at 100%
                  </mat-checkbox>
                  <button mat-icon-button color="accent"
                          matTooltipClass="jsp-profile-validation-tooltip"
                          [matTooltip]="'Using this setting will match all open role skills at 100% via the manual job board.'">
                      <mat-icon>info</mat-icon>
                  </button>
              </div>

              <ng-container ngProjectAs="body">
                  <div>
                      <button mat-raised-button color="primary" matStepperPrevious>
                          <mat-icon matSuffix>navigate_before</mat-icon>
                          Back
                      </button>
                      <button mat-raised-button color="primary" matStepperNext>
                          Proceed
                          <mat-icon matSuffix>navigate_next</mat-icon>
                      </button>
                      <button mat-button (click)="stepper.reset()">Cancel</button>
                  </div>
              </ng-container>
          </mat-step>
          
          <mat-step [stepControl]="niceToHaveSkillsForm">
              <ng-template matStepLabel>Nice To Have Skills</ng-template>
              <app-skills-select-component [form]="niceToHaveSkillsForm" [skillPropertyName]="'skills'"
                                           [excludedSkills]="mustHaveSkillsForm.value['skills']">
                  <ng-container ngProjectAs="body">
                      <div>
                          <button mat-raised-button color="primary" matStepperPrevious>
                              <mat-icon matSuffix>navigate_before</mat-icon>
                              Back
                          </button>
                          <button mat-raised-button color="primary" matStepperNext>
                              Proceed
                              <mat-icon matSuffix>navigate_next</mat-icon>
                          </button>
                          <button mat-button (click)="stepper.reset()">Cancel</button>
                      </div>
                  </ng-container>
              </app-skills-select-component>
          </mat-step>

          <mat-step [stepControl]="surveyForm">
              <ng-template matStepLabel>Questionnaire</ng-template>
              <mat-card>
                  <mat-card-title class="questionnaire-title" align="center">
                      <h3>Questionnaire</h3>
                      <span>Up to 10 questions</span>
                  </mat-card-title>
                  <mat-card-content align="center">
                      <app-survey-edit-container></app-survey-edit-container>
                  </mat-card-content>
                  <div>
                      <button mat-raised-button color="primary" matStepperPrevious>
                          <mat-icon matSuffix>navigate_before</mat-icon>
                          Back
                      </button>
                      <button mat-raised-button color="primary" matStepperNext>
                          Proceed
                          <mat-icon matSuffix>navigate_next</mat-icon>
                      </button>
                      <button mat-button (click)="stepper.reset()">Cancel</button>
                  </div>
              </mat-card>
          </mat-step>

          <ng-template [ngxPermissionsOnly]="['set_job_is_cover_letter_required']">
              <mat-step [stepControl]="coverLetterForm">
                  <ng-template matStepLabel>Cover Letter</ng-template>
                  <mat-card>
                      <mat-card-content align="center">
                          <app-job-cover-letter-required-form [form]="coverLetterForm">
                          </app-job-cover-letter-required-form>
                      </mat-card-content>
                      <div>
                          <button mat-raised-button color="primary" matStepperPrevious>
                              <mat-icon matSuffix>navigate_before</mat-icon>
                              Back
                          </button>
                          <button mat-raised-button color="primary" matStepperNext>
                              Proceed
                              <mat-icon matSuffix>navigate_next</mat-icon>
                          </button>
                          <button mat-button (click)="stepper.reset()">Cancel</button>
                      </div>
                  </mat-card>
              </mat-step>
          </ng-template>

          <mat-step>
              <ng-template matStepLabel>Save</ng-template>
              <app-job-date-form [form]="publishDateForm" [pending]="pending$ | async" [errors]="errors$ | async">
              </app-job-date-form>
              <div class="save-block">
                  <button mat-button matStepperPrevious>Back</button>
                  <button mat-raised-button color="primary" (click)="saveJob()">
                      Save
                      <mat-icon matSuffix>save</mat-icon>
                  </button>
                  <button mat-raised-button color="primary" (click)="saveAndPublishJob()">
                      Save and publish
                      <mat-icon matSuffix>save</mat-icon>
                  </button>
                  <button mat-button (click)="stepper.reset()">Cancel</button>
              </div>
          </mat-step>

      </mat-horizontal-stepper>
  `,
  styles: [`
      :host {
          display: flex;
          justify-content: center;
          margin: 72px 0;
      }

      h4 {
          font-weight: 900;
          margin-top: 20px;
          margin-bottom: 20px;
          margin-top: 0;
      }

      .toggler-description {
          margin-top: 20px;
      }

      .mat-button-toggle-label-content {
          line-height: 15px !important;
      }

      .supportive-wrapper {
          display: flex;
          flex-direction: row;
          align-items: center;
          margin: 20px 0 40px;
      }
      
      .manual-apply {
          margin-top: 30px;
          margin-bottom: 30px;
      }

      .mat-button-toggle-group {
          border-radius: 25px;
      }

      .mat-button-toggle {
          background: rgba(0, 0, 0, 0.87);
          color: #fff;
          width: 64px;
      }

      .mat-button-toggle-checked {
          background: red;
      }

      .mat-button-toggle:first-child {
          border-radius: 25px 0 0 25px;
      }

      .mat-button-toggle:last-child {
          border-radius: 0 25px 25px 0;
      }

      .mat-form-field {
          width: 100%;
          min-width: 300px;
      }

      mat-card-title,
      mat-card-content {
          display: flex;
          justify-content: center;
      }

      .questionnaire-title {
          flex-direction: column;
      }

      .save-block {
          margin-top: 25px;
      }
  `],
})
export class CreateJobPageComponent extends BaseJobPage implements OnInit, OnDestroy {
  @Select(CreateJobPageState.pending) pending$: Observable<boolean>;
  @Select(CreateJobPageState.errors) errors$: Observable<any>;
  @Select(CoreState.countries) countries$: Observable<object[]>;

  private skillPropertyName = 'skills';

  public industryFormGroup: FormGroup = new FormGroup({
    industry: new FormControl('', Validators.compose([Validators.required, ValidationService.selectListObjectValidator]))
  });

  public addressForm = new FormGroup({
    title: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    city: new FormControl('', Validators.required),
    country: new FormControl('', Validators.required),
    zip: new FormControl('', Validators.maxLength(InputLengths.zip))
  }, ValidationService.addressValidator);

  public profileDetailsForm: FormGroup = new FormGroup({
    position_type: new FormControl('', Validators.required),
    education: new FormControl(''),
    education_strict: new FormControl(false),
    experience: new FormControl(''),
    travel: new FormControl(''),
    salary_min: new FormControl('', ValidationService.numericValidator),
    salary_max: new FormControl('', ValidationService.numericValidator),
    salary_negotiable: new FormControl(false),
    clearance: new FormControl(''),
    benefits: new FormControl(''),
  }, ValidationService.educationValidator);

  public descriptionFormGroup: FormGroup = new FormGroup({
    description: new FormControl('',
      Validators.compose([Validators.required, Validators.maxLength(InputLengths.jobDescription)])),
  });

  public minimalSkillPercent: string = '0';

  public manual_apply_strict_required_skills_matching = false;

  public mustHaveSkillsForm: FormGroup = new FormGroup({
    skills: new FormControl([]),
  });

  public niceToHaveSkillsForm: FormGroup = new FormGroup({
    skills: new FormControl([]),
  });

  public publishDateForm: FormGroup = new FormGroup({
    publish_date: new FormControl(''),
    closing_date: new FormControl(''),
  }, ValidationService.jobDateValidator);

  public surveyForm: FormGroup = new FormGroup({
    questions: new FormControl(''),
  });

  public coverLetterForm: FormGroup = new FormGroup({
    is_cover_letter_required: new FormControl(false),
  });

  constructor(private store: Store) {
    super();
  }

  ngOnInit() {
    this.store.dispatch(new SurveyListActions.SetJobEditMode(true));
    const defaultCountry = this.store.selectSnapshot(CoreState.defaultCountry);
    this.addressForm.controls.country.setValue(defaultCountry);
  }

  ngOnDestroy() {
    this.store.dispatch(new SurveyListActions.SetJobEditMode(false));
    this.store.dispatch(new SurveyListActions.SetModalMode(false));
    this.store.dispatch(new SurveyListActions.SetCurrentSurvey(null));
    this.store.dispatch(new SurveyListActions.UpdateSurveyForJobEdit([]));
  }

  public saveAndPublishJob(): Observable<any> {
    const formDate = this.publishDateForm.value.publish_date;
    const message = (formDate)
      ? `Job posting will be published on ${formDate.format('L')} date`
      : 'Job posting published successfully';
    return this.postJobData(message, true);
  }

  public saveJob(): void {
    const message = 'Job posting saved successfully';
    this.postJobData(message);
    this.store.dispatch(new SurveyListActions.SetJobEditMode(false));
  }

  public getBaseJobData(): object {
    return {
      industry: this.industryFormGroup.value.industry.id,
      title: this.addressForm.value.title,
      location: UtilsService.prepareAddressData(this.addressForm.value),
      position_type: this.profileDetailsForm.value.position_type,
      education: this.profileDetailsForm.value.education,
      education_strict: Boolean(this.profileDetailsForm.value.education_strict),
      experience: this.profileDetailsForm.value.experience,
      travel: this.profileDetailsForm.value.travel,
      salary_min: this.profileDetailsForm.value.salary_min ? this.profileDetailsForm.value.salary_min : null,
      salary_max: this.profileDetailsForm.value.salary_max ? this.profileDetailsForm.value.salary_max : null,
      salary_negotiable: Boolean(this.profileDetailsForm.value.salary_negotiable),
      clearance: this.profileDetailsForm.value.clearance,
      benefits: this.profileDetailsForm.value.benefits,
      description: this.descriptionFormGroup.value.description,
      required_skills: this.getFormSkills(this.mustHaveSkillsForm, this.skillPropertyName),
      optional_skills: this.getFormSkills(this.niceToHaveSkillsForm, this.skillPropertyName),
      questions: this.store.selectSnapshot(SurveyState.surveyForJobEdit).questions,
      is_cover_letter_required: Boolean(this.coverLetterForm.value.is_cover_letter_required),
      autoapply_minimal_percent: Number(this.minimalSkillPercent),
      manual_apply_strict_required_skills_matching: this.manual_apply_strict_required_skills_matching,
    };
  }

  private postJobData(successPostMessage: string, isPublish: boolean = false): Observable<any> {
    const data = this.getJobData(this.publishDateForm, isPublish);
    if (data['publish_date']) {
      if (!this.isJobValidForPublish(data)) {
        return this.store.dispatch(new CoreActions.SnackbarOpen({
          message: this.getPublishJobRequiredFieldsErrorMessage,
          type: SnackBarMessageType.ERROR,
          delay: 10000,
        }));
      }
    }
    return this.store.dispatch(new CreateJobPageActions.CreateNewJob(data, successPostMessage));
  }

  private updateValidation(control: AbstractControl, validators) {
    control.setValidators(validators);
    control.updateValueAndValidity();
    validators ? control.enable() : control.disable();
  }
}
