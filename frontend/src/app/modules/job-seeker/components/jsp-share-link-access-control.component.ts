import { Component, EmbeddedViewRef, EventEmitter, Input, Output, TemplateRef, ViewChild } from '@angular/core';
import { MatSnackBar, MatSnackBarRef } from '@angular/material';
import * as copy from 'copy-to-clipboard';
import { JobSeekerRoute } from '../../shared/constants/routes/job-seeker-routes';

export enum IconState {
  Shared = 'link',
  Unshared = 'link_off',
}

@Component({
  selector: 'app-jsp-share-link-access-control',
  template: `
    <div class="jsp-share-link-control-container">
      <button
        mat-raised-button
        color="primary"
        [disabled]="!profileIsSharing"
        (click)="onShareButtonClick()"
      >
        Share profile via URL
      </button>
      <button
        mat-raised-button
        color="primary"
        matTooltip="{{getSharingToggleTooltipText()}}"
        (click)="onSharingToggleClick()"
      >
        <mat-icon matSuffix>{{getIconName()}}</mat-icon>
      </button>
    </div>
    <ng-template #snackTemplate>
      <div class="mat-simple-snackbar">
        <span>Your profile link is copied to clipboard</span>
        <span *ngIf="!profileIsPublic">Note that your profile is currently in Hidden mode</span>
        <div class="mat-simple-snackbar-action">
          <button mat-button class="mat-button" (click)="onSnackDismiss()">
            <span class="mat-button-wrapper">Ok, got it</span>
            <div
              class="mat-button-ripple mat-ripple"
              matripple
            >
            </div>
            <div class="mat-button-focus-overlay"></div>
          </button>
        </div>
      </div>
    </ng-template>
  `,
  styles: [
    `
    .jsp-share-link-control-container {
      margin: 5px 0;
    }
    .jsp-share-link-control-container button {
      margin: 0 5px 0 0;
    }
    .mat-simple-snackbar {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .mat-simple-snackbar-action {
      margin-top: 10px;
    }
    `
  ]
})
export class JspShareLinkAccessControlComponent {
  @Input()  profileIsPublic: boolean;
  @Input()  profileIsSharing: boolean;
  @Input()  uid: string;
  @Output() sharingToggleClicked = new EventEmitter<any>();
  @ViewChild('snackTemplate') snackTemplate: TemplateRef<any>;

  private readonly snackAppearenceDuration = 10000;
  public activeSnackRef?: MatSnackBarRef<EmbeddedViewRef<any>>;

  constructor(private snackBar: MatSnackBar) {}

  public onShareButtonClick() {
    if (this.uid) {
      copy(JobSeekerRoute.getPublicProfileUrl(this.uid));
      this.activeSnackRef = this.snackBar.openFromTemplate(this.snackTemplate, {
        duration: this.snackAppearenceDuration,
      });
    }
    if (!this.profileIsSharing) {
      this.emitSharingToggleClick();
    }
  }

  public onSnackDismiss() {
    if (this.activeSnackRef) {
      this.activeSnackRef.dismiss();
    }
  }

  public onSharingToggleClick() {
    this.emitSharingToggleClick();
  }

  public emitSharingToggleClick() {
    this.sharingToggleClicked.emit(!this.profileIsSharing);
  }

  public getIconName() {
    return this.profileIsSharing ? IconState.Shared : IconState.Unshared;
  }

  public getSharingToggleTooltipText() {
    return (this.profileIsSharing ? 'Cancel' : 'Enable') + ' access by URL';
  }
}
