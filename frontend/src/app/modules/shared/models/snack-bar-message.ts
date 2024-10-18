import { MatSnackBarConfig } from '@angular/material';

const DEFAULT_SNACK_BAR_MESSAGE_DELAY = 3000;

export { DEFAULT_SNACK_BAR_MESSAGE_DELAY };


export enum SnackBarMessageType {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error',
  DEFAULT_MESSAGE_TYPE = 'info',
}


export interface SnackBarMessage {
  message: string;
  action?: string;
  type?: SnackBarMessageType;
  delay?: number;
  config?: MatSnackBarConfig;
}
