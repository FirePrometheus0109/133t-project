export interface NotificationsShortModel {
  id: number;
  timestamp: string;
  description: string;
  data: {
    autoapply: {
      id: number;
      title: string;
    },
    subscription: object,
    plan: object,
  };
}
