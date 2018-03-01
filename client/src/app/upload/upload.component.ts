import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'op-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  config = {};
  files = [];

  constructor() { }

  ngOnInit() {
  }

  onUploadError($event) {
  }

  onUploadSuccess($event) {
    this.files.push($event[1].file);
  }

  submit() {
    // Send it to the backend and start to wait for the pusher events.
    console.log(this.files);
  }

}
