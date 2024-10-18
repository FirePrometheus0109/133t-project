import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-jsp-about-view',
  templateUrl: './jsp-about-view.component.html',
  styleUrls: ['./jsp-about-view.component.scss']
})
export class JspAboutViewComponent {
  @Input() initialData: string;
  @Output() changeToEditMode = new EventEmitter<boolean>();
}
