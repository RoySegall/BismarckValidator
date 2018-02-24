import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserModule } from '@angular/platform-browser';
import { ServiceWorkerModule } from '@angular/service-worker';

import { StoreDevtoolsModule } from '@ngrx/store-devtools';

import { DragulaModule } from 'ng2-dragula/ng2-dragula';
import { FlexLayoutModule } from '@angular/flex-layout';

import { AppRoutingModule } from './app-routing.module';

import { OpComponent } from './op.component';

import { environment } from '../environments/environment';
import { UploadComponent } from './upload/upload.component';
import { ResultsComponent } from './results/results.component';
import {HeaderComponent} from './header/header.component';
import {FooterComponent} from './footer/footer.component';

@NgModule({
  declarations: [
    OpComponent,
    HeaderComponent,
    FooterComponent,
    UploadComponent,
    ResultsComponent,
  ],
  imports: [
    BrowserModule,
    ServiceWorkerModule.register('/ngsw-worker.js', { enabled: environment.production }),
    HttpClientModule,
    FormsModule,
    AppRoutingModule,
    FlexLayoutModule,
    DragulaModule,
    !environment.production ? StoreDevtoolsModule.instrument() : [],
  ],
  providers: [],
  bootstrap: [OpComponent]
})
export class AppModule { }
