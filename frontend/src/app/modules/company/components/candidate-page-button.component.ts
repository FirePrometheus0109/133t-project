import { Component, Input } from '@angular/core';
import { NavigationService } from '../../core/services/navigation.service';


@Component({
  selector: 'app-candidate-page-button',
  template: `
    <button mat-button (click)="goToCandidatesPage()">{{candidatesCount}} Candidates</button>
  `,
  styles: []
})
export class CandidatePageButtonComponent {
  @Input() jobId: string;
  @Input() candidatesCount: number;

  constructor(private navigationService: NavigationService) {
  }

  goToCandidatesPage() {
    this.navigationService.goToViewCandidatesPage(this.jobId);
  }
}
