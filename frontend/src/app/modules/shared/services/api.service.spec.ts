import { HttpClientModule, HttpRequest } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { async, inject, TestBed } from '@angular/core/testing';

import { environment } from '../../../../environments/environment';
import { ApiService } from './api.service';

export const TEST_PARAM_1_KEY = 'param1';
export const TEST_PARAM_1_VALUE = 'value1';
export const TEST_PARAMS = {'param1': TEST_PARAM_1_VALUE};
export const TEST_PARAMS_STR = JSON.stringify(TEST_PARAMS);
export const TEST_DATA = {'bar': 'baz'};
export const TEST_DATA_STR = JSON.stringify(TEST_DATA);
export const TEST_RESPONSE_DATA = {'bar': 'barData'};
export const TEST_ROUTE = 'foo';
export const TEST_ROUTE_ID = 1;
export const TEST_BASE_ROUTE = 'http://localhost:8000/api/v1';
export const TEST_FULL_ROUTE = `${TEST_BASE_ROUTE}/foo/`;
export const TEST_FULL_ROUTE_WITH_ID = 'http://localhost:8000/api/v1/foo/1/';

describe(`ApiService`, () => {

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientModule,
        HttpClientTestingModule,
      ],
      providers: [
        ApiService,
      ],
    });
  });

  afterEach(inject([HttpTestingController], (backend: HttpTestingController) => {
    backend.verify();
  }));

  it('should be created', inject([ApiService], (api: ApiService) => {
    expect(api).toBeTruthy();
  }));

  it('test getFullApiRoute', inject([ApiService], (api: ApiService) => {
    const fullApiRoute = api.getFullApiRoute(TEST_ROUTE);

    expect(fullApiRoute).toContain(TEST_ROUTE);
    expect(fullApiRoute).toContain(environment.baseUrl);
    expect(fullApiRoute).toContain(environment.apiPrefix);
    expect(fullApiRoute).toContain(environment.apiVersion);

    expect(fullApiRoute).toEqual(
      `${environment.baseUrl}/${environment.apiPrefix}/${environment.apiVersion}/${TEST_ROUTE}/`,
    );
  }));

  it('test getFullApiRoute with ID', inject([ApiService], (api: ApiService) => {
    const fullApiRoute = api.getFullApiRoute(TEST_ROUTE, TEST_ROUTE_ID);

    expect(fullApiRoute).toContain(TEST_ROUTE);
    expect(fullApiRoute).toContain(`/${TEST_ROUTE_ID}/`);
    expect(fullApiRoute).toContain(environment.baseUrl);
    expect(fullApiRoute).toContain(environment.apiPrefix);
    expect(fullApiRoute).toContain(environment.apiVersion);

    expect(fullApiRoute).toEqual(
      `${environment.baseUrl}/${environment.apiPrefix}/${environment.apiVersion}/${TEST_ROUTE}/${TEST_ROUTE_ID}/`,
    );
  }));

  it(`should send an expected GET request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let getResponseData;

      api.get(TEST_ROUTE, TEST_PARAMS).subscribe((response) => {
        getResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'GET'
          && request.url === TEST_FULL_ROUTE
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && request.headers.get('Content-Type') === 'application/json';
      }, `GET of '${TEST_ROUTE}' with ${TEST_PARAMS_STR} params`).flush(TEST_RESPONSE_DATA);

      expect(getResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected GET by ID request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let getResponseData;

      api.getById(TEST_ROUTE, TEST_ROUTE_ID, TEST_PARAMS).subscribe((response) => {
        getResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'GET'
          && request.url === TEST_FULL_ROUTE_WITH_ID
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && request.headers.get('Content-Type') === 'application/json';
      }, `GET of '${TEST_ROUTE}/${TEST_ROUTE_ID}' with ${TEST_PARAMS_STR} params`).flush(TEST_RESPONSE_DATA);

      expect(getResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected POST request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.post(TEST_ROUTE, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'POST'
          && request.url === TEST_FULL_ROUTE
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `POST to '${TEST_ROUTE}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`).flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected POST by ID request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.postById(TEST_ROUTE, TEST_ROUTE_ID, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'POST'
          && request.url === TEST_FULL_ROUTE_WITH_ID
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `POST to '${TEST_ROUTE}/${TEST_ROUTE_ID}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`)
        .flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected PUT request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.put(TEST_ROUTE, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'PUT'
          && request.url === TEST_FULL_ROUTE
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `PUT to '${TEST_ROUTE}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`).flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected PUT by ID request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.putById(TEST_ROUTE, TEST_ROUTE_ID, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'PUT'
          && request.url === TEST_FULL_ROUTE_WITH_ID
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `PUT to '${TEST_ROUTE}/${TEST_ROUTE_ID}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`)
        .flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected DELETE request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let getResponseData;

      api.delete(TEST_ROUTE, TEST_PARAMS).subscribe((response) => {
        getResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'DELETE'
          && request.url === TEST_FULL_ROUTE
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && request.headers.get('Content-Type') === 'application/json';
      }, `DELETE of '${TEST_ROUTE}' with ${TEST_PARAMS_STR} params`).flush(TEST_RESPONSE_DATA);

      expect(getResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected DELETE by ID request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let getResponseData;

      api.deleteById(TEST_ROUTE, TEST_ROUTE_ID, TEST_PARAMS).subscribe((response) => {
        getResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'DELETE'
          && request.url === TEST_FULL_ROUTE_WITH_ID
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && request.headers.get('Content-Type') === 'application/json';
      }, `DELETE of '${TEST_ROUTE}/${TEST_ROUTE_ID}' with ${TEST_PARAMS_STR} params`).flush(TEST_RESPONSE_DATA);

      expect(getResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected PATCH request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.patch(TEST_ROUTE, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'PATCH'
          && request.url === TEST_FULL_ROUTE
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `PATCH to '${TEST_ROUTE}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`).flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

  it(`should send an expected PATCH by ID request`, async(inject([ApiService, HttpTestingController],
    (api: ApiService, backend: HttpTestingController) => {
      let postResponseData;

      api.patchById(TEST_ROUTE, TEST_ROUTE_ID, TEST_DATA, TEST_PARAMS).subscribe((response) => {
        postResponseData = response;
      });

      backend.expectOne((request: HttpRequest<any>) => {
        return request.method === 'PATCH'
          && request.url === TEST_FULL_ROUTE_WITH_ID
          && request.params.get(TEST_PARAM_1_KEY) === TEST_PARAM_1_VALUE
          && JSON.stringify(request.body) === JSON.stringify(TEST_DATA)
          && request.headers.get('Content-Type') === 'application/json';
      }, `PATCH to '${TEST_ROUTE}/${TEST_ROUTE_ID}' with ${TEST_PARAMS_STR} params and ${TEST_DATA_STR} data`)
        .flush(TEST_RESPONSE_DATA);

      expect(postResponseData).toEqual(TEST_RESPONSE_DATA);

    })));

});
