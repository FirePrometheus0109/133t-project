import { environment as base_environment } from './environment.base';

export const environment = Object.assign(
  base_environment, {
    production: true,
    baseUrl: 'https://133t-dev.demohoster.com',
    showTechnicalInfo: true,
  }
);
