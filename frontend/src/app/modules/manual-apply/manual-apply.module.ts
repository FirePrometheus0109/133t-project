// Modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { JobSeekerModule } from '../job-seeker/job-seeker.module';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';

// Components
import { AppMessageDialogComponent } from '../shared/components/app-dialog-message';
import { ManageApplyRequirementsDialogComponent } from '../shared/components/manage-apply-requirements-dialog.component';
import { JsManageCoverLettersComponent } from '../shared/components/manage-cover-letters/js-manage-cover-letters.container';
import { ManualApplyButtonComponent } from './components/manual-apply-button.component';

// Services
import { ManualApplyService } from './services';

// States
import { ManualApplyState } from './states/manual-apply-view.state';

export const MANUAL_APPLY_COMPONENTS = [
  ManualApplyButtonComponent
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    JobSeekerModule,
    NgxsModule.forFeature([
      ManualApplyState,
    ]),
  ],
  declarations: [MANUAL_APPLY_COMPONENTS],
  exports: [MANUAL_APPLY_COMPONENTS],
  entryComponents: [AppMessageDialogComponent, ManageApplyRequirementsDialogComponent, JsManageCoverLettersComponent],
  providers: [ManualApplyService],
})
export class ManualApplyModule {
}
