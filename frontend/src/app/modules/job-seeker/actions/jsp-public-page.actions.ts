export enum JobSeekerProfilePublicPageTypes {
  LoadPublicProfile = '[Job Seeker Public Profile Page] LoadPublicProfile',
  DisplayAsPublic = '[Job Seeker Public Profile Page] DisplayAsPublic'
}

export class LoadPublicProfile {
  static readonly type = JobSeekerProfilePublicPageTypes.LoadPublicProfile;
  constructor(public jsUid: string) {}
}

export class DisplayAsPublic {
  static readonly type = JobSeekerProfilePublicPageTypes.DisplayAsPublic;
  constructor(public isPublic: boolean = true) {}
}


export type JobSeekerProfilePublicPageActionsUnion =
  | DisplayAsPublic
  | LoadPublicProfile;
