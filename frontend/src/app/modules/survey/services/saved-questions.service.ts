import {Injectable} from '@angular/core';
import {ApiService} from '../../shared/services/api.service';
import {Question} from '../models/question.model';

@Injectable()
export class SavedQuestionsService {
  route = 'saved-question';

  constructor(private api: ApiService) {
  }

  getSavedQuestionsList(limit: number, offset: number) {
    return this.api.get(`${this.route}`, {limit: limit, offset: offset});
  }

  createNewQuestionInSaved(data: Question) {
    return this.api.post(`${this.route}`, data);
  }

  getSavedQuestion(questionId: number) {
    return this.api.getById(`${this.route}`, questionId);
  }

  updateSavedQuestion(questionId: number, data: Question) {
    return this.api.patchById(`${this.route}`, questionId, data);
  }

  deleteSavedQuestion(questionId: number) {
    return this.api.deleteById(`${this.route}`, questionId);
  }
}
