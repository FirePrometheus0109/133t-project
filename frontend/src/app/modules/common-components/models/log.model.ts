export interface OtherInfoLogModel {
  deleted_comment: {
    comment: string;
    submit_date: string;
    title: string;
    user: {
      id: number,
      name: string,
      company_user: {
        id: number
      }
    };
  };
}


export interface LogItem {
  id: number;
  message: string;
  other_info: OtherInfoLogModel;
  owner: {
    id: number,
    name: string
  };
  time: string;
}


export enum LogType {
  JobSeekerLog = 'jobseeker',
  JobLog = 'job'
}
