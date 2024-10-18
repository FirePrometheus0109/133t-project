import { Injectable } from '@angular/core';
import { MatIconRegistry } from '@angular/material';
import { DomSanitizer } from '@angular/platform-browser';


@Injectable({
  providedIn: 'root',
})
export class SocialIconsService {
  constructor(private matIconRegistry: MatIconRegistry,
              private domSanitizer: DomSanitizer) {
  }

  private readonly socialIcons = [
    {
      name: 'google',
      src: '../../assets/google.svg'
    },
    {
      name: 'facebook',
      src: '../../assets/facebook.svg'
    }
  ];

  setSocialIcons() {
    this.socialIcons.forEach((icon) => {
      this.matIconRegistry.addSvgIcon(
        icon.name,
        this.domSanitizer.bypassSecurityTrustResourceUrl(icon.src)
      );
    });
  }
}
