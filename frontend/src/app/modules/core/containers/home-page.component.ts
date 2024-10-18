import {ChangeDetectionStrategy, Component} from '@angular/core';
import {Select} from '@ngxs/store';
import {Observable} from 'rxjs';
import {AuthState} from '../../auth/states/auth.state';

@Component({
  selector: 'app-home-page',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <mat-card>
      <mat-card-title>Home</mat-card-title>
      <mat-card-content>
        <div *ngIf="loggedIn$ | async">
          <p>You are Logged In! Hello {{ username$ | async }}</p>
          <div *ngxPermissionsOnly="['is_company_user']">
            <p>You are Company User!</p>
          </div>
          <div *ngxPermissionsOnly="['is_job_seeker']">
            <p>You are Job Seeker!</p>
          </div>
        </div>
        <div *ngIf="!(loggedIn$ | async)">
          <p>You are Not Logged In!</p>
        </div>
      </mat-card-content>
      <mat-card-actions>
        <div *ngIf="loggedIn$ | async">
          <div *ngxPermissionsOnly="['is_company_user']">
            <button mat-raised-button color="accent" routerLink="/company/profile/my/edit">My Company Profile</button>
          </div>
          <div *ngxPermissionsOnly="['is_job_seeker']">
            <button mat-raised-button color="accent" routerLink="/job-seeker/profile/my/edit">My Job Seeker Profile
            </button>
          </div>
        </div>
        <div *ngIf="!(loggedIn$ | async)">
          <button mat-raised-button color="primary" routerLink="/login">Login</button>
          <button mat-raised-button color="primary" routerLink="/job-seeker-signup">Job Seeker Signup</button>
          <button mat-raised-button color="primary" routerLink="/company-signup">Company Signup</button>
        </div>
      </mat-card-actions>
    </mat-card>
  `,
  styles: [`
    :host {
      text-align: center;
    }
  `],
})
export class HomePageComponent {
  @Select(AuthState.isAuthorized) loggedIn$: Observable<boolean>;
  @Select(AuthState.username) username$: Observable<string>;
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;
  @Select(AuthState.user) user$: Observable<boolean>;
}
