import { Injectable } from '@angular/core';
import { Store } from '@ngxs/store';
import { FacebookLoginProvider, GoogleLoginProvider } from 'angularx-social-login';
import { LoginPageActions } from '../../auth/actions';
import { SocialMediaAccount } from '../../shared/enums/social-media-account';


@Injectable({
  providedIn: 'root',
})
export class AuthSocialService {
  googleLoginProvider: any;
  facebookLoginProvider: any;

  constructor(private store: Store) {
  }

  createSocialProvidersInstances(socialsIds) {
    this.googleLoginProvider = new GoogleLoginProvider(socialsIds.google);
    this.facebookLoginProvider = new FacebookLoginProvider(socialsIds.facebook,
      {auth_type: 'reauthenticate', enable_profile_selector: true});
    this.initializeSocialProviders();
  }

  initializeSocialProviders() {
    this.googleLoginProvider.initialize();
    this.facebookLoginProvider.initialize();
  }

  signInWithSocialAccount(socialMediaType: string) {
    let socialLoginProvider;
    (socialMediaType === SocialMediaAccount.GOOGLE) ? socialLoginProvider = this.googleLoginProvider :
      socialLoginProvider = this.facebookLoginProvider;
    socialLoginProvider.signIn().then((result) => {
      this.store.dispatch(new LoginPageActions.LoginWithSocialAccount(result.authToken, socialMediaType));
    }, (err) => {
      console.warn(err);
    });
  }
}
