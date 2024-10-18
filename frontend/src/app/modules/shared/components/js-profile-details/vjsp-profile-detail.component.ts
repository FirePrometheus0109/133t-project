import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-vjsp-profile-detail-value',
  template: `
    <div class="profile-detail-container">
      <div class="profile-type">
        {{ profileDetailName }}:&nbsp;
      </div>
      <div class="profile-value">
        {{ profileDetailValue }}
      </div>
    </div>
  `,
  styles: [`
    .profile-detail-container {
      display: flex;
      flex-direction: row;
      margin-bottom: 20px;
    }

    .profile-type {
      color: rgba(0, 0, 0, 0.54);
      font-size: 14px;
    }
  `],
})
export class VjspProfileDetailComponent {
  @Input() profileDetailName: string;
  @Input() profileDetailValue: string;
}
