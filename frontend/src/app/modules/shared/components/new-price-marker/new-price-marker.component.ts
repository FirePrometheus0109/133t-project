import { Component, Input } from '@angular/core';
import { DateTimeHelper } from '../../helpers/date-time.helper';


@Component({
  selector: 'app-new-price-marker',
  templateUrl: './new-price-marker.component.html',
  styleUrls: ['./new-price-marker.component.scss']
})
export class NewPriceMarkerComponent {
  @Input() newPrice: number;
  @Input() priceApplyDate: string;

  public get formattedDate() {
    return DateTimeHelper.getDate(this.priceApplyDate);
  }
}
