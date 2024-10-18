import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { InputLengths } from '../../shared/constants/validators/input-length';
import { Photo } from '../../shared/models';
import { Address } from '../../shared/models/address.model';
import { UtilsService } from '../../shared/services/utils.service';
import { ValidationService } from '../../shared/services/validation.service';
import { CompanyProfilePageActions } from '../actions';
import { CompanyService } from '../services/company.service';
import { CompanyProfilePageState } from '../states/company-profile-page.state';


@Component({
  selector: 'app-edit-company-profile-page',
  template: `
    <mat-card>
      <img mat-card-avatar class="big-avatar" [src]="(photo$ | async)?.original">
      <app-material-file-upload (complete)="onFileComplete($event)" [target]="targetFilesUpload" param="photo">
      </app-material-file-upload>

      <mat-accordion>
        <mat-expansion-panel [expanded]="true">
          <mat-expansion-panel-header>
            <mat-panel-title>Main info</mat-panel-title>
          </mat-expansion-panel-header>
          <app-company-profile-info-form (submitted)="onSubmitMainInfo($event)"
                                         [pending]="pending$ | async"
                                         [errors]="errors$ | async"
                                         [initialData]="(initialData$ | async)"
                                         [form]="infoForm">
            <mat-action-row>
              <button type="submit" mat-raised-button color="primary" [disabled]='!infoForm.valid'>
                Save
                <mat-icon matSuffix>save</mat-icon>
              </button>
              <button type="button" mat-raised-button color="primary"
                      (click)="discardSection(infoForm)">
                Discard
                <mat-icon matSuffix>close</mat-icon>
              </button>
            </mat-action-row>
          </app-company-profile-info-form>
        </mat-expansion-panel>

        <mat-expansion-panel>
          <mat-expansion-panel-header>
            <mat-panel-title>Address</mat-panel-title>
          </mat-expansion-panel-header>
          <app-address-component (submitted)="onSubmitAddress($event)"
                                 [pending]="pending$ | async"
                                 [errors]="errors$ | async"
                                 [initialData]="(initialData$ | async)?.address"
                                 [form]="addressForm">
            <mat-action-row>
              <button type="submit" mat-raised-button color="primary" [disabled]='!addressForm.valid'>
                Save Address
                <mat-icon matSuffix>save</mat-icon>
              </button>
              <button type="button" mat-raised-button color="primary"
                      (click)="discardSection(addressForm)">
                Discard
                <mat-icon matSuffix>close</mat-icon>
              </button>
            </mat-action-row>
          </app-address-component>
        </mat-expansion-panel>
      </mat-accordion>
    </mat-card>
  `,
  styles: [`
    mat-card-title,
    mat-card-content {
      display: flex;
      justify-content: center;
    }

    .mat-card-avatar.big-avatar {
      object-fit: cover;
      height: 200px;
      width: 200px;
    }
  `],
})
export class EditCompanyProfilePageComponent implements OnInit {
  @Select(CompanyProfilePageState.pending) pending$: Observable<boolean>;
  @Select(CompanyProfilePageState.errors) errors$: Observable<any>;
  @Select(CompanyProfilePageState.initialData) initialData$: Observable<any>;
  @Select(CompanyProfilePageState.photo) photo$: Observable<Photo>;

  public targetFilesUpload: string;
  private cId: number;

  infoForm: FormGroup = new FormGroup({
    description: new FormControl('', Validators.maxLength(InputLengths.descriptions)),
    phone: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.phone)])),
    fax: new FormControl('', Validators.maxLength(InputLengths.phone)),
    email: new FormControl('',
      Validators.compose([ValidationService.emailValidator, Validators.maxLength(InputLengths.email)])),
    website: new FormControl('', Validators.maxLength(InputLengths.website)),
    industry: new FormControl('', Validators.compose([Validators.required, ValidationService.selectListObjectValidator])),
    name: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.names)])),
  });

  addressForm: FormGroup = new FormGroup({
    city: new FormControl('', Validators.required),
    country: new FormControl('', Validators.required),
    zip: new FormControl('', Validators.compose([Validators.required, Validators.maxLength(InputLengths.zip)])),
    address: new FormControl('', Validators.required),
  }, ValidationService.addressValidator);

  constructor(private store: Store, private route: ActivatedRoute,
              private companyService: CompanyService) {
  }

  ngOnInit() {
    this.cId = this.route.snapshot.params['id'];
    this.targetFilesUpload = this.companyService.getCompanyPhotoRoute(this.cId);
  }

  onSubmitAddress(formData: Address) {
    this.store.dispatch(
      new CompanyProfilePageActions.PartialUpdate('address', this.cId, {address: UtilsService.prepareAddressData(formData)}),
    );
  }

  onFileComplete(data: any) {
    this.store.dispatch(new CompanyProfilePageActions.UpdateLogo(this.cId, data['photo']));
  }

  onSubmitMainInfo(formData: any) {
    formData.industry = formData.industry.id;
    this.store.dispatch(
      new CompanyProfilePageActions.PartialUpdate('', this.cId, formData),
    );
  }

  discardSection(form: FormGroup) {
    if (form.contains('city')) {
      form.patchValue(this.store.selectSnapshot(CompanyProfilePageState.initialData).address);
    } else {
      form.patchValue(this.store.selectSnapshot(CompanyProfilePageState.initialData));
    }
  }
}
