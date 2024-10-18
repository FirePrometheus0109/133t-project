import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialog, MatDialogRef } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CoreActions } from '../../core/actions';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { SnackBarMessageType } from '../../shared/models/snack-bar-message';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { AccountPageActions } from '../actions';
import { EditAccountPasswordFormComponent } from '../components/edit-account-password-form.component';
import { UpdatePasswordCredentials } from '../models/credentials.model';
import { User } from '../models/user.model';
import { AccountPageState } from '../states/account-page.state';
import { AuthState } from '../states/auth.state';


@Component({
  selector: 'app-account-page',
  template: `
    <div *ngIf="!(isJobSeeker$ | async) && (loggedIn$ | async)">
      <app-view-account *ngIf="!(isEditMode$ | async)"
                        [user]="user$ | async"
                        (editAccount)="onEditAccount()"
                        (changeAccountPassword)="onChangeAccountPassword()">
      </app-view-account>
      <app-edit-account *ngIf="(isEditMode$ | async)"
                        [form]="accountForm"
                        [initialData]="user$ | async"
                        [pending]="pending$ | async"
                        [errors]="errors$ | async"
                        (saveAccount)="onSaveAccount()"
                        (cancelEdit)="onCancelEdit()"
                        (changeAccountPassword)="onChangeAccountPassword()">
      </app-edit-account>
    </div>
    <div *ngIf="isJobSeeker$ | async">
      <button mat-raised-button color="primary" (click)="onChangeAccountPassword()">Password change</button>
    </div>

  `,
  styles: [],
})
export class AccountPageComponent {
  @Select(AccountPageState.user) user$: Observable<User>;
  @Select(AccountPageState.pending) pending$: Observable<any>;
  @Select(AccountPageState.errors) errors$: Observable<any>;
  @Select(AccountPageState.isEditMode) isEditMode$: Observable<boolean>;
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;
  @Select(AuthState.isAuthorized) loggedIn$: Observable<boolean>;

  public accountForm: FormGroup = new FormGroup({
    first_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
    last_name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
  });

  constructor(private store: Store,
              private dialog: MatDialog,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  public onEditAccount(): void {
    this.store.dispatch(new AccountPageActions.ToggleEditMode(true));
  }

  public onChangeAccountPassword(): void {
    this.openChangePasswordDialog();
  }

  public onCancelEdit(): void {
    this.store.dispatch(new AccountPageActions.ToggleEditMode(false));
  }

  public onSaveAccount(): void {
    this.store.dispatch(new AccountPageActions.UpdateAccountData(this.getAccountData()));
  }

  private getAccountData(): object {
    return {
      first_name: this.accountForm.value.first_name,
      last_name: this.accountForm.value.last_name,
    };
  }

  private openChangePasswordDialog() {
    const dialogRef = this.dialog.open(EditAccountPasswordFormComponent, {
      width: '60%',
    });
    dialogRef.componentInstance.errors = this.errors$;
    dialogRef.componentInstance.submitted.subscribe((formData: UpdatePasswordCredentials) => {
      if (formData) {
        this.updatePassword(formData, dialogRef);
      }
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.submitted.unsubscribe();
      dialogRef.close();
    });
  }

  private updatePassword(formData: UpdatePasswordCredentials, dialogRef: MatDialogRef<EditAccountPasswordFormComponent>) {
    this.store.dispatch(new AccountPageActions.UpdateAccountPassword(formData)).subscribe(() => {
      if (!this.store.selectSnapshot(AccountPageState.errors)) {
        dialogRef.close();
        this.openChangedPasswordConfirmationDialog();
      }
    });
  }

  private openChangedPasswordConfirmationDialog() {
    const successMessage: string = this.store.selectSnapshot(AccountPageState.successChangePasswordMessage);

    this.store.dispatch(new CoreActions.SnackbarOpen({
      message: successMessage,
      type: SnackBarMessageType.SUCCESS,
    }));
  }
}
