export interface Changelog {
  name: string;
  children?: Changelog[];
}


export interface Version {
  version: string;
  date: string;
  changelog: Changelog;
}
