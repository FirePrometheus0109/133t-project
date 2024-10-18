import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../../core/services/navigation.service';
import { InputLengths } from '../../../../shared/constants/validators/input-length';
import { LetterTemplateManageActions } from '../../../actions';
import {
  SelectLetterTemplateEventTypeComponent
} from '../../../components/letter-templates/select-letter-template-event-type/select-letter-template-event-type.component';
import { LetterTemplateEventType, LetterTemplateItem } from '../../../models/letter-templates.model';
import { LetterTemplateManagePageState } from '../../../states/letter-templates/letter-template-manage-page.state';


@Component({
  selector: 'app-letter-template-manage',
  templateUrl: './letter-template-manage.component.html',
  styleUrls: ['./letter-template-manage.component.scss']
})
export class LetterTemplateManageComponent {
  @Select(LetterTemplateManagePageState.createMode) createMode$: Observable<boolean>;
  @Select(LetterTemplateManagePageState.errors) errors$: Observable<object>;
  @Select(LetterTemplateManagePageState.editMode) editMode$: Observable<boolean>;
  @Select(LetterTemplateManagePageState.viewMode) viewMode$: Observable<boolean>;
  @Select(LetterTemplateManagePageState.letterTemplateEventTypes) letterTemplateEventTypes$: Observable<LetterTemplateEventType[]>;
  @Select(LetterTemplateManagePageState.currentLetterTemplate) currentLetterTemplate$: Observable<LetterTemplateItem>;

  letterTemplateForm = new FormGroup({
    name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    subject: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.titles)])),
    body: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.descriptions)])),
    event_type: new FormControl(null),
  });

  constructor(private store: Store, private navigationService: NavigationService, private dialog: MatDialog) {
  }

  createLetterTemplate() {
    this.store.dispatch(new LetterTemplateManageActions.CreateLetterTemplate(this.letterTemplateForm.value));
  }

  saveLetterTemplate() {
    this.store.dispatch(
      new LetterTemplateManageActions
        .SaveLetterTemplate(this.currentLetterTemplate.id, this.prepareEventTypeData(this.letterTemplateForm.value))
    );
  }

  goToLetterTemplateEdit() {
    this.navigationService.goToLetterTemplateEditPage(this.currentLetterTemplate.id.toString());
  }

  goToLetterTemplatesList() {
    this.navigationService.goToLetterTemplatesListPage();
  }

  provideDefaultChoice() {
    const dialogRef = this.dialog.open(SelectLetterTemplateEventTypeComponent, {
      width: '60%',
      data: {
        eventTypes: this.store.selectSnapshot(LetterTemplateManagePageState.letterTemplateEventTypes),
        selectedEventType: this.currentLetterTemplate.event_type
      },
    });
    dialogRef.componentInstance.submittedResult.subscribe((eventTypeId) => {
      this.updateEventTypeControlValue(eventTypeId);
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.submittedResult.unsubscribe();
      dialogRef.close();
    });
  }

  private prepareEventTypeData(formValue) {
    const result = {...formValue};
    if (result.event_type && result.event_type.hasOwnProperty('id')) {
      result.event_type = result.event_type.id;
    }
    return result;
  }

  private updateEventTypeControlValue(eventTypeId: number) {
    this.letterTemplateForm.controls['event_type'].setValue(eventTypeId);
  }

  private get currentLetterTemplate() {
    return this.store.selectSnapshot(LetterTemplateManagePageState.currentLetterTemplate);
  }
}
