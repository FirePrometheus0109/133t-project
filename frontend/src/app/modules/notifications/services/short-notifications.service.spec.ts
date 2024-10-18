import { TestBed } from '@angular/core/testing';

import { ShortNotificationsService } from './short-notifications.service';

describe('ShortNotificationsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ShortNotificationsService = TestBed.get(ShortNotificationsService);
    expect(service).toBeTruthy();
  });
});
