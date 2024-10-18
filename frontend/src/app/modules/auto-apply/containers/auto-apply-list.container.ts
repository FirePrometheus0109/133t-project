import { Component } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../core/services/navigation.service';
import { CoreState } from '../../core/states/core.state';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { AutoApplyListActions } from '../actions';
import { AutoApply } from '../models/auto-apply.model';
import { AutoApplyListState } from '../states/auto-apply-list.state';


@Component({
  selector: 'app-auto-apply-list-page',
  template: `
    <button type="button" mat-raised-button color="primary" (click)="createNewAutoApply()">
      Add new auto apply list
      <mat-icon matSuffix>add</mat-icon>
    </button>
    <app-auto-apply-preview *ngFor="let autoApplyItem of (autoApplyList$ | async)"
                            [autoApplyItem]="autoApplyItem"
                            (goToAutoApply)="goToAutoApply($event)"
                            (deleteAutoApply)="deleteAutoApply($event)"
                            [autoApplyEnums]="autoApplyEnums$ | async">
    </app-auto-apply-preview>
  `,
  styles: [],
})
export class AutoApplyListComponent {
  @Select(AutoApplyListState.autoApplyList) autoApplyList$: Observable<Array<AutoApply>>;
  @Select(CoreState.autoApplyEnums) autoApplyEnums$: Observable<object>;

  private confirmButtonText = 'I\'m sure. I want to delete this auto apply';
  private negativeButtonText = 'No';
  private modalTitle = 'Confirm removal';

  constructor(private store: Store,
              private navigationService: NavigationService,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  createNewAutoApply() {
    this.navigationService.goToAutoApplyCreatePage();
  }

  goToAutoApply(autoApply: AutoApply) {
    if (this.autoApplyEnums[autoApply.status] === this.autoApplyEnums.SAVED) {
      this.navigationService.goToAutoApplyEditPage(autoApply.id.toString());
    } else {
      this.navigationService.goToAutoApplyResultPage(autoApply.id.toString());
    }
  }

  deleteAutoApply(autoApply: AutoApply) {
    this.confirmationDialogService.openConfirmationDialog({
        message: this.prepareConfirmationMessage(autoApply),
        callback: this.deleteAutoApplyItem.bind(this),
        arg: autoApply,
        confirmationText: `${this.confirmButtonText}`,
        negativeText: `${this.negativeButtonText}`,
        title: `${this.modalTitle}`,
        dismissible: true
      },
    );
  }

  deleteAutoApplyItem(autoApply) {
    this.store.dispatch(new AutoApplyListActions.DeleteAutoApplyItem(autoApply.id));
  }

  private prepareConfirmationMessage(autoApply) {
    if (this.autoApplyEnums[autoApply.status] === this.autoApplyEnums.IN_PROGRESS) {
      return `<${autoApply.title}> is in the process. If proceed, Auto Apply will stop and all found Job Postings will be removed.` +
        `Are you sure you want to delete <${autoApply.title}>?`;
    } else {
      return `If proceed, all your saved information will be removed. Are you sure you want to delete <${autoApply.title}>?`;
    }
  }

  get autoApplyEnums() {
    return this.store.selectSnapshot(CoreState.autoApplyEnums);
  }
}
