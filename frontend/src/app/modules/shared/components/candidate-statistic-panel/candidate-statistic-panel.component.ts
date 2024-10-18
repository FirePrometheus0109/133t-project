import { Component, EventEmitter, Input, Output } from '@angular/core';


@Component({
  selector: 'app-candidate-statistic-panel',
  templateUrl: './candidate-statistic-panel.component.html',
  styleUrls: ['./candidate-statistic-panel.component.css']
})
export class CandidateStatisticPanelComponent {
  @Input() panelData: object;
  @Output() navigateToCandidates = new EventEmitter<any>();

  onCandidateOpen(item) {
    if (item.value) {
      this.navigateToCandidates.emit(item);
    }
  }
}
