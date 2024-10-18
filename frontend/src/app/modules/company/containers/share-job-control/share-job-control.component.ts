import { Component, Input } from '@angular/core';
import { MatDialog } from '@angular/material';

import { DialogData, ShareJobDialogComponent } from './share-job-dialog.component';

@Component({
  selector: 'app-share-job-control',
  templateUrl: './share-job-control.component.html',
  styleUrls: ['./share-job-control.component.scss']
})
export class ShareJobControlComponent {

  @Input() uid: string;
  // for support emai share
  @Input() id: number;

  constructor(public dialog: MatDialog) { }

  openShareDialog() {
    const data: DialogData = {uid: this.uid, id: this.id};
    this.dialog.open(ShareJobDialogComponent, {
      data
    });
  }

}
