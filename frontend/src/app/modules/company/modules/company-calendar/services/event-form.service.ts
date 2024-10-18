import { Injectable } from '@angular/core';

import { ApiService } from '../../../../shared/services/api.service';


@Injectable()
export class EventFormService {
  jobs = 'enums/jobs';
  colleagues = 'enums/company-users';
  candidates = 'enums/candidates';
  zones = 'geo/timezones';
  country = 'geo/country';
  city = 'geo/city';
  events = 'events';
  another_events = 'another-events';
  letter_templates = 'letter-templates';
  zips = 'zip';

  constructor(private api: ApiService) {}

  getColleagues() {
    return this.api.get(this.colleagues);
  }

  getCandidates(jobId) {
    return this.api.get(`${this.candidates}`, {job: jobId});
  }

  getZones() {
    return this.api.get(this.zones);
  }

  getJobPostings() {
    return this.api.get(this.jobs);
  }

  getEvent(eventId: number) {
    return this.api.get(`${this.events}/${eventId}`);
  }

  createEvent(eventData: any) {
    return this.api.post(this.events, eventData);
  }

  updateEvent(eventId: number, eventData: any) {
    return this.api.put(`${this.events}/${eventId}`, eventData);
  }

  deleteEvent(eventId: number) {
    return this.api.delete(`${this.events}/${eventId}`);
  }

  checkTime(queryParams: {time_from: string, time_to: string, id?: number}) {
    return this.api.get(this.another_events, queryParams);
  }

  getLetterTemplates() {
    return this.api.get(this.letter_templates);
  }

  getCounties() {
    return this.api.get(this.country);
  }

  getCities(countryId, name = '', offset = 0) {
    return this.api.get(this.city, {country_id: countryId, name, offset});
  }

  getZips(cityId) {
    return this.api.get([this.city, cityId, this.zips].join('/'));
  }
}
