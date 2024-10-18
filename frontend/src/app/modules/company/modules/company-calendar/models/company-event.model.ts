import { CalendarEvent } from 'angular-calendar';
import * as moment from 'moment-timezone';
import {
  CityModel,
  CountryModel,
  ZipModel
} from '../../../../shared/models/address.model';

export const EventColorScheme = {
  red: {
    primary: '#f44336',
    secondary: '#ff7961'
  }
};

export interface CompanyUserEnum {
  id: number;
  user: {
    id: number;
    name: string;
  };
}

export interface JobSeekerEnum {
  id: number;
  job_seeker: {
    id: number;
    user: {
      id: number;
      name: string;
    }
  };
}

// ============= //

export interface NestedEventType {
  id: number;
  name: string;
}

export interface NestedUser {
  id: number;
  name: string;
}

export interface NestedJob {
  id: number;
  title: string;
}

export interface NestedListUser {
  id: number;
  user: NestedUser;
  status: string;
}

export interface NestedAddress {
  id: number;
  address: string;
  country: CountryModel;
  city: CityModel;
  zip: ZipModel;
}

export interface ShortServerCalendarEvent {
  date: string;
  time_from: string;
  time_to: string;
  id: number;
  type: NestedEventType;
  subject: string;
  attendees: NestedListUser[];
}

export interface ExtendedCalendarEvent extends CalendarEvent {
  id: number;
  owner: NestedUser;
  type: NestedEventType;
  location: NestedAddress;
  subject: string;
  description: string;
  date: string;
  time_from: string;
  time_to: string;
  job: NestedJob;
  colleagues: NestedListUser[];
  candidates: NestedListUser[];
}

export interface ShortCalendarEvent
  extends CalendarEvent,
    ShortServerCalendarEvent {
  id: number;
  end: Date;
}

export class ExtendedCalendarEventModel {
  static readonly timeFormatForTitle = 'hh:mmA';

  static getValidDate(dateStr: string): Date {
    return moment(dateStr).toDate();
  }

  static formatEventDates(event: ShortServerCalendarEvent) {
    return {
      ...event,
      start: this.getValidDate(event.time_from),
      end: this.getValidDate(event.time_to)
    };
  }

  static setEventTitle(event) {
    const timeFrom = moment(event.time_from).format(this.timeFormatForTitle).toLowerCase();
    const timeTo = moment(event.time_to).format(this.timeFormatForTitle).toLowerCase();
    return {
      ...event,
      title: `${timeFrom}-${timeTo} ${event.type.name}`
    };
  }

  static setEventColor(event) {
    return {
      ...event,
      color: EventColorScheme.red
    };
  }

  static formatMultiple(
    serverEvents: ShortServerCalendarEvent[],
  ): ShortCalendarEvent[] {
    const formatedEvents: ShortCalendarEvent[] = serverEvents.map(
      serverEvent => {
        let tmp;
        tmp = this.formatEventDates(serverEvent);
        tmp = this.setEventTitle(tmp);
        tmp = this.setEventColor(tmp);
        return tmp;
      }
    );
    return formatedEvents;
  }
}
