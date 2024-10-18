import { ChangeDetectionStrategy, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatDialog } from '@angular/material';
import { NavigationEnd, Router } from '@angular/router';
import { Actions, ofActionSuccessful, Select, Store } from '@ngxs/store';
import { concat, forkJoin, Observable } from 'rxjs';
import { AuthActions } from '../../auth/actions';
import { LoggedUser } from '../../auth/models/user.model';
import { AuthState } from '../../auth/states/auth.state';
import { CandidatesQuickListActions } from '../../candidate/actions';
import { CandidatesQuickListComponent } from '../../candidate/containers/candidates-quick-list/candidates-quick-list.component';
import { LocationSearchFilter } from '../../company/models/jobs-list-filters.model';
import { NotificationsShortState } from '../../notifications/states/notifications-short.state';
import { AutoApplyRoute } from '../../shared/constants/routes/auto-apply-routes';
import { CandidateRoute } from '../../shared/constants/routes/candidate-routes';
import { CompanyRoute } from '../../shared/constants/routes/company-routes';
import { JobSeekerRoute } from '../../shared/constants/routes/job-seeker-routes';
import { SubscriptionRoute } from '../../shared/constants/routes/subscription-routes';
import { SurveyRoute } from '../../shared/constants/routes/survey-routes';
import { ConfirmationDialogService } from '../../shared/services/confirmation-dialog.service';
import { SocialIconsService } from '../../shared/services/social-icons.service';
import { UtilsService } from '../../shared/services/utils.service';
import { CoreActions, LayoutActions } from '../actions';
import { ProgressSpinnerComponent } from '../components/progress-spinner.component';
import { NavItem } from '../models/nav-item';
import { NavigationService } from '../services/navigation.service';
import { CoreState } from '../states/core.state';
import { LayoutState } from '../states/layout.states';


@Component({
  selector: 'app-root',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <app-layout>
      <div *ngIf="showGlobalSpinner$ | async" class="loading-indicator">
        <mat-spinner color="accent" [diameter]="30" [strokeWidth]="3"></mat-spinner>
      </div>

      <app-sidenav [open]="showSidenav$ | async" (closeMenu)="closeSidenav()">
        <mat-list-item (click)="closeSidenav()">
          <mat-icon mat-list-icon>close</mat-icon>
          <span mat-line>Close</span>
        </mat-list-item>
        <div *ngIf="loggedIn$ | async">
          <div *ngIf="isSubscriptionPurchased">
            <app-nav-item *ngFor="let item of companyLinks"
                          [item]="item">
              {{item.caption}}
            </app-nav-item>
          </div>
          <div *ngIf="isJobSeeker$ | async">
            <app-nav-item *ngFor="let item of jobSeekerLinks"
                          [item]="item">
              {{item.caption}}
            </app-nav-item>
          </div>
        </div>
      </app-sidenav>
      <app-toolbar (openMenu)="openSidenav()">
        <button mat-button (click)="goToHome()">
          <img src="assets/top-logo.png">
        </button>
        <span class="toolbar-spacer"></span>
        <div *ngIf="(loggedIn$ | async) && (showGlobalSearch$ | async)">
          <app-search-list-form [form]="globalSearchForm"
                                [showLocationSelection]="true"
                                [isGlobalSearch]="true"
                                [locationSearchFilter]="locationSearchFilter"
                                [placeholder]="globalSearchPlaceholder"
                                (submitted)="onSearchSubmit($event)">
          </app-search-list-form>
        </div>
        <span class="toolbar-spacer"></span>
        <button mat-raised-button *ngIf="isCompanyUser$ | async" (click)="showCandidatesQuickList()">
          Quicklist
        </button>
        <button mat-button [matMenuTriggerFor]="notifications" *ngIf="loggedIn$ | async">
          <mat-icon matSuffix>notifications</mat-icon>
          <span *ngIf="shortNotificationCount$ | async"
                matBadge="{{shortNotificationCount$ | async}}"
                matBadgeColor="warn">
          </span>
        </button>
        <mat-menu #notifications>
          <app-notifications-short></app-notifications-short>
        </mat-menu>
        <button mat-button [matMenuTriggerFor]="menu">
          <mat-icon matSuffix>account_circle</mat-icon>
        </button>
        <mat-menu #menu="matMenu">
          <div *ngIf="!(loggedIn$ | async)">
            <button (click)="goToLogin()" mat-menu-item>
              <mat-icon matSuffix>forward</mat-icon>
              Sign In
            </button>
          </div>
          <div *ngIf="loggedIn$ | async">
            <button (click)="goToAccountPage()" *ngIf="!(isJobSeeker$ | async)" mat-menu-item>
              <mat-icon matSuffix>account_box</mat-icon>
              Account
            </button>
            <button (click)="logout()" mat-menu-item>
              <mat-icon matSuffix>backspace</mat-icon>
              Sign Out
            </button>
            <div *ngIf="isJobSeeker$ | async">
              <button (click)="goToMyJSProfile()" mat-menu-item>
                <mat-icon matSuffix>account_box</mat-icon>
                My Profile
              </button>
            </div>
            <div *ngIf="isJobSeeker$ | async">
              <button (click)="goToMyJSSettings()" mat-menu-item>
                <mat-icon matSuffix>settings</mat-icon>
                Settings
              </button>
            </div>
          </div>
        </mat-menu>
        <span>
          <mat-spinner *ngIf="applicationBusy$ | async" color="accent" [diameter]="30" [strokeWidth]="3"></mat-spinner>
        </span>
      </app-toolbar>
      <router-outlet></router-outlet>
    </app-layout>
  `,
  styles: [`
    .toolbar-spacer {
      flex: 1 1 auto;
    }

    .loading-indicator {
      position: fixed;
      z-index: 999;
      height: 2em;
      width: 2em;
      overflow: show;
      margin: auto;
      top: 0;
      left: 0;
      bottom: 0;
      right: 0;
    }

    .loading-indicator:before {
      content: '';
      display: block;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 0.3);
    }
  `],
})
export class AppComponent implements OnInit {
  @Select(CoreState.applicationBusy) applicationBusy$: Observable<boolean>;
  @Select(CoreState.showGlobalSpinner) showGlobalSpinner$: Observable<boolean>;
  @Select(CoreState.showGlobalSearch) showGlobalSearch$: Observable<boolean>;
  @Select(LayoutState.showSidenav) showSidenav$: Observable<boolean>;
  @Select(AuthState.isAuthorized) loggedIn$: Observable<boolean>;
  @Select(AuthState.isCompanyUser) isCompanyUser$: Observable<boolean>;
  @Select(AuthState.isJobSeeker) isJobSeeker$: Observable<boolean>;
  @Select(AuthState.user) user$: Observable<any>;
  @Select(NotificationsShortState.shortNotificationCount) shortNotificationCount$: Observable<number>;

  public ProgressSpinnerComponent = ProgressSpinnerComponent;
  public companyLinks: NavItem[];
  public jobSeekerLinks: NavItem[];
  public locationSearchFilter = LocationSearchFilter;

  public globalSearchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
    location: new FormControl(''),
  });

  constructor(private actions$: Actions,
              private cdRef: ChangeDetectorRef,
              private store: Store,
              private navigationService: NavigationService,
              private socialIconsService: SocialIconsService,
              private router: Router,
              private confirmationDialogService: ConfirmationDialogService,
              private dialog: MatDialog) {
  }

  private get user(): LoggedUser {
    return this.store.selectSnapshot(AuthState.user);
  }

  ngOnInit(): void {
    this.socialIconsService.setSocialIcons();
    this.store.dispatch(new CoreActions.DispatchActionsOnInit());
    this.detectNavigationChanges();
    this.user$.subscribe(() => {
      this.initializeCompanyLinks();
      this.initializeJobSeekerLinks();
    });
  }

  onSearchSubmit(value) {
    forkJoin(
      this.store.dispatch(new CoreActions.SetGlobalSearchParam(value.search)),
      this.store.dispatch(new CoreActions.SetGlobalLocationParam(value.location))
    );
    this.store.selectSnapshot(AuthState.isCompanyUser) ? this.goToJobSeekerListSearch() : this.goToJobListSearch();
    this.globalSearchForm.reset();
  }

  goToHome() {
    this.closeSidenav();
    this.navigationService.goToHomePage();
  }

  closeSidenav() {
    this.store.dispatch(new LayoutActions.CloseSidenav());
  }

  openSidenav() {
    this.store.dispatch(new LayoutActions.OpenSidenav());
  }

  goToLogin() {
    this.closeSidenav();
    this.navigationService.goToLoginPage();
  }

  logout() {
    this.closeSidenav();
    this.confirmationDialogService.openConfirmationDialog({
      message: `Are you sure you want to logout?`,
      callback: this.provideLogOut.bind(this),
      confirmationText: `Logout`,
      title: `Logout`,
      dismissible: true
    });
  }

  goToMyPublicCompanyProfile() {
    this.closeSidenav();
    this.navigationService.goToCompanyProfileViewPage(this.user.company.id.toString());
  }

  goToMyCompanyProfile() {
    this.closeSidenav();
    this.navigationService.goToCompanyProfileEditPage(this.user.company.id.toString());
  }

  goToMyJSProfile() {
    this.closeSidenav();
    this.navigationService.goToJobSeekerProfileEditPage(this.user.job_seeker.id.toString());
  }

  goToAccountPage() {
    this.navigationService.goToAccountPage();
  }

  goToMyJSSettings() {
    this.closeSidenav();
    this.navigationService.goToJobSeekerProfileSettings(this.user.job_seeker.id.toString());
  }

  goToJobListSearch() {
    this.closeSidenav();
    this.navigationService.goToJobSearchPage();
  }

  goToJobSeekerListSearch() {
    this.closeSidenav();
    this.navigationService.goToJobSeekerList();
  }

  showCandidatesQuickList() {
    this.store.dispatch(new CandidatesQuickListActions.GetCandidatesQuickList()).subscribe(() => {
      this.provideQuickListDialog();
    });
  }

  get globalSearchPlaceholder() {
    return this.store.selectSnapshot(AuthState.isCompanyUser) ? 'Skill, keyword' : 'Job title, company, keyword';
  }

  get isSubscriptionPurchased() {
    return this.store.selectSnapshot(AuthState.isCompanyUser)
      && this.store.selectSnapshot(AuthState.isSubsctiptionPurchased);
  }

  private provideLogOut() {
    this.store.dispatch(new AuthActions.Logout());
  }

  private detectNavigationChanges() {
    this.router.events.subscribe(
      (event: any) => {
        if (event instanceof NavigationEnd) {
          const contentContainer = document.querySelector('.mat-sidenav-content') || UtilsService.nativeWindow;
          contentContainer.scrollTop = 0;
        }
      }
    );
  }

  private provideQuickListDialog() {
    const dialogRef = this.dialog.open(CandidatesQuickListComponent, {
      width: '80%'
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }

  private initializeCompanyLinks() {
    if (this.user && this.user.company) {
      this.companyLinks = [
        {
          caption: 'My Company',
          icon: 'group',
          children: [
            {
              caption: 'Profile',
              routerLink: CompanyRoute
                .getFullRouteWithId(CompanyRoute.companyProfileEditRoute, CompanyRoute.id, this.user.company.id.toString()),
              icon: 'account_box'
            },
            {
              caption: 'Users',
              routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyUsersListRoute),
              icon: 'group'
            },
            {
              caption: 'Calendar',
              routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyCalendarRoute),
              icon: 'calendar_today'
            },
            {
              caption: 'Manage Subscription',
              routerLink: SubscriptionRoute.getFullRoute(SubscriptionRoute.manageSubsctiptionRoute),
              icon: 'add_shopping_cart'
            },
            {
              caption: 'Questionnaire',
              routerLink: SurveyRoute.getFullRoute(SurveyRoute.questionListRoute),
              icon: 'question_answer'
            },
            {
              caption: 'Reports',
              routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyReports),
              icon: 'assessment'
            },
            {
              caption: 'Letter Templates',
              routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyLetterTemplatesList),
              icon: 'email'
            }
          ]
        },
        {
          caption: 'Dashboard',
          routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyDashboard),
          icon: 'dashboard'
        },
        {
          caption: 'Jobs',
          routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyJobListRoute),
          icon: 'list'
        },
        {
          caption: 'Create New Job',
          routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyJobCreateRoute),
          icon: 'create'
        },
        {
          caption: 'Dummy Job Creator (TEST)',
          routerLink: CompanyRoute.getFullRoute(CompanyRoute.dummyData),
          icon: 'dashboard'
        },
        {
          caption: 'Candidates',
          routerLink: CandidateRoute.getFullRoute(CandidateRoute.candidateList),
          icon: 'view_list'
        },
        {
          caption: 'Job Seeker List',
          routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerList),
          icon: 'view_list'
        },
        {
          caption: 'Purchased List',
          routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerPurchasedList),
          icon: 'view_list'
        },
        {
          caption: 'Saved List',
          routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerSavedList),
          icon: 'view_list'
        }
      ];
    }

  }

  private initializeJobSeekerLinks() {
    this.jobSeekerLinks = [
      {
        caption: 'Dashboard',
        routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerDashboardPage),
        icon: 'dashboard'
      },
      {
        caption: 'Find job',
        routerLink: CompanyRoute.getFullRoute(CompanyRoute.companyJobSearchRoute),
        icon: 'find_in_page'
      },
      {
        caption: 'Auto Apply',
        routerLink: AutoApplyRoute.getFullRoute(AutoApplyRoute.autoApplyListRoute),
        icon: 'list'
      },
      {
        caption: 'Applied Jobs',
        routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerAppliedJobs),
        icon: 'spellcheck'
      },
      {
        caption: 'Saved Jobs',
        routerLink: JobSeekerRoute.getFullRoute(JobSeekerRoute.jobSeekerSavedJobs),
        icon: 'star_rate'
      }
    ];
  }
}
