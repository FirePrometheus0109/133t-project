import { Component, Input } from '@angular/core';
import { DeletedJobModel } from '../../models/deleted-job.model';


@Component({
  selector: 'app-deleted-job-view',
  templateUrl: './deleted-job-view.component.html',
  styleUrls: ['./deleted-job-view.component.scss']
})
export class DeletedJobViewComponent {
  @Input() deletedJob: DeletedJobModel;
}
