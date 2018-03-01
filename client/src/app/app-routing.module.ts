import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { ResultsComponent } from './results/results.component';

const routes: Routes = [
  { path: '', component: UploadComponent, pathMatch: 'full' },
  { path: 'results', component: ResultsComponent },
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
