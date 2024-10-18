import { animate, state, style, transition, trigger } from '@angular/animations';
import { HttpClient, HttpEventType, HttpRequest } from '@angular/common/http';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { of, Subscription } from 'rxjs';
import { catchError, last, map, tap } from 'rxjs/operators';

export const fadeInOutDuration = 300;


@Component({
  selector: 'app-material-file-upload',
  templateUrl: './material-file-upload.component.html',
  styleUrls: ['./material-file-upload.component.css'],
  animations: [
    trigger('fadeInOut', [
      state('in', style({opacity: 100})),
      transition('* => void', [
        animate(fadeInOutDuration, style({opacity: 0})),
      ]),
    ]),
  ],
})
export class MaterialFileUploadComponent implements OnInit {
  /** Link text */
  @Input() text = 'Upload';
  /** Name used in form which will be sent in HTTP request. */
  @Input() param = 'file';
  /** Target URL for file uploading. */
  @Input() target = 'https://file.io';
  /** File extension that accepted, same as 'accept' of <input type="file" />. By the default, it's set to 'image/*'. */
  @Input() accept = 'image/png,image/jpg,image/jpeg,image/bmp,image/x-ms-bmp';

  @Input() isImageUploaded = false;
  /** Allow you to add handler after its completion. Bubble up response text from remote. */
  @Output() complete = new EventEmitter<string>();
  @Output() deleteFile = new EventEmitter<any>();

  public files: Array<FileUploadModel> = [];
  public errorMessage = '';

  constructor(private _http: HttpClient) {
  }

  ngOnInit() {
  }

  onClick() {
    const fileUpload = document.getElementById('fileUpload') as HTMLInputElement;
    fileUpload.onchange = () => {
      for (let index = 0; index < fileUpload.files.length; index++) {
        const file = fileUpload.files[index];
        this.files.push({data: file, state: 'in', inProgress: false, progress: 0, canRetry: false, canCancel: true});
      }
      this.uploadFiles();
    };
    fileUpload.click();
  }

  onDelete() {
    this.files = [];
    this.deleteFile.emit();
  }

  cancelFile(file: FileUploadModel) {
    if (file) {
      if (file.sub) {
        file.sub.unsubscribe();
      }
      this.removeFileFromArray(file);
    }
  }

  retryFile(file: FileUploadModel) {
    this.uploadFile(file);
    file.canRetry = false;
  }

  private uploadFile(file: FileUploadModel) {
    const maxPercentNumber = 100;
    const fd = new FormData();
    fd.append(this.param, file.data);

    const req = new HttpRequest('PUT', this.target, fd, {
      reportProgress: true,
    });

    file.inProgress = true;
    file.sub = this._http.request(req).pipe(
      map(event => {
        switch (event.type) {
          case HttpEventType.UploadProgress:
            file.progress = Math.round(event.loaded * maxPercentNumber / event.total);
            break;
          case HttpEventType.Response:
            this.errorMessage = '';
            this.files = [];
            return event;
        }
      }),
      tap(() => {
      }),
      last(),
      catchError((error) => {
        this.errorMessage = error.error.errors.photo.join();
        file.inProgress = false;
        file.canRetry = true;
        return of(`${file.data.name} upload failed.`);
      }),
    ).subscribe(
      (event: any) => {
        if (typeof (event) === 'object') {
          this.removeFileFromArray(file);
          this.complete.emit(event.body);
        }
      },
    );
  }

  private uploadFiles() {
    const fileUpload = document.getElementById('fileUpload') as HTMLInputElement;
    fileUpload.value = '';

    this.files.forEach(file => {
      if (!file.inProgress) {
        this.uploadFile(file);
      }
    });
  }

  private removeFileFromArray(file: FileUploadModel) {
    const index = this.files.indexOf(file);
    if (index > -1) {
      this.files.splice(index, 1);
    }
  }
}


export class FileUploadModel {
  data: File;
  state: string;
  inProgress: boolean;
  progress: number;
  canRetry: boolean;
  canCancel: boolean;
  sub?: Subscription;
}
