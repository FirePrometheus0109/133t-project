import { Component, EventEmitter, Input, Output } from '@angular/core';
import { SkillItem } from '../../../../shared/models/skill.model';


@Component({
  selector: 'app-jsp-skills-view',
  templateUrl: './jsp-skills-view.component.html',
  styleUrls: ['./jsp-skills-view.component.scss']
})
export class JspSkillsViewComponent {
  @Input() initialData: SkillItem[];
  @Output() changeToEditMode = new EventEmitter<boolean>();
}
