import { TestBed } from '@angular/core/testing';

import { ManageNotifications.ServiceService } from './manage-notifications.service.service';

describe('ManageNotifications.ServiceService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: ManageNotifications.ServiceService = TestBed.get(ManageNotifications.ServiceService);
    expect(service).toBeTruthy();
  });
});
