import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-view-company-profile',
  template: `
    <mat-card>
      <div class="company-profile-detail-container">
        <mat-card-title>
          {{ companyData?.name }}
        </mat-card-title>
      </div>
      <div>
      </div>
      <div class="company-profile-detail-container">
        <mat-card-content>
          <app-profile-address-view [addressData]="companyData?.address">
          </app-profile-address-view>
        </mat-card-content>
      </div>
      <div class="company-profile-detail-container">
        <img mat-card-avatar class="big-avatar" [src]="companyData?.photo?.original">
      </div>
      <div class="company-profile-detail-container">

        <mat-card-subtitle>
          Company phone:&nbsp;
        </mat-card-subtitle>
        <mat-card-content>
          {{ companyData?.phone }}
        </mat-card-content>
      </div>

      <div class="company-profile-detail-container">
        <mat-card-subtitle>
          Company fax:&nbsp;
        </mat-card-subtitle>
        <mat-card-content>
          {{ companyData?.fax }}
        </mat-card-content>
      </div>

      <div class="company-profile-detail-container">
        <mat-card-subtitle>
          Company website:&nbsp;
        </mat-card-subtitle>
        <mat-card-content>
          {{ companyData?.website }}
        </mat-card-content>
      </div>

      <div class="company-profile-detail-container">
        <mat-card-subtitle>
          Company email:&nbsp;
        </mat-card-subtitle>
        <mat-card-content>
          {{ companyData?.email }}
        </mat-card-content>
      </div>
    </mat-card>
  `,
  styles: [`
    .company-profile-detail-container {
      display: flex;
      flex-direction: row;
    }
  `],
})
export class ViewCompanyProfileComponent {
  @Input() companyData: any;
}
