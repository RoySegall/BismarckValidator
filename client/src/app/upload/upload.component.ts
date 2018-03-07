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

  data = {
    'files': [],
    'room': Date.now()
  };

  canUpload = false;

  constructor(private http: HttpClient, private router: Router) {
  }

  ngOnInit() {
  }

  onUploadError($event) {
  }

  onUploadSuccess($event) {
    this.canUpload = true;
    this.data['files'].push($event[1].file);
  }

  submit() {

    let body = new URLSearchParams();
    body.set('files', this.data['files']);
    body.set('room', this.data['room']);

    let options = {
      headers: new HttpHeaders().set('Content-Type', 'application/x-www-form-urlencoded')
    };

    let router = this.router;

    // Send it to the backend and start to wait for the pusher events.
    this.http.post(environment.backend + 'process_files', body.toString(), options).subscribe(data => {
      router.navigate(["/results/" + data.data.id]);
    }, err => {
      console.log(err);
    });
  }

}
