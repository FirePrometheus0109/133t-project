import { Component, EventEmitter, Inject, OnInit, Output } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MAT_DIALOG_DATA } from '@angular/material';


@Component({
  selector: 'app-select-letter-template-category',
  templateUrl: './select-letter-template-event-type.component.html',
  styleUrls: ['./select-letter-template-event-type.component.scss']
})
export class SelectLetterTemplateEventTypeComponent implements OnInit {
  @Output() submittedResult = new EventEmitter<number>();

  public selectedEventType: FormControl = new FormControl();

  constructor(@Inject(MAT_DIALOG_DATA) public modalData: any) {
  }

  ngOnInit() {
    if (this.modalData.selectedEventType) {
      this.selectedEventType.setValue(this.modalData.selectedEventType.id);
    }
  }

  selectEventType() {
    this.submittedResult.emit(this.selectedEventType.value);
  }
}
