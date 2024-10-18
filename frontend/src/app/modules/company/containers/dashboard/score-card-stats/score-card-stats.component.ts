import { Component } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { CandidateStatus } from 'src/app/modules/candidate/models/candidate-item.model';
import { CoreState } from 'src/app/modules/core/states/core.state';
import { CheckBoxHelper } from 'src/app/modules/shared/helpers/list-checkbox.helper';
import { CompanyDashboardActions } from '../../../actions';
import { ActivityStats } from '../../../models/company-reports.model';
import { ScoreCardMode } from '../../../models/scorecard-mode.model';
import { CompanyDashboardState } from '../../../states/company-dashboard.state';


@Component({
  selector: 'app-score-card-stats',
  templateUrl: './score-card-stats.component.html',
  styleUrls: ['./score-card-stats.component.css']
})
export class ScoreCardStatsComponent {
  @Select(CompanyDashboardState.statCardData) cardData$: Observable<ActivityStats[]>;
  @Select(CompanyDashboardState.allStatCardData) allStatCardData$: Observable<ActivityStats[]>;
  @Select(CompanyDashboardState.statCardMode) cardMode$: Observable<ScoreCardMode>;

  @Select(CoreState.CandidateStatuses) statuses$: Observable<CandidateStatus[]>;

  checkBoxHelper = new CheckBoxHelper('edit-score-card-checkbox');

  constructor(private store: Store) {
  }

  onToggleScoreCard() {
    this.store.dispatch(new CompanyDashboardActions.LoadAllScoreCardData());
    this.store.dispatch(new CompanyDashboardActions.ToggleScoreCardMode());
  }

  isCardViewMode(mode: ScoreCardMode) {
    return mode === ScoreCardMode.VIEW;
  }

  getSelectedStatuses() {
    this.store.dispatch(new CompanyDashboardActions.SetScoreCardSettings(
      this.checkBoxHelper.getAllSelectedItems()));
  }

  isStatSelected(id: number) {
    const selectedStats = this.store.selectSnapshot(CompanyDashboardState.statCardDataIds);
    return selectedStats.includes(id);
  }
}
