// modules
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { NgxsModule } from '@ngxs/store';
import { MaterialModule } from '../material';
import { SharedModule } from '../shared';
import { SurveyRoutingModule } from './survey-routing.module';

// services
import { ConfirmationDialogService } from '../shared/services/confirmation-dialog.service';
import { DefaultQuestionsService } from './services/default-questions.service';
import { SavedQuestionsService } from './services/saved-questions.service';
import { SurveyService } from './services/survey.service';

// resolvers
import { DefaultQuestionsPageResolver } from './resolvers/default-questions-page.resolver';
import { SavedQuestionsPageResolver } from './resolvers/saved-questions-page.resolver';
import { SurveyListPageResolver } from './resolvers/survey-list-page.resolver';

// states
import { AnswersState } from './states/answers.state';
import { DefaultQuestionsState } from './states/default-questions.state';
import { SavedQuestionsState } from './states/saved-questions.state';
import { SurveyEditState } from './states/survey-edit.state';
import { SurveyState } from './states/survey.state';

// components
import { ConfirmationDialogComponent } from '../shared/components/confirmation-dialog.component';
import { AnswerQuestionsComponent } from './components/answers/answer-questions.component';
import { ViewAnswerComponent } from './components/answers/view-answer.component';
import { EditQuestionFormComponent } from './components/edit-question-form.component';
import { ModalQuestionCreateComponent } from './components/modal-question-create.component';
import { NewQuestionCreateComponent } from './components/new-question-create.component';
import { QuestionPreviewComponent } from './components/question-preview.component';
import { QuestionsFromSelectedComponent } from './components/questions-from-selected.component';
import { SelectSurveyDialogComponent } from './components/select-survey-dialog.component';
import { SurveyPreviewComponent } from './components/survey-preview.component';
import { SurveyTitleEditFormComponent } from './components/survey-title-edit-form.component';
import { SurveyTitlePreviewComponent } from './components/survey-title-preview.component';
import { SurveyViewModalComponent } from './components/survey-view-modal.component';
import { DefaultQuestionsComponent } from './containers/default-questions.container';
import { SavedQuestionsComponent } from './containers/saved-questions.container';
import { SurveyEditComponent } from './containers/survey-edit.container';
import { SurveyListComponent } from './containers/survey-list.container';
import { SurveyComponent } from './containers/survey.container';

export const SURVEY_COMPONENTS = [
  // containers
  SurveyComponent,
  DefaultQuestionsComponent,
  SavedQuestionsComponent,
  SurveyListComponent,
  SurveyEditComponent,
  // components
  EditQuestionFormComponent,
  QuestionPreviewComponent,
  SurveyPreviewComponent,
  SurveyTitleEditFormComponent,
  SurveyTitlePreviewComponent,
  NewQuestionCreateComponent,
  ModalQuestionCreateComponent,
  QuestionsFromSelectedComponent,
  SelectSurveyDialogComponent,
  SurveyViewModalComponent,
  ViewAnswerComponent,
  AnswerQuestionsComponent,
];


@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MaterialModule,
    SharedModule,
    SurveyRoutingModule,
    NgxsModule.forFeature([
      DefaultQuestionsState,
      SavedQuestionsState,
      SurveyState,
      SurveyEditState,
      AnswersState,
    ]),
  ],
  declarations: SURVEY_COMPONENTS,
  exports: SURVEY_COMPONENTS,
  providers: [
    DefaultQuestionsService,
    DefaultQuestionsPageResolver,
    SavedQuestionsService,
    SavedQuestionsPageResolver,
    SurveyService,
    SurveyListPageResolver,
    ConfirmationDialogService
  ],
  entryComponents: [
    NewQuestionCreateComponent,
    QuestionsFromSelectedComponent,
    ConfirmationDialogComponent,
  ],
})
export class SurveyModule {
}
