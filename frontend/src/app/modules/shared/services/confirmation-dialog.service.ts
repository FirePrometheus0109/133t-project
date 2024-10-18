import { Injectable } from '@angular/core';
import { MatDialog, MatDialogRef } from '@angular/material';
import { Subject } from 'rxjs';
import { ConfirmationDialogComponent } from '../components/confirmation-dialog.component';


interface ConfirmationDialogArguments {
  message: string;
  callback?: Function;
  callbackNegative?: Function;
  arg?: any;
  argNegative?: any;
  confirmationText?: string;
  negativeText?: string;
  title?: string;
  dismissible?: boolean;
}


@Injectable({
  providedIn: 'root',
})
export class ConfirmationDialogService {
  private confirmationButtonDefaultText = 'Ok';
  private negativeButtonDefaultText = 'Cancel';
  private defaultDialogWidth = '60%';

  modalSelection$: Subject<boolean> = new Subject<boolean>();

  constructor(private dialog: MatDialog) {
  }

  public openConfirmationDialog(namedArgs: ConfirmationDialogArguments): MatDialogRef<ConfirmationDialogComponent> {
    const dialogRef = this.dialog.open(ConfirmationDialogComponent, {
      width: this.defaultDialogWidth,
      data: {
        message: namedArgs.message,
        confirmButtonText: namedArgs.confirmationText || this.confirmationButtonDefaultText,
        negativeButtonText: namedArgs.negativeText || this.negativeButtonDefaultText,
        title: namedArgs.title || '',
        dismissible: namedArgs.dismissible || true,
      },
    });
    dialogRef.componentInstance.confirmed.subscribe((result) => {
      this.dialog.closeAll();
      this.modalSelection$.next(result);
      if (result && namedArgs.callback) {
        (namedArgs.arg) ? namedArgs.callback(namedArgs.arg) : namedArgs.callback(result);
      } else if (!result && namedArgs.callbackNegative) {
        (namedArgs.argNegative) ? namedArgs.callbackNegative(namedArgs.argNegative) : namedArgs.callbackNegative(result);
      }
      dialogRef.close();
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.componentInstance.confirmed.unsubscribe();
      dialogRef.close();
    });
    return dialogRef;
  }

  public openSimplifiedConfirmationDialog(message: string, callback?: Function) {
    const args = {message: message, callback: callback};
    this.openConfirmationDialog(args);
  }
}
