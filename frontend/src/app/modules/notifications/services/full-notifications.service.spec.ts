import { TestBed } from '@angular/core/testing';

import { FullNotificationsService } from './full-notifications.service';

describe('FullNotificationsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: FullNotificationsService = TestBed.get(FullNotificationsService);
    expect(service).toBeTruthy();
  });
});
