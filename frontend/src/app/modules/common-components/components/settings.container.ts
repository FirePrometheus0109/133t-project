import { Component } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Store } from '@ngxs/store';
import { SettingsPageActions } from '../../auth/actions';
import { CoreState } from '../../core/states/core.state';
import { DeleteAccountDialogComponent } from '../../shared/components/delete-account-dialog.component';


@Component({
  selector: 'app-settings',
  template: `
    <mat-card>
      <mat-card-title align="center">
        Settings
      </mat-card-title>
      <mat-card-content>
        <mat-accordion>
          <mat-expansion-panel [expanded]="true">
            <mat-expansion-panel-header>
              <mat-panel-title>General</mat-panel-title>
            </mat-expansion-panel-header>
            <app-account-page></app-account-page>
            <button type="button" mat-raised-button color="primary" (click)="deleteAccount()">
              <mat-icon matSuffix>delete</mat-icon>
              Delete account
            </button>
          </mat-expansion-panel>
          <mat-expansion-panel>
            <mat-expansion-panel-header>
              <mat-panel-title>Notifications</mat-panel-title>
            </mat-expansion-panel-header>
            <app-job-seeker-manage-notifications></app-job-seeker-manage-notifications>
          </mat-expansion-panel>
        </mat-accordion>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    button {
      margin-top: 1em;
    }
  `],
})
export class SettingsComponent {
  constructor(private dialog: MatDialog, private store: Store) {
  }

  deleteAccount() {
    const dialogRef = this.dialog.open(DeleteAccountDialogComponent, {
      width: '80%',
      data: {
        account_deletion_reasons: this.store.selectSnapshot(CoreState.accountDeletionReasons)
      }
    });
    const sub = dialogRef.componentInstance.confirmed.subscribe((deletionReason) => {
      this.store.dispatch(new SettingsPageActions.DeleteAccount(deletionReason));
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      sub.unsubscribe();
      dialogRef.close();
    });
  }
}
