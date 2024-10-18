import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-completion-spinner',
  templateUrl: './completion-spinner.component.html',
  styleUrls: ['./completion-spinner.component.scss']
})
export class CompletionSpinnerComponent {
  @Input() completionPercent: number;
}
