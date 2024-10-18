import { Address } from './address.model';
import { Owner } from './owner.model';


export class BaseJob {
  id: number;
  title: string;
  location: Address;
  position_type: string;
  education: string;
  clearance: string;
  experience: string;
  salary_min: number;
  salary_max: number;
  salary_negotiable: boolean;
  benefits: string;
  travel: string;
  owner: Owner;
  created_at: string;
  closing_date: string;
}
