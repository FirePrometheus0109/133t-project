import { Injectable } from '@angular/core';

import { ApiService } from '../../../../shared/services/api.service';


@Injectable()
export class CalendarService {
  events = 'events';

  constructor(private api: ApiService) {}

  getCalendarEvents(params) {
    return this.api.get(this.events, params);
  }
}
