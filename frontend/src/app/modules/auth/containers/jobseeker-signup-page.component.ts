import { Component, OnInit } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { JobSeekerSignupPageActions } from '../actions';
import { SignupCredentials } from '../models/credentials.model';
import { JobSeekerSignupFormState } from '../states/js-signup-page.state';


@Component({
  selector: 'app-jobseeker-signup-page',
  template: `
    <app-job-seeker-signup-form (submitted)="onSubmit($event)"
                                [pending]="pending$ | async"
                                [errors]="errors$ | async">
    </app-job-seeker-signup-form>
  `,
  styles: [],
})
export class JobSeekerSignupPageComponent implements OnInit {
  @Select(JobSeekerSignupFormState.pending) pending$: Observable<boolean>;
  @Select(JobSeekerSignupFormState.errors) errors$: Observable<any>;

  constructor(private store: Store) {
  }

  ngOnInit() {
  }

  onSubmit(credentials: SignupCredentials) {
    this.store.dispatch(new JobSeekerSignupPageActions.Signup(credentials));
  }
}
