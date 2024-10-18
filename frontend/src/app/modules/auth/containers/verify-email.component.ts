import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { VerifyEmailActions } from '../actions';
import { VerifyEmailState } from '../states/verify-email.state';


@Component({
  selector: 'app-verify-email',
  template: `
    <mat-card>
      <mat-card-title>
        <p *ngIf="verified$ | async">Email Verified!</p>
        <p *ngIf="pending$ | async">Verification Email...</p>
      </mat-card-title>
      <mat-card-content>
        <mat-spinner
            *ngIf="pending$ | async"
            style="margin:0 auto;"
            mode="indeterminate">
        </mat-spinner>
        <h2 *ngIf="verified$ | async">DONE!</h2>
      </mat-card-content>
    </mat-card>
  `,
  styles: [],
})
export class VerifyEmailComponent implements OnInit {
  @Select(VerifyEmailState.pending) pending$: Observable<boolean>;
  @Select(VerifyEmailState.verified) verified$: Observable<boolean>;

  constructor(private store: Store,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.store.dispatch(new VerifyEmailActions.VerifyEmail(params['token']));
    });
  }
}
