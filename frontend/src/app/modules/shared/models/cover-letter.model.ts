export interface CoverLetterItem {
  id: number;
  title: string;
  body: string;
  is_default: boolean;
}


export enum CoverLetterMode {
  VIEW = 'view',
  EDIT = 'edit',
  NEW = 'new',
}


export interface CoverLetterApplyData {
  cover_letter: number;
}
