import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from '../../shared/services/api.service';


@Injectable({
  providedIn: 'root',
})
export class PurchasedJobSeekersService {
  route = 'purchased-job-seekers';

  constructor(private api: ApiService) {
  }

  loadPurchasedJobSeekers(): Observable<any> {
    return this.api.get(`${this.route}`, {limit: 10000});
  }
}
