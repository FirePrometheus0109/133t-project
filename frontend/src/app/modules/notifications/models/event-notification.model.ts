export interface EventNotificationModel {
  address: string;
  attendee_id?: number;
  city_name: string;
  company_address: string;
  company_name: string;
  country_name: string;
  event_description: string;
  event_owner_full_name: string;
  event_subject: string;
  job_details_url: string;
  job_title: string;
  state_abbreviation: string;
  time_from: string;
  time_to: string;
  timezone: string;
  zip_code: string;
  status?: EventNotificationStatus;
  cancelled: boolean;
}


export enum EventNotificationStatus {
  ACCEPTED = 'ACCEPTED',
  REJECTED = 'REJECTED'
}

export interface EventNotificationResponseModel {
  id: number;
  status: string;
}
