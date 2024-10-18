import { OnDestroy } from '@angular/core';
import { MatSelect } from '@angular/material';
import { Observable, ReplaySubject, Subject } from 'rxjs';
import { take, takeUntil } from 'rxjs/operators';

export interface ObjectWithTitle {
  title: string;
  [key: string]: any;
}

export type ValidOption = ObjectWithTitle | string;


export abstract class SelectorWithSearchBaseComponent implements OnDestroy {
  select: MatSelect;
  comparingKey = 'title';

  protected _onDestroy = new Subject<void>();

  ngOnDestroy() {
    this._onDestroy.next();
    this._onDestroy.complete();
  }

  setInitialValue(options: Observable<ValidOption[]> | ReplaySubject<ValidOption[]>) {
    options
      .pipe(take(1), takeUntil(this._onDestroy))
      .subscribe(() => {
        // TODO: make type restructuration
        this.select.compareWith = (a: ValidOption, b: ValidOption) => {
          if (
               typeof a === 'string'
            || typeof a === 'number'
            || typeof b === 'string'
            || typeof b === 'number'
          ) {
            return a === b;
          }
          else {
            return a && b && a[this.comparingKey] === b[this.comparingKey];
          }
        };
      });
  }
}
