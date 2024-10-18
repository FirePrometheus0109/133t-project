import { TokenResult } from 'ngx-stripe';

export class PaymentData {
  auto_renew_subscription: boolean;
  token: string;
  email: string;

  constructor(token: TokenResult, email: string, is_auto_renew: boolean ) {
    this.token = token.token.id;
    this.email = email;
    this.auto_renew_subscription = is_auto_renew;
  }
}
