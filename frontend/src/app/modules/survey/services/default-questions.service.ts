import {Injectable} from '@angular/core';
import {ApiService} from '../../shared/services/api.service';

@Injectable()
export class DefaultQuestionsService {
  route = 'default-question';

  constructor(private api: ApiService) {
  }

  getDefaultQuestionsList() {
    return this.api.get(`${this.route}`);
  }
}
