import { Component, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import { Store } from '@ngxs/store';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/internal/operators';
import { User } from '../../auth/models/user.model';
import { CoreState } from '../../core/states/core.state';
import { AssignCandidateActions } from '../actions';
import { AssignCandidateComponent } from '../containers/assign-candidate.container';


@Component({
  selector: 'app-assign-candidate-button',
  template: `
    <div *ngxPermissionsOnly="['add_candidate']">
      <div class="tooltip-wrapper" [matTooltip]="getTooltipMessage((profilePurchasedOrCandidate$ | async))">
        <button mat-button [disabled]="!(profilePurchasedOrCandidate$ | async)" (click)="assignToJob()">
          <mat-icon matSuffix>add_to_queue</mat-icon>
          <div *ngIf="shouldShowText">Assign Candidate</div>
        </button>
      </div>
    </div>`,
  styles: []
})
export class AssignCandidateButtonComponent implements OnInit {
  // assignedUser <--
  private _assignedUser: Array<User> = null;
  @Input() shouldShowText = false;
  @Input() isCandidate = false;

  @Input()
  set assignedUser(assignedUser: Array<User>) {
    if (assignedUser) {
      this.handleAssignedUser(assignedUser);
    }
    this._assignedUser = assignedUser.filter((entry, index) => assignedUser.findIndex(a => a.id === entry.id) === index);

  }

  get assignedUser(): Array<User> {
    return this._assignedUser;
  }

  // assignedUser -->
  public profilePurchasedOrCandidate$: Observable<boolean>;
  private allowingMessage = 'Assign this profile to job';
  private restrictiveMessage = 'Purchase this profile to assign it to job posting';

  constructor(public dialog: MatDialog,
              private store: Store) {
  }

  ngOnInit() {
    if (this.assignedUser) {
      this.handleAssignedUser(this.assignedUser);
    }
  }

  get lenInput(): number {
    return this.assignedUser.length;
  }

  getTooltipMessage(isPurchased) {
    if (this.isCandidate) {
      return this.allowingMessage;
    } else {
      return isPurchased ? this.allowingMessage : this.restrictiveMessage;
    }
  }

  handleAssignedUser(assignedUser: Array<User>) {
    if (assignedUser && assignedUser[0]) {
      if (this.isCandidate) {
        this.profilePurchasedOrCandidate$ = of(this.isCandidate);
      } else {
        this.profilePurchasedOrCandidate$ = this.store.select(CoreState.profilePurchased).pipe(
          map(filterFn => filterFn(assignedUser[0].id)),
        );
      }
    }
  }

  assignToJob() {
    this.store.dispatch(new AssignCandidateActions.LoadInitialData());
    const dialogRef = this.dialog.open(AssignCandidateComponent, {
      width: '90%',
      height: '400px',
      data: {
        userData: this.assignedUser
      }
    });
    dialogRef.afterClosed().subscribe(() => {
      dialogRef.close();
    });
  }
}
