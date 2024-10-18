import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-jsp-publish-profile',
  template: `
    <button mat-raised-button
            color="primary"
            [disabled]="!isProfileCanBePublic"
            (click)="toggleProfile()">
      {{buttonName}}
      <mat-icon matSuffix>publish</mat-icon>
    </button>
    <mat-icon
        mat-raised-button
        [matTooltip]="publishHideProfileTooltipText"
        matTooltipClass="jsp-profile-validation-tooltip"
        matSuffix>
      help
    </mat-icon>

  `,
  styles: [],
})
export class JspPublishProfileComponent {
  @Input() isProfilePublic: boolean;
  @Input() isProfileCanBePublic: boolean;
  @Input() publishHideProfileTooltipText: string;
  @Output() toggleProfileStatus = new EventEmitter<any>();

  public get buttonName(): string {
    const prefix: string = this.isProfilePublic ? 'Hide' : 'Publish';
    return `${prefix} profile`;
  }

  public toggleProfile() {
    this.toggleProfileStatus.emit(!this.isProfilePublic);
  }
}
