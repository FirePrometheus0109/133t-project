import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { map } from 'rxjs/internal/operators';
import * as CoreActions from '../../core/actions/core.actions';
import { CoreState } from '../../core/states/core.state';
import { ConfirmationDialogService } from '../services/confirmation-dialog.service';


@Component({
  selector: 'app-purchase-profile-button',
  template: `
    <div *ngxPermissionsOnly="['purchase_js_profile']">
      <div *ngIf="!(profilePurchased$ | async)">
        <button mat-button
                (click)="purchaseProfileBtn()"
                matTooltip="{{generalMsg}}"
                [matTooltipDisabled]="!compactMode">
          <mat-icon matSuffix>shopping_cart</mat-icon>
          <span *ngIf="!compactMode && !(profilePurchased$ | async)">{{generalMsg}}</span>
        </button>
      </div>
    </div>
    <div *ngxPermissionsOnly="['view_purchased_job_seekers']">
      <div *ngIf="(profilePurchased$ | async)">
        <button mat-button
                matTooltip="{{generalMsg}}"
                [disabled]="true"
                [matTooltipDisabled]="!compactMode">
          <mat-icon matSuffix>shopping_cart</mat-icon>
          <span *ngIf="!compactMode">{{generalMsg}}</span>
        </button>
      </div>
    </div>
  `,
  styles: []
})
export class PurchaseProfileButtonComponent implements OnInit {
  @Input() compactMode = false;
  @Output() purchaseComplete = new EventEmitter<any>();
  // id <--
  private _id: any = null;

  @Input()
  set id(id: any) {
    if (id) {
      this.handleInputId(id);
    }
    this._id = id;
  }

  get id(): any {
    return this._id;
  }

  // id -->

  @Input() first_name: string;
  @Input() last_name: string;

  private confirmButtonText = 'Confirm';
  private negativeButtonText = 'Cancel';
  private modalTitle = 'Purchase Profile';
  public generalMsg = 'Purchase Profile';
  public profilePurchased$: Observable<boolean>;

  constructor(private store: Store,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  ngOnInit() {
    if (this.id) {
      this.handleInputId(this.id);
    }
  }

  handleInputId(id: number) {
    this.profilePurchased$ = this.store.select(CoreState.profilePurchased).pipe(
      map(filterFn => filterFn(id)),
    );
    this.profilePurchased$.subscribe((result) => {
      if (result) {
        this.generalMsg = 'Profile Purchased';
      } else {
        this.generalMsg = 'Purchase Profile';
      }
    });
  }

  purchaseProfileBtn() {
    this.confirmationDialogService.openConfirmationDialog({
        message: this.prepareConfirmationMessage(),
        callback: this.purchaseProfile.bind(this),
        confirmationText: `${this.confirmButtonText}`,
        negativeText: `${this.negativeButtonText}`,
        title: `${this.modalTitle}`,
        dismissible: true
      },
    );
  }

  private purchaseProfile() {
    this.store.dispatch(new CoreActions.PurchaseJobSeeker(this.id)).subscribe(() => {
      this.purchaseComplete.emit();
    });
  }

  private prepareConfirmationMessage() {
    return `You are purchasing profile of ${this.first_name} ${this.last_name}`;
  }
}
