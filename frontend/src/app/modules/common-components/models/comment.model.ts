export interface CommentModel {
  id?: number;
  title: string;
  comment: string;
  source?: number;
}


export interface CommentItem {
  id: number;
  title: string;
  comment: string;
  submit_date: string;
  user: {
    name: string,
    id: number
  };
}


export enum CommentType {
  JobSeekerComment = 'job-seeker-comment',
  JobComment = 'job-comment'
}
