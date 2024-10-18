export interface Question {
  id: number;
  body: string;
  is_answer_required: boolean;
  is_default: boolean;
  disqualifying_answer: string;
  add_to_saved_questions: boolean;
  answer_type: string;
}


export const QuestionDefault = {
  body: '',
  is_answer_required: false,
  disqualifying_answer: '',
  add_to_saved_questions: false,
};
