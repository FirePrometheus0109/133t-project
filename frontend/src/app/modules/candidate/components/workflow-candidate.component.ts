import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MatButtonToggleChange } from '@angular/material/button-toggle';
import { Store } from '@ngxs/store';
import { CoreActions } from '../../core/actions';
import { CoreState } from '../../core/states/core.state';
import { CandidateStatusEnum, Enums } from '../../shared/models/enums.model';
import { CandidateItem } from '../models/candidate-item.model';


@Component({
  selector: 'app-workflow-candidate',
  template: `
    <div *ngxPermissionsOnly="['change_candidatestatus']">
      <mat-button-toggle-group (change)="onChangeWorkflowStatus($event)"
                               [disabled]="forDisplay"
                               [value]="status">
        <mat-button-toggle *ngFor="let key of (CandidateStatusEnum | enumKeys)"
                           value="{{key}}"
                           checked="{{status === key}}"
                           [matTooltip]="CandidateStatusEnum[key]"
                           [disabled]="status === REJECTED || forDisplay">
          <mat-icon matSuffix>{{getIcon(key)}}</mat-icon>
        </mat-button-toggle>
        <mat-button-toggle [value]="RESTORE"
                           [matTooltip]="restoreTooltipValue"
                           *ngIf="status === REJECTED && !forDisplay">
          <mat-icon matSuffix>restore</mat-icon>
        </mat-button-toggle>
      </mat-button-toggle-group>
    </div>
  `,
  styles: [`
    :host {
      display: flex;
      justify-content: center;
    }
  `]
})
export class WorkflowCandidateComponent implements OnInit {
  @Input() candidate: CandidateItem;
  @Input() candidateId: number;
  @Input() candidateStatus: number;
  @Input() quickViewMode = false;
  @Input() forDisplay = false;
  @Input() enums: Enums;
  @Output() change = new EventEmitter();

  public status: CandidateStatusEnum;
  CandidateStatusEnum: any;
  private restoreTooltip = `This will restore candidate at the step she/he was before rejection`;

  REJECTED = 'REJECTED';
  RESTORE = 'RESTORE';

  private WorkflowStatusIconMap = {
    'APPLIED': 'list',
    'SCREENED': 'remove_red_eye',
    'INTERVIEWED': 'assignment',
    'OFFERED': 'local_offer',
    'HIRED': 'done_all',
    'REJECTED': 'cancel_presentation',
  };

  private CandidateWorkflowQuickViewEnum = {
    REJECTED: 'Rejected'
  };

  constructor(private store: Store) {
  }

  ngOnInit() {
    (this.quickViewMode) ? this.CandidateStatusEnum = this.CandidateWorkflowQuickViewEnum :
      this.CandidateStatusEnum = this.store.selectSnapshot(CoreState.CandidateStatusEnum);
    (this.candidateStatus) ? this.setStatus(this.candidateStatus, true) :
      this.setStatus(this.setInitialStatus(this.candidate.status.name), true);
  }

  getIcon(key) {
    return this.WorkflowStatusIconMap[key];
  }

  onChangeWorkflowStatus(result: MatButtonToggleChange) {
    this.setStatus(result.value);
  }

  private setStatus(status, initial?) {
    this.status = status;
    if (status === this.RESTORE) {
      this.restoreStatus();
    } else {
      if (!initial) {
        this.store.dispatch(new CoreActions.UpdateCandidateStatus(this.setCandidateId(), this.status)).subscribe(() => {
          this.change.emit({status: this.status});
        });
      }
    }
  }

  restoreStatus() {
    this.store.dispatch(new CoreActions.RestoreCandidateStatus(this.setCandidateId())).subscribe(() => {
      this.change.emit({action: 'RESTORE_STATUS'});
    });
  }

  public get restoreTooltipValue() {
    return this.restoreTooltip;
  }

  private setCandidateId() {
    if (this.candidateId) {
      return this.candidateId;
    } else {
      return this.candidate.id;
    }
  }

  private setInitialStatus(initStatus) {
    return Object.keys(this.enums.CandidateStatusEnum).find(key => this.enums.CandidateStatusEnum[key] === initStatus);
  }
}
