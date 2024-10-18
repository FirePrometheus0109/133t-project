export interface CandidateActivityModel {
  activity: string;
  candidate: {
    id: number,
    name: string
  };
  created_at: string;
  job: {
    id: number,
    title: string
  };
}
