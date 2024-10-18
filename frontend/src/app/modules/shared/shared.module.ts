// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { RouterModule } from '@angular/router';
import { MaterialModule } from '../material';

// Service
import { CandidateService } from '../candidate/services/candidate.service';
import { JobService } from '../company/services/job.service';
import { PurchasedJobSeekersService } from '../company/services/purchased-job-seekers.service';
import { JobSeekerService } from '../job-seeker/services';
import { ConfirmationDialogService } from './services/confirmation-dialog.service';
import { GeneralActionService } from './services/general-action.service';
import { SocialIconsService } from './services/social-icons.service';

// Components
import { AddressComponent } from './components/address.component';
import { YesNoAnswerComponent } from './components/answers-components/yes-no-answer.component';
import { AppMessageDialogComponent } from './components/app-dialog-message';
import { AutocompleteFilterComponent } from './components/autocomplete-filter/autocomplete-filter.component';
import {
  AutocompleteMultiselectFilterComponent
} from './components/autocomplete-multiselect-filter/autocomplete-multiselect-filter.component';
import { BaseFormComponent } from './components/base-form.component';
import { CandidateStatisticPanelComponent } from './components/candidate-statistic-panel/candidate-statistic-panel.component';
import { ChangePasswordFormComponent } from './components/change-password-form.component';
import { CompletionSpinnerComponent } from './components/completion-spinner/completion-spinner.component';
import { ConfirmationDialogComponent } from './components/confirmation-dialog.component';
import { ControlMessagesComponent } from './components/control-messages.component';
import { DeleteAccountDialogComponent } from './components/delete-account-dialog.component';
import { DeletedJobViewComponent } from './components/deleted-job-view/deleted-job-view.component';
import { DownloadSelectedToCSVComponent } from './components/download-selected-to-csv/download-selected-to-csv.component';
import { JspCertificationPreviewComponent } from './components/education/jsp-certification-preview.component';
import { JspEducationPreviewComponent } from './components/education/jsp-education-preview.component';
import { JspExperiencePreviewComponent } from './components/experience/jsp-experience-preview.component';
import { FiltersChipListComponent } from './components/filters-chip-list/filters-chip-list.component';
import { IndustrySelectFormComponent } from './components/industry-select-form.component';
import { InputFilterComponent } from './components/input-filter/input-filter.component';
import { JobFavoriteToggleComponent } from './components/job-favorite.toggle';
import { JobMetadataComponent } from './components/job-metadata.component';
import { JobSeekerFavoritesButtonComponent } from './components/job-seeker-favorites-button/job-seeker-favorites-button.component';
import { ViewJobSkillComponent } from './components/job-skill.component';
import { SortingFieldComponent } from './components/job-sorting-field.component';
import { VjspProfileDetailComponent } from './components/js-profile-details/vjsp-profile-detail.component';
import { VjspShortcutInfoComponent } from './components/js-profile-details/vjsp-shortcut-info.component';
import { CitySelectComponent } from './components/location/city-select/city-select.component';
import { LocationSelectFilterComponent } from './components/location/location-select-filter/location-select-filter.component';
import { ZipSelectComponent } from './components/location/zip-select/zip-select.component';
import { ManageApplyRequirementsDialogComponent } from './components/manage-apply-requirements-dialog.component';
import { CoverLetterSelectFormComponent } from './components/manage-cover-letters/cover-letter-select-form.component';
import { JsManageCoverLettersComponent } from './components/manage-cover-letters/js-manage-cover-letters.container';
import { JspCoverLetterFormComponent } from './components/manage-cover-letters/jsp-cover-letter-form.component';
import { JspCoverLetterListComponent } from './components/manage-cover-letters/jsp-cover-letter-list.component';
import { JspCoverLetterPreviewComponent } from './components/manage-cover-letters/jsp-cover-letter-preview.component';
import { MaterialFileUploadComponent } from './components/material-file-upload/material-file-upload.component';
import { NewPriceMarkerComponent } from './components/new-price-marker/new-price-marker.component';
import { ProfileAddressViewComponent } from './components/profile-address-view/profile-address-view.component';
import { ProfileDetailsExtComponent } from './components/profile-details-ext-form.component';
import { ProfileDetailsComponent } from './components/profile-details-form.component';
import { PurchaseProfileButtonComponent } from './components/purchase-profile-button.component';
import { RadioFilterComponent } from './components/radio-filter.component';
import { SearchFieldComponent } from './components/search-field/search-field.component';
import { SearchListFormComponent } from './components/search-list-form/search-list-form.component';
import { SkillsSelectComponent } from './components/skills-select.component';
import { SkillsViewComponent } from './components/skills-view.component';
import { StopJobDialogComponent } from './components/stop-job-dialog.component';

// Pipes
import { EnumKeysPipe } from './pipes/enumKeys.pipe';
import { KeysPipe } from './pipes/keys.pipe';
import { PostedDatePipe } from './pipes/postedDate.pipe';
import { SalaryViewPipe } from './pipes/salary-view.pipe';
import { SearchLocationPipe } from './pipes/search-location.pipe';

// Directives
import { PhoneMaskDirective } from './directives/phone-mask.directive';

export const SHARED_COMPONENTS = [
  ControlMessagesComponent,
  AddressComponent,
  BaseFormComponent,
  IndustrySelectFormComponent,
  KeysPipe,
  EnumKeysPipe,
  SalaryViewPipe,
  SkillsSelectComponent,
  SkillsViewComponent,
  MaterialFileUploadComponent,
  ProfileDetailsComponent,
  ProfileDetailsExtComponent,
  JobMetadataComponent,
  JobFavoriteToggleComponent,
  AppMessageDialogComponent,
  ViewJobSkillComponent,
  ConfirmationDialogComponent,
  PostedDatePipe,
  DeleteAccountDialogComponent,
  ChangePasswordFormComponent,
  JsManageCoverLettersComponent,
  JspCoverLetterFormComponent,
  JspCoverLetterListComponent,
  JspCoverLetterPreviewComponent,
  ManageApplyRequirementsDialogComponent,
  CoverLetterSelectFormComponent,
  YesNoAnswerComponent,
  SortingFieldComponent,
  PurchaseProfileButtonComponent,
  RadioFilterComponent,
  JspExperiencePreviewComponent,
  JspCertificationPreviewComponent,
  JspEducationPreviewComponent,
  VjspShortcutInfoComponent,
  VjspProfileDetailComponent,
  AutocompleteFilterComponent,
  StopJobDialogComponent,
  CitySelectComponent,
  ZipSelectComponent,
  LocationSelectFilterComponent,
  ProfileAddressViewComponent,
  SearchLocationPipe,
  PhoneMaskDirective,
  FiltersChipListComponent,
  InputFilterComponent,
  AutocompleteMultiselectFilterComponent,
  CandidateStatisticPanelComponent,
  JobSeekerFavoritesButtonComponent,
  CompletionSpinnerComponent,
  NewPriceMarkerComponent,
  DeletedJobViewComponent,
  DownloadSelectedToCSVComponent,
  SearchListFormComponent,
  SearchFieldComponent,
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    MaterialModule,
  ],
  declarations: SHARED_COMPONENTS,
  exports: SHARED_COMPONENTS,
  providers: [
    JobSeekerService,
    JobService,
    ConfirmationDialogService,
    GeneralActionService,
    PurchasedJobSeekersService,
    CandidateService,
    SocialIconsService,
    {provide: MatDialogRef, useValue: {}},
    {provide: MAT_DIALOG_DATA, useValue: []},
  ],
})
export class SharedModule {
}
