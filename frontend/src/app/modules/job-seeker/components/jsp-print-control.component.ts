import { Component, Input, ViewChild } from '@angular/core';
import { MatTooltip } from '@angular/material';
import { Router } from '@angular/router';
import { JobSeekerRoute } from '../../shared/constants/routes/job-seeker-routes';

@Component({
  selector: 'app-jsp-print-control',
  template: `
  <div *ngIf="!iconOnly; else iconTmp">
    <button
      class="in-vertical-list"
      *ngIf="!pending"
      mat-raised-button
      color="primary"
      (click)="printDocument()"
    >
      Download profile to PDF
      <mat-icon matSuffix>save_alt</mat-icon>
    </button>
  </div>
  <ng-template #iconTmp>
    <button
      *ngIf="!pending"
      mat-icon-button
      matTooltip="Download profile"
      #tooltip="matTooltip"
      (click)="printDocument()"
    >
      <mat-icon aria-label="Download profile">save_alt</mat-icon>
    </button>
  </ng-template>
  `,
  styles: [`
  .in-vertical-list {
    margin-top: 5px;
  }
  `]
})
export class JspPrintControlComponent {
  @Input() pending = false;
  @Input() iconOnly: boolean;

  @ViewChild('tooltip') tooltip: MatTooltip;

  constructor(private router: Router) {}

  printDocument() {
    if (this.tooltip) {
      this.tooltip.hide();
    }
    this.router.navigate([
      this.router.url,
      { outlets: { [JobSeekerRoute.printOutletName]: JobSeekerRoute.jobSeekerPrintProfile } }
    ]);
    setTimeout(() => {
      window.print();
      this.router.navigate([
        this.router.url,
        { outlets: { [JobSeekerRoute.printOutletName]: null } }
      ]);
    });
  }
}
