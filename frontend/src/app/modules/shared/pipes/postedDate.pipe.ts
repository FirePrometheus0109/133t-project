import {Pipe, PipeTransform} from '@angular/core';
import * as moment from 'moment';

@Pipe({
  name: 'postedDate'
})
export class PostedDatePipe implements PipeTransform {
  transform(value: any, ...args: any[]) {
    if (value) {
      const momentDate = moment(value);
      const prefix = momentDate.diff(moment()) > 0 ? 'Will be posted:' : 'Posted:';
      return `${prefix} ${momentDate.fromNow()}`;
    } else {
      return 'Not published';
    }
  }
}
