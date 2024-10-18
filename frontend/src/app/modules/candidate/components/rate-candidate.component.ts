import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Select, Store } from '@ngxs/store';
import { Observable } from 'rxjs';
import { User } from '../../auth/models/user.model';
import { CoreActions } from '../../core/actions';
import { CoreState } from '../../core/states/core.state';


@Component({
  selector: 'app-rate-candidate',
  template: `
    <div class="star-rating" *ngxPermissionsOnly="['can_rate_candidate']">
        <span class="star-rating">
          <ng-container *ngIf="!forDisplay">
            <i *ngFor="let n of range; let $index = index;"
               class="material-icons to-rate"
               [matTooltip]="ratingNameMapping[$index+1]"
               (click)="mark($index)"
               [ngClass]="isMarked($index)">{{isMarked($index)}}</i>
          </ng-container>
          <ng-container *ngIf="forDisplay">
            <i *ngFor="let n of range; let $index = index;"
               class="material-icons to-display"
               [matTooltip]="ratingNameMapping[$index+1]"
               [ngClass]="isMarked($index)">{{isMarked($index)}}</i>
          </ng-container>
        </span>
    </div>
  `,
  styles: [`
    .to-rate {
      cursor: pointer;
      padding: 0 3px;
    }

    .star_border {
      color: orange;
    }

    .star {
      color: orange;
    }

    .star_half {
      color: orange;
    }

    .to-display {
      padding: 0 2px;
    }
  `]
})
export class RateCadidateComponent implements OnInit {
  @Select(CoreState.CandidateRatingEnum) CandidateRatingEnum$: Observable<object>;
  @Input() candidate: User;
  @Input() scoreValue: string;
  @Input() forDisplay = false;
  @Input() candidateId: number;
  @Output() rateChanged = new EventEmitter();
  public maxScore = 0;
  public score: number;
  public ratingMapping: object = {};
  public ratingNameMapping: object = {};
  public ratingMappingReversed: object = {};

  range = [];
  marked = -1;

  constructor(private store: Store) {
  }

  ngOnInit() {
    const enumRating = this.store.selectSnapshot(CoreState.CandidateRatingEnum);
    let counter = 0;
    for (const suit of Object.keys(enumRating)) {
      if (!Number(suit)) {
        this.ratingMapping[counter] = suit;
        this.ratingMappingReversed[suit] = counter;
        counter++;
      }

      Object.values(enumRating).forEach((value, index) =>
        this.ratingNameMapping[index] = value);
    }
    this.maxScore = counter - 1;
    for (let i = 0; i < this.maxScore; i++) {
      this.range.push(i);
    }
    this.score = this.ratingMappingReversed[this.scoreValue];
    this.mark(this.score - 1, true);
  }

  public mark = (index, initial?) => {
    this.marked = this.marked === index ? index - 1 : index;
    this.score = this.marked + 1;
    this.scoreValue = this.ratingMapping[this.score];
    this.rateChanged.next(this.ratingMapping[this.score]);
    if (!initial) {
      (this.candidateId) ? this.rateCandidateAction(this.candidateId) : this.rateCandidateAction(this.candidate.id);
      this.rateChanged.emit(this.ratingMapping[this.score]);
    }
  }

  public isMarked = (index) => {
    if (!this.forDisplay) {
      if (index <= this.marked) {
        return 'star';
      } else {
        return 'star_border';
      }
    } else {
      if (this.score >= index + 1) {
        return 'star';
      } else if (this.score > index && this.score < index + 1) {
        return 'star_half';
      } else {
        return 'star_border';
      }
    }
  }

  private rateCandidateAction(candidateId: number) {
    this.store.dispatch(new CoreActions.RateCandidate(candidateId, this.ratingMapping[this.score]));
  }
}
