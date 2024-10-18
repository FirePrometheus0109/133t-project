import { JSNameAndId } from '../../job-seeker/models/job-seeker-profile.model';
import { CandidateStatus } from './candidate-item.model';


export interface CandidateQuickListItem {
  id: number;
  user: JSNameAndId;
  job: {
    id: number,
    title: string
  };
  status: CandidateStatus;
}
