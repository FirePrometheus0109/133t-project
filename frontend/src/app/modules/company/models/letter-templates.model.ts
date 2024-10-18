export class LetterTemplateItem {
  id?: number;
  name: string;
  subject: string;
  body: string;
  modified_at?: string;
  event_type?: LetterTemplateEventType;
}


export interface LetterTemplateEventType {
  id: number;
  name: string;
}
