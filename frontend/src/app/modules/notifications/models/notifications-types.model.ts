export interface NotificationsTypesModel {
  ['133T']: NotificationTypeItemModel[];
  Email: NotificationTypeItemModel[];
}


export interface NotificationTypeItemModel {
  id: number;
  name: string;
  checked?: boolean;
}
