import { Injectable } from '@angular/core';
import { ApiService } from '../../shared/services/api.service';


@Injectable()
export class CompanyLetterTemplatesService {
  route = 'letter-templates';
  eventTypes = 'event-types';

  constructor(private api: ApiService) {
  }

  public getLetterTemplates(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  public getLetterTemplatesEventTypes() {
    return this.api.get(`${this.eventTypes}`);
  }

  public createNewLetterTemplate(letterTemplate: object) {
    return this.api.post(`${this.route}`, letterTemplate);
  }

  public getLetterTemplateData(letterTemplateId: number) {
    return this.api.getById(`${this.route}`, letterTemplateId);
  }

  public saveLetterTemplate(letterTemplateId: number, letterTemplate: object) {
    return this.api.putById(`${this.route}`, letterTemplateId, letterTemplate);
  }

  public deleteLetterTemplate(letterTemplateId: number) {
    return this.api.deleteById(`${this.route}`, letterTemplateId);
  }
}
