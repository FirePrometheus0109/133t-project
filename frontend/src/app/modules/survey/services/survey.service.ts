import { Injectable } from '@angular/core';
import { environment } from '../../../../environments/environment';
import { ApiService } from '../../shared/services/api.service';
import { Question } from '../models/question.model';
import { Survey } from '../models/survey.model';


@Injectable()
export class SurveyService {
  route = 'survey';
  question = 'question';
  existingQuestions = 'existing-questions';
  job = 'job';
  answer = 'answer';

  constructor(private api: ApiService) {
  }

  getSurveyList(limit: number, offset: number, search?: string) {
    let params;
    search ? params = {limit: limit, offset: offset, search: search} : params = {limit: limit, offset: offset};
    return this.api.get(`${this.route}`, params);
  }

  createNewSurvey(data: Survey) {
    return this.api.post(`${this.route}`, data);
  }

  getSurvey(surveyId: number) {
    return this.api.getById(`${this.route}`, surveyId);
  }

  updateSurveyTitle(surveyId: number, title: string) {
    return this.api.patchById(`${this.route}`, surveyId, {title});
  }

  deleteSurvey(surveyId: number) {
    return this.api.deleteById(`${this.route}`, surveyId);
  }

  deleteQuestionFromSurvey(surveyId: number, questionId: number) {
    return this.api.delete(`${this.route}/${surveyId}/${this.question}/${questionId}`);
  }

  updateQuestionInSurvey(surveyId: number, questionId: number, questionData: Question) {
    return this.api.patch(`${this.route}/${surveyId}/${this.question}/${questionId}`, questionData);
  }

  addNewlyCreatedQuestionsToSurvey(surveyId: number, questionsData: Array<Question>) {
    return this.api.post(`${this.route}/${surveyId}/${this.question}`, questionsData);
  }

  addQuestionsFromSelectedToSurvey(surveyId: number, questionsData: Array<number>) {
    return this.api.post(`${this.route}/${surveyId}/${this.existingQuestions}`, {questions: questionsData});
  }

  isQuestionsCountAcceptable(questionsInSurvey: number, formArrayLength: number) {
    return (environment.maxQuestionsLength - questionsInSurvey - formArrayLength);
  }
}
