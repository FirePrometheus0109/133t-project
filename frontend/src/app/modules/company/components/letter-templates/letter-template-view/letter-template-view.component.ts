import { Component, Input } from '@angular/core';
import { LetterTemplateItem } from '../../../models/letter-templates.model';


@Component({
  selector: 'app-letter-template-view',
  templateUrl: './letter-template-view.component.html',
  styleUrls: ['./letter-template-view.component.scss']
})
export class LetterTemplateViewComponent {
  @Input() letterTemplate: LetterTemplateItem;
}
