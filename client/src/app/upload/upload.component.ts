import {Component, OnInit, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {HttpHeaders} from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'op-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})

@Injectable()
export class UploadComponent implements OnInit {

  config = {};
  data = {};
  canVerify = false;
  processing = false;

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
    this.data['room'] = Date.now();
    this.data['files'] = [];
  }

  onUploadError($event) {
  }

  onUploadSuccess($event) {
    this.canVerify = true;
    this.data['files'].push($event[1].file);
  }

  submit() {
    this.processing = true;
    this.canVerify = false;

    let body = new URLSearchParams();
    body.set('files', this.data['files']);
    body.set('room', this.data['room']);

    let options = {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    };

    let router = this.router;

    // Send it to the backend and start to wait for the pusher events.
    this.http.post(environment.backend + 'process_files', body.toString(), options).subscribe((data: UploadResponse) => {

      let localStorage = window.localStorage;

      if (localStorage.getItem('results_' + data.data.id) == null) {
        localStorage.setItem('results_' + data.data.id, JSON.stringify(data.data.results));
      }
      router.navigate(["/results/" + data.data.id]);
    }, err => {
      console.log(err);
    });
  }

}
