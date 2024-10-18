import { Component, EventEmitter, Input, Output } from '@angular/core';
import { LogItem } from '../../models/log.model';


@Component({
  selector: 'app-log-item',
  templateUrl: './log-item.component.html',
  styleUrls: ['./log-item.component.scss']
})
export class LogItemComponent {
  @Input() logItem: LogItem;
  @Output() viewDeletedComment = new EventEmitter<LogItem>();
  @Output() deleteLog = new EventEmitter<number>();

  public get isHasDeletedComment() {
    return this.logItem.other_info.hasOwnProperty('deleted_comment');
  }
}
