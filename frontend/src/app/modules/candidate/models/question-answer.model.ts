import { Question } from '../../survey/models/question.model';


export interface QuestionAnswer {
  id: number;
  question: Question;
  answer: string;
  is_disqualify: boolean;
}
