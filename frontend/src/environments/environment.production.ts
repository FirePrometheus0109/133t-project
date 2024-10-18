import { environment as base_environment } from './environment.base';

export const environment = Object.assign(
  base_environment, {
    production: true,
    baseUrl: 'http://165.227.83.243',
    showTechnicalInfo: false,
  }
);
