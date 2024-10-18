import { environment as base_environment } from './environment.base';

export const environment = Object.assign(
  base_environment, {
    production: false,
    baseUrl: 'http://localhost:8000',
    showTechnicalInfo: true
  }
);
