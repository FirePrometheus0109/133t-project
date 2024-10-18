import { Component } from '@angular/core';
import { SocialMediaAccount } from '../../../shared/enums/social-media-account';
import { AuthSocialService } from '../../services/auth-social.service';


@Component({
  selector: 'app-social-auth',
  templateUrl: './social-auth.component.html',
  styleUrls: ['./social-auth.component.css']
})
export class SocialAuthComponent {

  constructor(private authSocialService: AuthSocialService) {
  }

  signInWithGoogle(): void {
    this.authSocialService.signInWithSocialAccount(SocialMediaAccount.GOOGLE);
  }

  signInWithFacebook(): void {
    this.authSocialService.signInWithSocialAccount(SocialMediaAccount.FACEBOOK);
  }
}
