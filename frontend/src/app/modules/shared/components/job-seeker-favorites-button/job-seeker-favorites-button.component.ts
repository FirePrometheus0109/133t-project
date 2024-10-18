import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Store } from '@ngxs/store';
import { CoreActions } from 'src/app/modules/core/actions';
import { CoreState } from '../../../core/states/core.state';


@Component({
  selector: 'app-job-seeker-favorites-button',
  templateUrl: './job-seeker-favorites-button.component.html',
  styleUrls: ['./job-seeker-favorites-button.component.css']
})
export class JobSeekerFavoritesButtonComponent {
  @Input() isFavorite: boolean;
  @Input() id: number;
  @Output() savedSuccessfully = new EventEmitter<any>();

  constructor(private store: Store) {
  }

  toggleJobFavorite() {
    this.store.dispatch(new CoreActions.SaveJobSeekerToFavorites(this.id, this.isFavorite)).subscribe(() => {
      if (!this.store.selectSnapshot(CoreState.errors)) {
        this.isFavorite = !this.isFavorite;
        this.savedSuccessfully.emit();
      }
    });
  }
}
