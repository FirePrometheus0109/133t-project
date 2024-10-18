import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-download-selected-to-csv',
  templateUrl: './download-selected-to-csv.component.html',
  styleUrls: ['./download-selected-to-csv.component.scss']
})
export class DownloadSelectedToCSVComponent {
  @Input() isDisabled: boolean;
  @Output() downloadToCSV = new EventEmitter<any>();
}
