import {Component, OnInit, Injectable} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HttpClient} from '@angular/common/http';
import {MetadataService} from "../metadata.service";


@Component({
  selector: 'op-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})

@Injectable()
export class ResultsComponent implements OnInit {

  id = '';

  constructor(private route: ActivatedRoute, private http: HttpClient, private metadata: MetadataService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.id = params.id;
    });
  }

}
