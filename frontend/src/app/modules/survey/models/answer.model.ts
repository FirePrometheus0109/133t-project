export interface Answer {
  id: number;
  question: {
    id: number,
    body: string,
  };
  answer: string;
}


export interface AnswerData {
  question: number;
  answer: {
    yes_no_value: string;
  };
}
