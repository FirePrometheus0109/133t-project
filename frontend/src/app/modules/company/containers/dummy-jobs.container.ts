import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {BaseFormComponent} from '../../shared/components/base-form.component';
import {ApiService} from '../../shared/services/api.service';
import {CompanyService} from '../services/company.service';


@Component({
  selector: 'app-dummy-jobs-page',
  template: `
      <mat-card>
          <mat-card-title>Add dummy jobs</mat-card-title>
          <mat-card-content>
              <form [formGroup]="form" ngxsForm="login.form" ngxsFormClearOnDestroy="true" (ngSubmit)="submit()">
                  <p>
                      <mat-form-field>
                          <input type="text" matInput placeholder="Title" formControlName="title">
                      </mat-form-field>
                      <app-control-messages [form]="form"
                                            [control]="f.title"
                                            [submitted]="isSubmitted">
                      </app-control-messages>
                  </p>

                  <p>
                      <mat-form-field>
                          <input type="number" matInput placeholder="Amount" formControlName="amount">
                      </mat-form-field>
                      <app-control-messages [form]="form"
                                            [control]="f.amount"
                                            [submitted]="isSubmitted">
                      </app-control-messages>
                  </p>
                  <mat-button-toggle-group class="sendForm">
                      <button type="submit" mat-raised-button (click)="sendForm()">Send form</button>
                  </mat-button-toggle-group>
              </form>
          </mat-card-content>
      </mat-card>
  `,
  styles: [`
      :host {
          display: flex;
          justify-content: center;
          margin: 72px 0;
      }

      .mat-form-field {
          width: 100%;
          min-width: 300px;
      }

      mat-card-title,
      mat-card-content {
          display: flex;
          justify-content: center;
      }
  `],
})
export class DummyJobsComponent extends BaseFormComponent implements OnInit, OnDestroy {

  public form: FormGroup = new FormGroup({
    title: new FormControl(''),
    amount: new FormControl(''),
  });

  get f() {
    return this.form['controls'];
  }

  constructor(private api: ApiService,
              private companyService: CompanyService) {
    super();
  }

  sendForm() {
    this.companyService.setDummyJob(this.form.value).subscribe(() => {
      this.form.reset();
    });
  }

  ngOnInit() {

  }

  ngOnDestroy() {

  }
}
