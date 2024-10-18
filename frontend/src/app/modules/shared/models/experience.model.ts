export interface JobItem {
  id: number;
  company: string;
  job_title: string;
  description: string;
  date_from: string;
  date_to: string;
  status: string;
  is_current: boolean;
  employment: string;
}


export enum ExperienceMode {
  VIEW = 'view',
  EDIT = 'edit',
  NEW = 'new',
}
