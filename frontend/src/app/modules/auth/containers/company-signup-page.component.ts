import { Component, OnInit } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CompanySignupPageActions } from '../actions';
import { SignupCredentials } from '../models/credentials.model';
import { CompanySignupFormState } from '../states/company-signup-page.state';


@Component({
  selector: 'app-company-signup-page',
  template: `
    <app-company-signup-form
        (submitted)="onSubmit($event)"
        [pending]="pending$ | async"
        [errors]="errors$ | async">
    </app-company-signup-form>
  `,
  styles: [],
})
export class CompanySignupPageComponent implements OnInit {
  @Select(CompanySignupFormState.pending) pending$: Observable<boolean>;
  @Select(CompanySignupFormState.errors) errors$: Observable<any>;

  constructor(private store: Store) {
  }

  ngOnInit() {
  }

  onSubmit(credentials: SignupCredentials) {
    this.store.dispatch(new CompanySignupPageActions.Signup(credentials));
  }
}
