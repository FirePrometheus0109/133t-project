import { HttpClientModule, HttpRequest } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { async, inject, TestBed } from '@angular/core/testing';

import { DEFAULT_SETTINGS } from '../../../tests';
import { TEST_BASE_ROUTE } from './api.service.spec';
import { PublicService } from './public.service';

describe('PublicService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      providers: [PublicService],
    });
  });

  it('should be created', inject([PublicService], (service: PublicService) => {
    expect(service).toBeTruthy();
  }));

  it('test getInitialSettings', async(inject([PublicService, HttpTestingController],
    (publicApi: PublicService, backend: HttpTestingController) => {

      let initialSettings;

      publicApi.getInitialSettings().subscribe((response) => {
        initialSettings = DEFAULT_SETTINGS;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'GET'
          && request.url === `${TEST_BASE_ROUTE}/${publicApi.route}/${publicApi.INITIAL_SETTINGS}/`
          && request.headers.get('Content-Type') === 'application/json';
      }, `GET of '${publicApi.route}/${publicApi.INITIAL_SETTINGS}'`).flush(DEFAULT_SETTINGS);

      expect(initialSettings).toEqual(DEFAULT_SETTINGS);

    })));

});
