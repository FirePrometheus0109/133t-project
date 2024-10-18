import { Component, Inject, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { environment } from '../../../../environments/environment';
import { User } from '../../auth/models/user.model';
import { AssignCandidateActions } from '../actions';
import { AssignCandidateState } from '../states/assign-candidate.state';


@Component({
  selector: 'app-assign-candidate-modal',
  template: `
    <h4 mat-dialog-title> Assignment </h4>
    <mat-dialog-content style="overflow:unset" *ngIf="!(assignmentResult$ | async)">
      <div style="margin-bottom:20px; display:inline" *ngFor="let user of selectedUser">
        <span>{{user.first_name || user.user?.first_name}}</span>
        <span> {{user.last_name || user.user?.last_name}}</span>
        <button type="button" mat-button (click)="removeUser(user)">
          <mat-icon>close</mat-icon>
        </button>
      </div>
      <div>
        <mat-chip-list>
          <mat-chip *ngFor="let job of selectedJobs.value">{{ job.title }}</mat-chip>
        </mat-chip-list>

        <mat-select
            style="margin-top: 40px; width:40%" placeholder="Select Job Posting" [formControl]="selectedJobs" multiple>
          <mat-option *ngFor="let job of (jobData$ | async)" [value]="job">{{job.title}}</mat-option>
        </mat-select>
        <mat-error *ngIf="selectedUser.length === 0">No user to assign</mat-error>
        <mat-error *ngIf="selectedUser.length > maxAssignedUser">
          You can assign not more than 50 profiles at a time. Select less profiles
        </mat-error>
      </div>
      <mat-dialog-actions>
        <button type="button" mat-raised-button="mat-raised-button"
                [disabled]="!selectedJobs.valid || selectedUser.length === 0"
                *ngxPermissionsOnly="['add_candidate']"
                (click)="assignUsers()" color="primary">
          <span>Assign</span>
        </button>
        <button mat-button [mat-dialog-close]>Cancel</button>
      </mat-dialog-actions>
    </mat-dialog-content>

    <mat-dialog-content *ngIf="(assignmentResult$ | async)">
      <h4>
        Your Assignment Complete. Please see results below
      </h4>
      <div *ngFor="let successAssignment of (assignmentResult$ | async).assigned">
        <mat-icon>done</mat-icon>
        {{successAssignment.candidate}} is successfully assigned to
        <span *ngFor="let jobItem of successAssignment.jobs ">
          {{jobItem}},
        </span>
      </div>
      <div *ngFor="let failedAssignment of (assignmentResult$ | async).already_assigned">
        <mat-icon>sms_failed</mat-icon>
        {{failedAssignment.candidate}} is Already Assigned to
        <span *ngFor="let jobItem of failedAssignment.jobs ">
          {{jobItem}},
        </span>
      </div>
      <mat-dialog-actions>
        <button mat-button [mat-dialog-close]>Got It</button>
      </mat-dialog-actions>
    </mat-dialog-content>
  `,
  styles: []
})
export class AssignCandidateComponent implements OnInit {
  @Select(AssignCandidateState.jobData) jobData$: Observable<Array<object>>;
  @Select(AssignCandidateState.assignmentResult) assignmentResult$: Observable<object>;

  selectedJobs = new FormControl('', Validators.required);
  selectedUser: Array<User>;

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any,
              @Inject(MatDialogRef) public dialogRef: MatDialogRef<any>,
              private store: Store) {
  }

  ngOnInit() {
    this.dialogRef.afterClosed().subscribe(() => {
      this.resetAssignment();
    });

    this.selectedUser = this.modalData.userData.slice();
  }

  get maxAssignedUser() {
    return environment.maxAssignedUser;
  }

  assignUsers() {
    const users = this.selectedUser;
    const jobs = this.selectedJobs.value;

    this.store.dispatch(new AssignCandidateActions.AssignCandidate(users, jobs));
  }

  removeUser(user) {
    this.selectedUser.splice(this.selectedUser.indexOf(user), 1);
  }

  resetAssignment() {
    this.store.dispatch(new AssignCandidateActions.ResetAssignmentWindow());
  }
}
