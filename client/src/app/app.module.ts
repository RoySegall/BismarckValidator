import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpClientModule} from '@angular/common/http';
import {BrowserModule} from '@angular/platform-browser';
import {ServiceWorkerModule} from '@angular/service-worker';

import {StoreDevtoolsModule} from '@ngrx/store-devtools';

import {FlexLayoutModule} from '@angular/flex-layout';

import {AppRoutingModule} from './app-routing.module';

import {OpComponent} from './op.component';

import {environment} from '../environments/environment';
import {UploadComponent} from './upload/upload.component';
import {ResultsComponent} from './results/results.component';
import {HeaderComponent} from './header/header.component';
import {FooterComponent} from './footer/footer.component';
import {DropzoneModule} from 'ngx-dropzone-wrapper';
import {DROPZONE_CONFIG} from 'ngx-dropzone-wrapper';
import {DropzoneConfigInterface} from 'ngx-dropzone-wrapper';

const DEFAULT_DROPZONE_CONFIG: DropzoneConfigInterface = {
  // Change this to your upload POST address:
  url: 'https://httpbin.org/post',
  maxFilesize: 50,
  acceptedFiles: 'image/*'
};

@NgModule({
  declarations: [
    OpComponent,
    HeaderComponent,
    FooterComponent,
    UploadComponent,
    ResultsComponent,
  ],
  imports: [
    DropzoneModule,
    BrowserModule,
    ServiceWorkerModule.register('/ngsw-worker.js', {enabled: environment.production}),
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    FlexLayoutModule,
    !environment.production ? StoreDevtoolsModule.instrument() : [],
  ],
  providers: [{
    provide: DROPZONE_CONFIG,
    useValue: DEFAULT_DROPZONE_CONFIG
  }],
  bootstrap: [OpComponent]
})
export class AppModule {
}
