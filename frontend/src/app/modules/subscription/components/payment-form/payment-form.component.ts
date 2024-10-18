import { Component, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Store } from '@ngxs/store';
import { ElementOptions, ElementsOptions, StripeCardComponent, StripeService } from 'ngx-stripe';
import { CoreState } from 'src/app/modules/core/states/core.state';
import { PaymentData } from '../../models/payment-data.model';


@Component({
  selector: 'app-payment-form',
  templateUrl: './payment-form.component.html',
  styleUrls: ['./payment-form.component.css']
})
export class PaymentFormComponent implements OnInit {
  @Input() payButtonText = 'Pay';
  @Output() processPayment = new EventEmitter<any>();
  @Output() cancelButton = new EventEmitter<any>();

  @ViewChild(StripeCardComponent) card: StripeCardComponent;

  isCancelUsed: boolean;
  stripeComponentError: any;
  isCardDataCompleted = false;

  cardOptions: ElementOptions = {
    style: {
      base: {
        iconColor: '#276fd3',
        color: '#31325F',
        lineHeight: '40px',
        fontWeight: 300,
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '18px',
        '::placeholder': {
          color: '#CFD7E0'
        }
      }
    },
    hidePostalCode: true,
  };

  elementsOptions: ElementsOptions = {
    locale: 'en'
  };

  stripeUserForm = new FormGroup({
    name: new FormControl('', Validators.required),
    email: new FormControl('', Validators.compose([Validators.required, Validators.email])),
    address_line1: new FormControl('', Validators.required),
    address_city: new FormControl(''),
    address_state: new FormControl(''),
    address_country: new FormControl(''),
    auto_renew: new FormControl(true)
  });

  constructor(private stripeService: StripeService,
              private store: Store) {
  }

  ngOnInit(): void {
    this.keyUpdated(this.store.selectSnapshot(CoreState.stripeKey));
    this.isCancelUsed = this.cancelButton.observers.length > 0;
  }

  keyUpdated(stripeKey) {
    this.stripeService.changeKey(stripeKey);
  }

  onCancelButton() {
    this.cancelButton.emit();
  }

  detectChanges(event) {
    this.stripeComponentError = (event.event.hasOwnProperty('error') && event.event.error) ? event.event.error : null;
    if (event.type === 'change') {
      this.isCardDataCompleted = event.event.complete;
    }
  }

  getCardToken() {
    this.stripeService.createToken(this.card.getCard(), {
      name: this.stripeUserForm.value.name,
      address_line1: this.stripeUserForm.value.address_line1,
      address_city: this.stripeUserForm.value.address_city,
      address_state: this.stripeUserForm.value.address_state,
      address_country: 'US'
    }).subscribe(result => {
      const paymentData = new PaymentData(result, this.stripeUserForm.value.email, this.stripeUserForm.value.auto_renew);
      this.processPayment.emit(paymentData);
    });
  }

}
