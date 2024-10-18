import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Enums } from '../../../shared/models/enums.model';
import { CandidateQuickListItem } from '../../models/candidate-quick-list.model';


@Component({
  selector: 'app-quick-list-item',
  templateUrl: './quick-list-item.component.html',
  styleUrls: ['./quick-list-item.component.scss']
})
export class QuickListItemComponent {
  @Input() quickListItem: CandidateQuickListItem;
  @Input() enums: Enums;
  @Output() change = new EventEmitter<object>();
  @Output() navigateToProfile = new EventEmitter<number>();
  @Output() navigateToJob = new EventEmitter<number>();

  onChangeCandidateWorkflow(data) {
    this.change.emit(data);
  }
}
