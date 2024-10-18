import { Injectable } from '@angular/core';
import { ApiService } from '../../shared/services/api.service';


@Injectable()
export class LogsService {
  private route = 'logs';

  constructor(private api: ApiService) {
  }

  public getLogsData(params?: object) {
    return this.api.get(`${this.route}`, params);
  }

  public deleteLog(logId: number) {
    return this.api.deleteById(`${this.route}`, logId);
  }
}
