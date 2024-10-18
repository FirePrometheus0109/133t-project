import { Injectable } from '@angular/core';
import { ApiService } from '../../../../shared/services/api.service';


@Injectable()
export class EventCreatorService {
  event_types = 'event-types';

  constructor(private api: ApiService) {}

  getCalendarEventTypes() {
    return this.api.get(this.event_types);
  }
}
