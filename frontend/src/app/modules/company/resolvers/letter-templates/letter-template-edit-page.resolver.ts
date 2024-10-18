import { Injectable } from '@angular/core';
import { Resolve } from '@angular/router';
import { ActivatedRouteSnapshot } from '@angular/router';
import { Store } from '@ngxs/store';
import { forkJoin, Observable } from 'rxjs';
import { LetterTemplateManageActions } from '../../actions';


@Injectable()
export class LetterTemplateEditPageResolver implements Resolve<Observable<any>> {
  constructor(private store: Store) {
  }

  resolve(route: ActivatedRouteSnapshot) {
    /* tslint:disable */
    return forkJoin(
      this.store.dispatch(new LetterTemplateManageActions.ResetCurrentLetterTemplate()),
      this.store.dispatch(new LetterTemplateManageActions.SetEditMode(true)),
      this.store.dispatch(new LetterTemplateManageActions.LoadLetterTemplatesEventTypes()),
      this.store.dispatch(new LetterTemplateManageActions.LoadLetterTemplateData(route.params.id)),
    );
    /* tslint:enable */
  }
}
