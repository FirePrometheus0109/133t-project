export interface EducationItem {
  id: number;
  owner: number;
  type: string;
  status: string;
  institution: string;
  field_of_study: string;
  degree: string;
  date_from: string;
  date_to: string;
  location: string;
  description: string;
  is_current: boolean;
}


export interface CertificationItem {
  id: number;
  owner: number;
  type: string;
  status: string;
  institution: string;
  field_of_study: string;
  graduated: string;
  licence_number: string;
  location: string;
  description: string;
  is_current: boolean;
}


export enum EducationMode {
  VIEW = 'view',
  EDIT = 'edit',
  NEW = 'new',
}


export enum EducationType {
  EDUCATION = 'education',
  CERTIFICATION = 'certification',
}
