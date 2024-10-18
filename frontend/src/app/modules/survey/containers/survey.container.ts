import {Component} from '@angular/core';
import {SurveyRoute} from '../../shared/constants/routes/survey-routes';

@Component({
  selector: 'app-survey-page',
  template: `
    <nav mat-tab-nav-bar>
      <a mat-tab-link
         *ngFor="let link of surveyLinks"
         [routerLink]="link.path"
         routerLinkActive #rla="routerLinkActive"
         [active]="rla.isActive">
        {{link.label}}
      </a>
    </nav>
    <router-outlet></router-outlet>
  `,
  styles: [],
})
export class SurveyComponent {
  surveyLinks = [
    {label: 'Question list', path: SurveyRoute.questionListRoute},
    {label: 'Default questions', path: SurveyRoute.defaultQuestionsRoute},
    {label: 'Saved questions', path: SurveyRoute.savedQuestionsRoute},
  ];
}
