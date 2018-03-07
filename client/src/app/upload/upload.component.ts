import { Component, OnInit, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {environment} from '../../environments/environment';

@Component({
  selector: 'op-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})

@Injectable()
export class UploadComponent implements OnInit {

  config = {};

  data = {
    'files': [],
    'room': Date.now()
  };

  constructor(private http: HttpClient) { }

  ngOnInit() {
  }

  onUploadError($event) {
  }

  onUploadSuccess($event) {
    this.data['files'].push($event[1].file);
  }

  submit() {
    debugger;
    // Send it to the backend and start to wait for the pusher events.
    console.log(environment.backend + '/process_files');
  }

}
