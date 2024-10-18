import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { MatButtonToggleChange, MatDialog } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { NavigationService } from '../../../core/services/navigation.service';
import { CoreState } from '../../../core/states/core.state';
import { Enums } from '../../../shared/models/enums.model';
import { CandidatesQuickListActions } from '../../actions';
import { CandidateStatus } from '../../models/candidate-item.model';
import { CandidateQuickListItem } from '../../models/candidate-quick-list.model';
import { CandidatesQuickListState } from '../../states/candidates-quick-list.state';


@Component({
  selector: 'app-candidates-quick-list',
  templateUrl: './candidates-quick-list.component.html',
  styleUrls: ['./candidates-quick-list.component.scss']
})
export class CandidatesQuickListComponent {
  @Select(CoreState.CandidateStatuses) CandidateStatuses$: Observable<CandidateStatus[]>;
  @Select(CoreState.enums) enums$: Observable<Enums>;
  @Select(CandidatesQuickListState.candidatesQuickList) candidatesQuickList$: Observable<CandidateQuickListItem[]>;

  public searchForm: FormGroup = new FormGroup({
    search: new FormControl(''),
  });

  constructor(private store: Store, private navigationService: NavigationService, private dialog: MatDialog) {
  }

  statusChanged(event: MatButtonToggleChange) {
    this.store.dispatch(new CandidatesQuickListActions.UpdateQuickListParams({status: event.value}));
  }

  onSearchSubmit() {
    this.store.dispatch(new CandidatesQuickListActions.UpdateQuickListParams(this.searchForm.value));
  }

  navigateToJobPage(jobId: number) {
    this.dialog.closeAll();
    this.navigationService.goToCompanyJobViewDetailsPage(jobId.toString());
  }

  navigateToCandidateProfile(candidateId: number) {
    this.dialog.closeAll();
    this.navigationService.goToCandidateProfileViewPage(candidateId.toString());
  }

  onChangeCandidate(data) {
    // Reload list after restore status
    if (data && data['action'] && data['action'] === 'RESTORE_STATUS') {
      this.store.dispatch(new CandidatesQuickListActions
        .GetCandidatesQuickList(this.store.selectSnapshot(CandidatesQuickListState.params)));
    }
  }
}
