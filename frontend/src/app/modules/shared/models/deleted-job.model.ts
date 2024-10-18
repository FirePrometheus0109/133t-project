export interface DeletedJobModel {
  id: number;
  title: string;
  is_deleted: boolean;
  company: {
    id: number,
    name: string
  };
}
