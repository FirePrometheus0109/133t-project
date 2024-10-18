import { Component, EventEmitter, Input, Output } from '@angular/core';
import { DateTimeHelper } from '../../../../shared/helpers/date-time.helper';
import { LetterTemplateItem } from '../../../models/letter-templates.model';


@Component({
  selector: 'app-letter-template-list-item',
  templateUrl: './letter-template-list-item.component.html',
  styleUrls: ['./letter-template-list-item.component.scss']
})
export class LetterTemplateItemComponent {
  @Input() letterTemplateItem: LetterTemplateItem;
  @Output() deleteLetterTemplate = new EventEmitter<LetterTemplateItem>();
  @Output() editLetterTemplate = new EventEmitter<number>();
  @Output() viewLetterTemplate = new EventEmitter<number>();

  getModifiedDate() {
    return DateTimeHelper.getDate(this.letterTemplateItem.modified_at);
  }
}
