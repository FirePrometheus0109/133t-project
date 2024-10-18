import { Component, OnInit } from '@angular/core';
import { Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/internal/operators';
import { CoreState } from '../../core/states/core.state';
import { Industry } from '../models/industry.model';
import { BaseFormComponent } from './base-form.component';


@Component({
  selector: 'app-industry-select-form',
  template: `
    <mat-card>
      <mat-card-title>
        <ng-content select="title"></ng-content>
      </mat-card-title>
      <mat-card-content>
        <form [formGroup]="form" (ngSubmit)="submit()">
          <mat-form-field class="search-form-class">
            <input type="text" placeholder="Industry" aria-label="Industry" matInput formControlName="industry" [matAutocomplete]="auto">
            <mat-autocomplete #auto="matAutocomplete" [displayWith]="displayFn">
              <mat-option *ngFor="let industry of filteredIndustries$ | async" [value]="industry">
                {{industry.name}}
              </mat-option>
            </mat-autocomplete>
          </mat-form-field>
          <app-control-messages [form]="form"
                                [control]="f.industry"
                                [submitted]="isSubmitted"
                                [errors]="errors">
          </app-control-messages>
          <ng-content select="body"></ng-content>
        </form>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .search-form-class {
      width: 400px;
    }
  `],
})
export class IndustrySelectFormComponent extends BaseFormComponent implements OnInit {

  industries: Industry[];
  filteredIndustries$: Observable<Industry[]>;

  constructor(public store: Store) {
    super();
  }

  ngOnInit() {
    this.industries = this.store.selectSnapshot(CoreState.industries);
    if (this.form && this.form.controls.industry) {
      this.filteredIndustries$ = this.form.controls.industry.valueChanges
        .pipe(
          startWith<string | Industry | null>(''),
          map(value => typeof value === 'string' ? value : (value) ? value.name : ''),
          map(name => name ? this._filter(name) : this.industries.slice())
        );
    }
    super.ngOnInit();
  }

  displayFn(industry?: Industry): string | undefined {
    return industry ? industry.name : undefined;
  }

  private _filter(name: string) {
    const filterValue = name.toLowerCase();
    return this.industries.filter(industry => industry['name'].toLowerCase().includes(filterValue));
  }
}
