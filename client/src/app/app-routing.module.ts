import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { ResultsComponent } from './results/results.component';
import {FileComponent} from "./file/file.component";

const routes: Routes = [
  { path: '', component: UploadComponent, pathMatch: 'full' },
  { path: 'results/:id', component: ResultsComponent },
  { path: 'results/:id/:file', component: FileComponent },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
