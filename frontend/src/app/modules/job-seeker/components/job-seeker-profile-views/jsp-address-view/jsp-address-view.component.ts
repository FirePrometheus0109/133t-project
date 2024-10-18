import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-jsp-address-view',
  templateUrl: './jsp-address-view.component.html',
  styleUrls: ['./jsp-address-view.component.scss']
})
export class JspAddressViewComponent {
  @Input() initialData: any;
  @Output() changeToEditMode = new EventEmitter<boolean>();
}
