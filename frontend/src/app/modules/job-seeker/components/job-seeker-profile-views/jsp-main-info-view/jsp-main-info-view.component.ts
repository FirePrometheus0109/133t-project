import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-jsp-main-info-view',
  templateUrl: './jsp-main-info-view.component.html',
  styleUrls: ['./jsp-main-info-view.component.scss']
})
export class JspMainInfoViewComponent {
  @Input() initialData: any;
  @Input() phoneNumber: any;
  @Output() changeToEditMode = new EventEmitter<boolean>();
}
