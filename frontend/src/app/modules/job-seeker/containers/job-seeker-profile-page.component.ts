import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { CoreState } from '../../core/states/core.state';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { JobSeekerProfileSectionsEnum } from '../../shared/enums/job-seeker-profile.enums';
import { Address } from '../../shared/models/address.model';
import { CoverLetterItem } from '../../shared/models/cover-letter.model';
import { EducationMode, EducationType } from '../../shared/models/education.model';
import { Enums } from '../../shared/models/enums.model';
import { ExperienceMode } from '../../shared/models/experience.model';
import { Photo } from '../../shared/models/photo.model';
import { SkillItem } from '../../shared/models/skill.model';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { UtilsService } from '../../shared/services/utils.service';
import { ValidationService } from '../../shared/services/validation.service';
import { JobSeekerProfilePageActions } from '../actions';
import { JobSeekerProfile } from '../models';
import { JobSeekerService } from '../services/job-seeker.service';
import { JSPPageState } from '../states/jsp-page.state';
import { JobSeekerProfilePageViewComponent } from './job-seeker-profile-page-view.component';


@Component({
  selector: 'app-job-seeker-profile-page',
  template: `
    <mat-accordion class="removed-from-print" [hideToggle]="true" [multi]="true">
      <mat-expansion-panel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>General</mat-panel-title>
        </mat-expansion-panel-header>
        <mat-card>
          <mat-grid-list cols="3">
            <h2 class="example-h2">Progress</h2>
            <mat-grid-tile [style.border-right]="'1px dashed #ddd'">
              <app-profile-completion-view [profileCompletion]="(initialData$ | async)?.profile_completion">
              </app-profile-completion-view>
            </mat-grid-tile>
            <mat-grid-tile [style.border-right]="'1px dashed #ddd'">
              <img mat-card-avatar class="big-avatar" [src]="(photoProfile$ | async)?.original">
              <app-material-file-upload (complete)="onFileComplete($event)"
                                        (deleteFile)="onImageDelete()"
                                        [target]="targetFilesUpload"
                                        [isImageUploaded]="photoProfile$ | async"
                                        param="photo">
              </app-material-file-upload>
            </mat-grid-tile>
            <mat-grid-tile>
              <div class="button-section">
                <app-jsp-publish-profile [isProfilePublic]="(currentJspObject$ | async)?.is_public"
                                        [isProfileCanBePublic]="(currentJspObject$ | async)?.isProfileCanBePublic"
                                        [publishHideProfileTooltipText]="publishHideProfileTooltipText$ | async"
                                        (toggleProfileStatus)="onPublishHideProfile($event)">
                </app-jsp-publish-profile>
                <div>
                  <button mat-raised-button
                          color="primary"
                          (click)="providePreviewProfile()">
                    Preview profile
                    <mat-icon matSuffix>account_box</mat-icon>
                  </button>
                  <mat-icon mat-raised-button [matTooltip]="previewProfileText" matSuffix>
                    help
                  </mat-icon>
                </div>
                <app-jsp-print-control
                  [pending]="pending$ | async">
                </app-jsp-print-control>
                <app-jsp-share-link-access-control
                    [profileIsPublic]="(currentJspObject$ | async)?.is_public"
                    [profileIsSharing]="(currentJspObject$ | async)?.is_shared"
                    [uid]="(initialData$ | async)?.guid"
                    (sharingToggleClicked)="toggleSharing($event)">
                </app-jsp-share-link-access-control>
                <mat-error *ngIf="!(currentJspObject$ | async)?.is_public">Current status: Hidden</mat-error>
              </div>
            </mat-grid-tile>
          </mat-grid-list>
        </mat-card>
      </mat-expansion-panel>

      <mat-expansion-panel #mainInfoSection [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Main info</mat-panel-title>
        </mat-expansion-panel-header>
        <app-jsp-main-info-form *ngIf="mainInfoSectionEditMode$ | async"
                                (submittedChanges)="onSubmitMainInfo($event)"
                                [pending]="pending$ | async"
                                [errors]="errors$ | async"
                                [form]="mainInfoForm"
                                [initialData]="(initialData$ | async)?.user"
                                [phoneNumber]="(initialData$ | async)?.phone">
          <mat-action-row>
            <button type="button" mat-raised-button color="primary"
                    (click)="closeFormSection(JobSeekerProfileSectionsEnum.MAIN_INFO_SECTION_EDIT_MODE)">
              Close
              <mat-icon matSuffix>close</mat-icon>
            </button>
            <button type="submit" mat-raised-button color="primary" [disabled]="!mainInfoForm.valid">
              Save
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </app-jsp-main-info-form>
        <app-jsp-main-info-view *ngIf="!(mainInfoSectionEditMode$ | async)"
                                [initialData]="(initialData$ | async)?.user"
                                [phoneNumber]="(initialData$ | async)?.phone"
                                (changeToEditMode)="setMainInfoEditMode($event)">
        </app-jsp-main-info-view>
      </mat-expansion-panel>

      <mat-expansion-panel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Address</mat-panel-title>
        </mat-expansion-panel-header>
        <app-address-component *ngIf="addressSectionEditMode$ | async"
                              (submitted)="onSubmitAddress($event)"
                              [pending]="pending$ | async"
                              [errors]="errors$ | async"
                              [form]="addressForm"
                              [initialData]="(initialData$ | async)?.address">
          <mat-action-row>
            <button type="button" mat-raised-button color="primary"
                    (click)="closeFormSection(JobSeekerProfileSectionsEnum.ADDRESS_SECTION_EDIT_MODE)">
              Close
              <mat-icon matSuffix>close</mat-icon>
            </button>
            <button type="submit" mat-raised-button color="primary" [disabled]="!addressForm.valid">
              Save
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </app-address-component>
        <app-jsp-address-view *ngIf="!(addressSectionEditMode$ | async)"
                              [initialData]="(initialData$ | async)?.address"
                              (changeToEditMode)="setAddressEditMode($event)">
        </app-jsp-address-view>
      </mat-expansion-panel>

      <mat-expansion-panel #aboutSection [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>About</mat-panel-title>
        </mat-expansion-panel-header>
        <app-jsp-about-form *ngIf="aboutSectionEditMode$ | async"
                            (submitted)="onSubmitAbout($event)"
                            [initialData]="(initialData$ | async)"
                            [pending]="pending$ | async"
                            [errors]="errors$ | async"
                            [form]="aboutForm">
          <mat-action-row>
            <button type="button" mat-raised-button color="primary"
                    (click)="closeFormSection(JobSeekerProfileSectionsEnum.ABOUT_SECTION_EDIT_MODE)">
              Close
              <mat-icon matSuffix>close</mat-icon>
            </button>
            <button type="submit" mat-raised-button color="primary" [disabled]="aboutForm.invalid">
              Save
              <mat-icon matSuffix>save</mat-icon>
            </button>
          </mat-action-row>
        </app-jsp-about-form>
        <app-jsp-about-view *ngIf="!(aboutSectionEditMode$ | async)"
                            [initialData]="(initialData$ | async)?.about"
                            (changeToEditMode)="setAboutEditMode($event)">
        </app-jsp-about-view>
      </mat-expansion-panel>

      <mat-expansion-panel #profileDetailsSection [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Profile Details</mat-panel-title>
        </mat-expansion-panel-header>
        <app-profile-details-form *ngIf="profileDetailsSectionEditMode$ | async"
                                  (submitted)="onSubmitProfileDetails($event)"
                                  [pending]="pending$ | async"
                                  [errors]="errors$ | async"
                                  [initialData]="initialData$ | async"
                                  [form]="profileDetailsForm">
          <ng-container ngProjectAs="title">
            <h4>Profile details</h4>
          </ng-container>
          <ng-container ngProjectAs="body">
            <mat-action-row>
              <button type="button" mat-raised-button color="primary"
                      (click)="closeFormSection(JobSeekerProfileSectionsEnum.PROFILE_DETAILS_SECTION_EDIT_MODE)">
                Close
                <mat-icon matSuffix>close</mat-icon>
              </button>
              <button type="submit" mat-raised-button color="primary" [disabled]="!profileDetailsForm.valid">
                Save
                <mat-icon matSuffix>save</mat-icon>
              </button>
            </mat-action-row>
          </ng-container>
        </app-profile-details-form>
        <app-jsp-profile-details-view *ngIf="!(profileDetailsSectionEditMode$ | async)"
                                      [enums]="enums$ | async"
                                      [initialData]="(initialData$ | async)"
                                      (changeToEditMode)="setProfileDetailsEditMode($event)">
        </app-jsp-profile-details-view>
      </mat-expansion-panel>

      <mat-expansion-panel #skillsPanel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Skills</mat-panel-title>
        </mat-expansion-panel-header>
        <app-skills-select-component *ngIf="skillsSectionEditMode$ | async"
                                    (submitted)="onSubmitSkills($event)"
                                    [pending]="pending$ | async"
                                    [errors]="errors$ | async"
                                    [form]="skillsForm"
                                    [initialData]="initialData$ | async"
                                    [skillPropertyName]="'skills'">
          <ng-container ngProjectAs="title">
            <span>Add new skills...</span>
          </ng-container>
          <ng-container ngProjectAs="body">
            <mat-action-row>
              <button type="button" mat-raised-button color="primary"
                      (click)="closeFormSection(JobSeekerProfileSectionsEnum.SKILLS_SECTION_EDIT_MODE)">
                Close
                <mat-icon matSuffix>close</mat-icon>
              </button>
              <button type="submit" mat-raised-button color="primary" [disabled]="!skillsForm.valid">
                Save
                <mat-icon matSuffix>save</mat-icon>
              </button>
            </mat-action-row>
          </ng-container>
        </app-skills-select-component>
        <app-jsp-skills-view *ngIf="!(skillsSectionEditMode$ | async)"
                            [initialData]="(initialData$ | async)?.skills"
                            (changeToEditMode)="setSkillsEditMode($event)">
        </app-jsp-skills-view>
      </mat-expansion-panel>

      <mat-expansion-panel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Education</mat-panel-title>
        </mat-expansion-panel-header>
        <button type="button" mat-raised-button color="primary" *ngIf="(educationMode$ | async) === EducationMode.VIEW"
                (click)="addNewEducation()" [disabled]="isEducationMaxCount()">
          Add new Education
          <mat-icon matSuffix>add</mat-icon>
        </button>
        <button type="button" mat-raised-button color="primary" *ngIf="(educationMode$ | async) === EducationMode.VIEW"
                (click)="addNewCertification()" [disabled]="isEducationMaxCount()">
          Add new Certification
          <mat-icon matSuffix>add</mat-icon>
        </button>
        <app-jsp-education-form
            (submitted)="onSubmitEducation($event)"
            (closeForm)="closeForm()"
            *ngIf="((educationType$ | async) === EducationType.EDUCATION) && ((educationMode$ | async) !== EducationMode.VIEW)"
            [pending]="pending$ | async"
            [errors]="errors$ | async"
            [form]="educationForm"></app-jsp-education-form>
        <app-jsp-certification-form
            (submitted)="onSubmitCertification($event)"
            (closeForm)="closeForm()"
            *ngIf="((educationType$ | async) === EducationType.CERTIFICATION) && ((educationMode$ | async) !== EducationMode.VIEW)"
            [pending]="pending$ | async"
            [errors]="errors$ | async"
            [form]="certificationForm">
        </app-jsp-certification-form>
        <app-jsp-education-list-form [initialData]="educationAndCertificationData$ | async"
                                    [enums]="enums$ | async"
                                    (editEducationItem)="onEditEducation($event)"
                                    (editCertificationItem)="onEditCertification($event)"
                                    (deletedEducationItem)="deleteEducationItem($event)"
                                    (deletedCertificationItem)="deleteCertificationItem($event)">
        </app-jsp-education-list-form>
      </mat-expansion-panel>

      <mat-expansion-panel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Experience</mat-panel-title>
        </mat-expansion-panel-header>
        <button type="button" mat-raised-button color="primary"
                *ngIf="(experienceMode$ | async) === ExperienceMode.VIEW"
                [disabled]="(experienceCount$ | async) === environment.maxExperienceCount"
                (click)="addNewJob()">
          Add new Job
          <mat-icon matSuffix>add</mat-icon>
        </button>
        <app-jsp-experience-form
            (submitted)="onSubmitExperience($event)"
            (closeForm)="closeExperienceForm()"
            *ngIf="(experienceMode$ | async) !== ExperienceMode.VIEW"
            [enums]="enums$ | async"
            [pending]="pending$ | async"
            [errors]="errors$ | async"
            [form]="experienceForm">
        </app-jsp-experience-form>
        <app-jsp-experience-list-form [initialData]="experience$ | async"
                                      [enums]="enums$ | async"
                                      (editJobItem)="onEditExperience($event)"
                                      (deletedJobItem)="deleteExperienceItem($event)">
        </app-jsp-experience-list-form>
      </mat-expansion-panel>

      <mat-expansion-panel [expanded]="true" [disabled]="true">
        <mat-expansion-panel-header>
          <mat-panel-title>Cover Letter</mat-panel-title>
        </mat-expansion-panel-header>
        <app-js-manage-cover-letters></app-js-manage-cover-letters>
      </mat-expansion-panel>
    </mat-accordion>
    <router-outlet name="print"></router-outlet>
  `,
  styles: [`
    :host > div {
      display: flex;
      justify-content: center;
    }

    mat-accordion {
      width: 100%;
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

    .mat-card-avatar.big-avatar {
      object-fit: cover;
      height: 200px;
      width: 200px;
    }

    h4 {
      margin-top: 10px;
      margin-bottom: 10px;
    }
  `],
})
export class JobSeekerProfilePageComponent implements OnInit {
  @Select(JSPPageState.pending) pending$: Observable<boolean>;
  @Select(JSPPageState.errors) errors$: Observable<any>;
  @Select(JSPPageState.initialData) initialData$: Observable<JobSeekerProfile>;
  @Select(JSPPageState.educationAndCertificationData) educationAndCertificationData$: Observable<any>;
  @Select(JSPPageState.educationMode) educationMode$: Observable<any>;
  @Select(JSPPageState.educationType) educationType$: Observable<any>;
  @Select(JSPPageState.experience) experience$: Observable<any>;
  @Select(JSPPageState.experienceCount) experienceCount$: Observable<number>;
  @Select(JSPPageState.experienceMode) experienceMode$: Observable<any>;
  @Select(JSPPageState.coverLetter) coverLetter$: Observable<Array<CoverLetterItem>>;
  @Select(JSPPageState.coverLetterMode) coverLetterMode$: Observable<string>;
  @Select(JSPPageState.defaultCoverLetter) defaultCoverLetter$: Observable<any>;
  @Select(JSPPageState.Photo) photoProfile$: Observable<Photo>;
  @Select(JSPPageState.publishHideProfileTooltipText) publishHideProfileTooltipText$: Observable<string>;
  @Select(JSPPageState.currentJspObject) currentJspObject$: Observable<JobSeekerProfile>;
  @Select(JSPPageState.mainInfoSectionEditMode) mainInfoSectionEditMode$: Observable<boolean>;
  @Select(JSPPageState.addressSectionEditMode) addressSectionEditMode$: Observable<boolean>;
  @Select(JSPPageState.aboutSectionEditMode) aboutSectionEditMode$: Observable<boolean>;
  @Select(JSPPageState.profileDetailsSectionEditMode) profileDetailsSectionEditMode$: Observable<boolean>;
  @Select(JSPPageState.skillsSectionEditMode) skillsSectionEditMode$: Observable<boolean>;
  @Select(CoreState.enums) enums$: Observable<Enums>;

  public environment = environment;
  public profileData: JobSeekerProfile;
  public EducationMode = EducationMode;
  public ExperienceMode = ExperienceMode;
  public EducationType = EducationType;
  public JobSeekerProfileSectionsEnum = JobSeekerProfileSectionsEnum;
  public previewProfileText = `In preview mode you will see your profile the same way other users see it.`;

  private jsId: number;
  private submitSkillsMessage = 'You are saving your profile without fields that are required for publishing your' +
    ' profile: skills.\nDo you want to save profile in Hidden mode?';
  private submitSkillsConfirmButtonText = 'Save';

  mainInfoForm: FormGroup = new FormGroup({
    first_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    last_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    email: new FormControl('', Validators.compose([Validators.required, ValidationService.emailValidator])),
    phone: new FormControl(''),
  });

  addressForm: FormGroup = new FormGroup({
    city: new FormControl(''),
    country: new FormControl(''),
    zip: new FormControl('', Validators.maxLength(InputLengths.zip)),
    address: new FormControl(''),
  }, ValidationService.addressValidator);

  aboutForm: FormGroup = new FormGroup({
    about: new FormControl('', Validators.maxLength(InputLengths.about)),
  });

  profileDetailsForm: FormGroup = new FormGroup({
    position_type: new FormControl(''),
    education: new FormControl(''),
    experience: new FormControl(''),
    travel: new FormControl(''),
    salary_min: new FormControl('',
      Validators.compose([ValidationService.numericValidator, Validators.maxLength(InputLengths.salary)])),
    salary_max: new FormControl('',
      Validators.compose([ValidationService.numericValidator, Validators.maxLength(InputLengths.salary)])),
    salary_negotiable: new FormControl(false),
    clearance: new FormControl(''),
    benefits: new FormControl(''),
  }, ValidationService.salaryValidator);

  skillsForm: FormGroup = new FormGroup({
    skills: new FormControl([]),
  });

  educationForm: FormGroup = new FormGroup({
    institution: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    field_of_study: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    degree: new FormControl('', Validators.required),
    date_from: new FormControl('', Validators.required),
    date_to: new FormControl(''),
    location: new FormControl('', Validators.maxLength(InputLengths.location)),
    description: new FormControl('', Validators.maxLength(InputLengths.descriptions)),
    is_current: new FormControl(false),
  }, ValidationService.isCurrentAndDateToValidator);

  certificationForm: FormGroup = new FormGroup({
    institution: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    field_of_study: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    graduated: new FormControl(''),
    licence_number: new FormControl('', Validators.maxLength(InputLengths.licenceNumber)),
    location: new FormControl('', Validators.maxLength(InputLengths.location)),
    description: new FormControl('', Validators.maxLength(InputLengths.descriptions)),
    is_current: new FormControl(false),
  });

  experienceForm: FormGroup = new FormGroup({
    company: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    job_title: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    description: new FormControl('', Validators.maxLength(InputLengths.descriptions)),
    date_from: new FormControl('', Validators.required),
    date_to: new FormControl(''),
    is_current: new FormControl(false),
    employment: new FormControl('', Validators.required),
  }, ValidationService.isCurrentAndDateToValidator);

  targetFilesUpload: string;

  constructor(private store: Store,
              private route: ActivatedRoute,
              private jSService: JobSeekerService,
              private dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  ngOnInit() {
    this.profileData = this.route.snapshot.data.profileData;
    this.jsId = this.route.snapshot.params['id'];
    this.targetFilesUpload = this.jSService.getJobSeekerPhotoRoute(this.jsId);
    this.store.dispatch(new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.ADDRESS_SECTION_EDIT_MODE, true));
  }

  setMainInfoEditMode(value: boolean) {
    this.store.dispatch(new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.MAIN_INFO_SECTION_EDIT_MODE, value));
  }

  setAddressEditMode(value: boolean) {
    this.store.dispatch(new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.ADDRESS_SECTION_EDIT_MODE, value));
  }

  setAboutEditMode(value: boolean) {
    this.store.dispatch(new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.ABOUT_SECTION_EDIT_MODE, value));
  }

  setProfileDetailsEditMode(value: boolean) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.PROFILE_DETAILS_SECTION_EDIT_MODE, value)
    );
  }

  setSkillsEditMode(value: boolean) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.SetJSPSectionMode(JobSeekerProfileSectionsEnum.SKILLS_SECTION_EDIT_MODE, value)
    );
  }

  public onPublishHideProfile(flag: boolean) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('user', this.jsId, {is_public: flag}),
    );
  }

  toggleSharing(flag: boolean) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('user', this.jsId, {is_shared: flag})
    );
  }

  onFileComplete(data: any) {
    this.store.dispatch(new JobSeekerProfilePageActions.UpdatePhoto(this.jsId, data['photo']));
  }

  onImageDelete() {
    this.store.dispatch(new JobSeekerProfilePageActions.UpdatePhoto(this.jsId, null));
    this.store.dispatch(
      new JobSeekerProfilePageActions.DeleteProfileImage(this.jsId),
    );
  }

  onSubmitAddress(formData: Address) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('address', this.jsId, {address: UtilsService.prepareAddressData(formData)})
    );
    this.setAddressEditMode(false);
  }

  onSubmitMainInfo(formData: any) {
    const postData = this.modifyDataWithPhoneNumber(formData);
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('user', this.jsId, postData),
    );
    this.setMainInfoEditMode(false);
  }

  onSubmitAbout(formData: any) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('', this.jsId, formData),
    );
    this.setAboutEditMode(false);
  }

  onSubmitProfileDetails(formData: any) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('', this.jsId, UtilsService.prepareSalaryData(formData)),
    );
    this.setProfileDetailsEditMode(false);
  }

  onSubmitSkills(formData: any) {
    const skills: SkillItem[] = formData['skills'];
    if (skills.length < environment.jspMinPublishSkillsCount) {
      this.confirmationDialogService.openConfirmationDialog({
        message: `${this.submitSkillsMessage}`,
        callback: this.submitSkills.bind(this),
        arg: skills,
        confirmationText: `${this.submitSkillsConfirmButtonText}`,
      });
    } else {
      this.submitSkills(skills);
    }
  }

  submitSkills(skills: SkillItem[]) {
    const skillIds: Array<number> = [];
    skills.forEach(s => skillIds.push(s.id));
    this.store.dispatch(
      new JobSeekerProfilePageActions.PartialUpdate('', this.jsId, {skills: skillIds}),
    );
    this.setSkillsEditMode(false);
  }

  // Education section
  addNewEducation() {
    this.resetIsCurrentTypeForm(this.educationForm);
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.NEW),
    );
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationType(this.EducationType.EDUCATION),
    );
  }

  addNewCertification() {
    this.resetIsCurrentTypeForm(this.certificationForm);
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.NEW),
    );
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationType(this.EducationType.CERTIFICATION),
    );
  }

  onSubmitEducation(formData: any) {
    if (this.store.selectSnapshot(JSPPageState.educationMode) === this.EducationMode.NEW) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.CreateNewEducation(this.jsId, formData),
      );
      this.resetIsCurrentTypeForm(this.educationForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.VIEW),
      );
    }
    if (this.store.selectSnapshot(JSPPageState.educationMode) === this.EducationMode.EDIT) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateEducation(this.jsId, formData.id, formData),
      );
      this.resetIsCurrentTypeForm(this.educationForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.VIEW),
      );
    }
  }

  onSubmitCertification(formData: any) {
    if (this.store.snapshot().JSPPage.educationMode === this.EducationMode.NEW) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.CreateNewCertification(this.jsId, formData),
      );
      this.resetIsCurrentTypeForm(this.certificationForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.VIEW),
      );
    }
    if (this.store.snapshot().JSPPage.educationMode === this.EducationMode.EDIT) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateCertification(this.jsId, formData.id, formData),
      );
      this.resetIsCurrentTypeForm(this.certificationForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.VIEW),
      );
    }
  }

  onEditEducation(formData: any) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationType(this.EducationType.EDUCATION),
    );
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.EDIT),
    );
    this.educationForm.patchValue(formData);
    this.educationForm.addControl('id', new FormControl(formData.id));
  }

  onEditCertification(formData: any) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationType(this.EducationType.CERTIFICATION),
    );
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.EDIT),
    );
    this.certificationForm.patchValue(formData);
    this.certificationForm.addControl('id', new FormControl(formData.id));
  }

  deleteEducationItem(educationId: number) {
    this.store.dispatch(new JobSeekerProfilePageActions.DeleteEducation(this.jsId, educationId));
  }

  deleteCertificationItem(certificationId: number) {
    this.store.dispatch(new JobSeekerProfilePageActions.DeleteCertification(this.jsId, certificationId));
  }

  closeForm() {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateEducationMode(this.EducationMode.VIEW),
    );
  }

  isEducationMaxCount() {
    return this.store.selectSnapshot(JSPPageState.educationAndCertificationData) === environment.maxEducationCount;
  }

  private resetIsCurrentTypeForm(form: FormGroup) {
    form.reset();
    form.patchValue({is_current: false});
  }

  // Experience section
  addNewJob() {
    this.resetIsCurrentTypeForm(this.experienceForm);
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateExperienceMode(this.ExperienceMode.NEW),
    );
  }

  onSubmitExperience(formData: any) {
    if (this.store.snapshot().JSPPage.experienceMode === this.ExperienceMode.NEW) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.CreateNewExperience(this.jsId, formData),
      );
      this.resetIsCurrentTypeForm(this.experienceForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateExperienceMode(this.ExperienceMode.VIEW),
      );
    }
    if (this.store.snapshot().JSPPage.experienceMode === this.ExperienceMode.EDIT) {
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateExperience(this.jsId, formData.id, formData),
      );
      this.resetIsCurrentTypeForm(this.experienceForm);
      this.store.dispatch(
        new JobSeekerProfilePageActions.UpdateExperienceMode(this.ExperienceMode.VIEW),
      );
    }
  }

  onEditExperience(formData: any) {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateExperienceMode(this.ExperienceMode.EDIT),
    );
    this.experienceForm.patchValue(formData);
    this.experienceForm.addControl('id', new FormControl(formData.id));
  }

  deleteExperienceItem(jobId: number) {
    this.store.dispatch(new JobSeekerProfilePageActions.DeleteExperience(this.jsId, jobId));
  }

  closeExperienceForm() {
    this.store.dispatch(
      new JobSeekerProfilePageActions.UpdateExperienceMode(this.ExperienceMode.VIEW),
    );
  }

  closeFormSection(sectionEditMode: string) {
    switch (sectionEditMode) {
      case (JobSeekerProfileSectionsEnum.MAIN_INFO_SECTION_EDIT_MODE):
        this.setMainInfoEditMode(false);
        break;
      case (JobSeekerProfileSectionsEnum.ADDRESS_SECTION_EDIT_MODE):
        this.setAddressEditMode(false);
        break;
      case (JobSeekerProfileSectionsEnum.ABOUT_SECTION_EDIT_MODE):
        this.setAboutEditMode(false);
        break;
      case (JobSeekerProfileSectionsEnum.PROFILE_DETAILS_SECTION_EDIT_MODE):
        this.setProfileDetailsEditMode(false);
        break;
      case (JobSeekerProfileSectionsEnum.SKILLS_SECTION_EDIT_MODE):
        this.setSkillsEditMode(false);
        break;
      default:
        break;
    }
  }

  providePreviewProfile() {
    const dialogPreviewRef = this.dialog.open(JobSeekerProfilePageViewComponent, {
      width: '80%',
      data: {
        isModal: true
      },
    });
    dialogPreviewRef.afterClosed().subscribe(() => {
      dialogPreviewRef.close();
    });
  }

  public get aboutData() {
    return {about: this.initialData.about};
  }

  private modifyDataWithPhoneNumber(formData) {
    const maskSymbol = '-';
    const key = 'phone';
    const {
      [key]: phoneValue,
      ...userData
    } = formData;

    return {
      [key]: (phoneValue && phoneValue !== maskSymbol) ? phoneValue : null,
      user: userData
    };
  }

  private get initialData() {
    return this.store.selectSnapshot(JSPPageState.initialData);
  }
}
