import { Component, Input } from '@angular/core';
import { SkillItem } from '../../shared/models/skill.model';
import { MaterialChips } from '../models/material-chips';


@Component({
  selector: 'app-skills-view-component',
  template: `
    <mat-card class="skill-card" [ngClass]="{'full-width-skills': isProfileMode}">
      <mat-card-title>
        <span>{{title}}</span>
      </mat-card-title>
      <mat-card-content>
        <mat-chip-list>
          <mat-chip *ngFor="let skillItem of skillsToDisplay" [color]="matchSkills(skillItem)" selected>
            {{skillItem.name}}
          </mat-chip>
        </mat-chip-list>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .skill-card {
      border: 1px solid #607d8b;
      border-radius: 15px;
      max-width: 300px;
    }

    .full-width-skills {
      max-width: 100%;
    }

    mat-card-title {
      text-align: center;
    }
  `],
})
export class SkillsViewComponent {
  @Input() title: string;
  @Input() skillsToDisplay: Array<SkillItem>;
  @Input() isMatchMode: boolean;
  @Input() isProfileMode: boolean;

  public matchSkills(skillItem: SkillItem): string {
    if (this.isMatchMode) {
      if (skillItem.match) {
        return MaterialChips.ACCENT;
      } else {
        return MaterialChips.WARN;
      }
    } else {
      return MaterialChips.PRIMARY;
    }
  }
}

