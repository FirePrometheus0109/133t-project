import { Component, Input } from '@angular/core';
import { Address } from '../../models/address.model';


@Component({
  selector: 'app-profile-address-view',
  templateUrl: './profile-address-view.component.html',
  styleUrls: ['./profile-address-view.component.css']
})
export class ProfileAddressViewComponent {
  @Input() addressData: Address;

}
