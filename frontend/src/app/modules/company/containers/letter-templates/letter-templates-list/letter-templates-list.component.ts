import { Component, OnInit } from '@angular/core';
import { MatAutocompleteSelectedEvent, PageEvent } from '@angular/material';
import { Select, Store } from '@ngxs/store';
import { Observable, Subject } from 'rxjs';
import { debounceTime } from 'rxjs/internal/operators';
import { environment } from '../../../../../../environments/environment';
import { NavigationService } from '../../../../core/services/navigation.service';
import { GridViewHelper } from '../../../../shared/helpers/grid-view.helper';
import { SortingFilter } from '../../../../shared/models/filters.model';
import { DEFAULT_PAGINATED_OPTIONS } from '../../../../shared/models/paginated-data.model';
import { ConfirmationDialogService } from '../../../../shared/services/confirmation-dialog.service';
import { LetterTemplatesListActions } from '../../../actions';
import { LetterTemplateItem } from '../../../models/letter-templates.model';
import { LetterTemplatesListState } from '../../../states/letter-templates/letter-templates-list-page.state';


@Component({
  selector: 'app-letter-templates-list',
  templateUrl: './letter-templates-list.component.html',
  styleUrls: ['./letter-templates-list.component.scss']
})
export class LetterTemplatesListComponent implements OnInit {
  @Select(LetterTemplatesListState.count) count$: Observable<number>;
  @Select(LetterTemplatesListState.pageSize) pageSize$: Observable<number>;
  @Select(LetterTemplatesListState.templatesSortingFilter) templatesSortingFilter$: Observable<SortingFilter[]>;
  @Select(LetterTemplatesListState.pageSizeOptions) pageSizeOptions$: Observable<number[]>;
  @Select(LetterTemplatesListState.letterTemplatesList) letterTemplatesList$: Observable<LetterTemplateItem[]>;

  private searchUpdated = new Subject();

  constructor(private store: Store,
              private navigationService: NavigationService,
              private confirmationDialogService: ConfirmationDialogService) {
  }

  ngOnInit() {
    this.searchUpdated.pipe(debounceTime(environment.searchDebounceTime)).subscribe((searchValue: string) => {
      this.onSearchChanged(searchValue);
    });
  }

  onPageChanged(event: PageEvent) {
    this.store.dispatch(new LetterTemplatesListActions.UpdateListParams(GridViewHelper.getPaginationParams(event)));
  }

  onSortingFilterSelect(event: MatAutocompleteSelectedEvent) {
    const paramsWithDefaultPagination = GridViewHelper.updateParams(this.currentListParams, DEFAULT_PAGINATED_OPTIONS);
    this.store.dispatch(new LetterTemplatesListActions
      .UpdateListParams(GridViewHelper.updateWithSortingParams(paramsWithDefaultPagination, event['value'])));
  }

  provideSearch(event: any) {
    this.searchUpdated.next(event.target.value);
  }

  onSearchChanged(search: string) {
    const paramsWithDefaultPagination = GridViewHelper.updateParams(this.currentListParams, DEFAULT_PAGINATED_OPTIONS);
    this.store.dispatch(new LetterTemplatesListActions
      .UpdateListParams(GridViewHelper.updateParams(paramsWithDefaultPagination, {search})));
  }

  provideLetterTemplateCreation() {
    this.navigationService.goToLetterTemplateCreatePage();
  }

  provideLetterTemplateDeletion(letterTemplate: LetterTemplateItem) {
    this.confirmationDialogService.openConfirmationDialog({
      message: `Are you sure you want to delete ${letterTemplate.name}?`,
      callback: this.deleteLetterTemplate.bind(this, letterTemplate.id),
      confirmationText: 'Yes',
      negativeText: 'No',
      dismissible: true
    });
  }

  provideEditLetterTemplate(letterTemplateId: number) {
    this.navigationService.goToLetterTemplateEditPage(letterTemplateId.toString());
  }

  provideViewLetterTemplate(letterTemplateId: number) {
    this.navigationService.goToLetterTemplateViewPage(letterTemplateId.toString());
  }

  isCreateButtonDisabled() {
    return this.store.selectSnapshot(LetterTemplatesListState.count) === environment.maxLetterTemplatesCount;
  }

  private deleteLetterTemplate(letterTemplateId: number) {
    this.store.dispatch(new LetterTemplatesListActions.DeleteLetterTemplate(letterTemplateId));
  }

  private get currentListParams() {
    return this.store.selectSnapshot(LetterTemplatesListState.params);
  }
}
