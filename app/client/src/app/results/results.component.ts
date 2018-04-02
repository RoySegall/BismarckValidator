import {Component, OnInit, Injectable} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HttpClient} from '@angular/common/http';
import {environment} from "../../environments/environment";
import {MetadataService} from "../metadata.service";


@Component({
  selector: 'op-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})

@Injectable()
export class ResultsComponent implements OnInit {

  results = [];

  processing = false;

  activeClass = '';

  tabs_maximum = [];

  meta = {}

  constructor(private route: ActivatedRoute, private http: HttpClient, private metadata: MetadataService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let item_id = 'results_' + params.id;

      let results = window.localStorage.getItem(item_id);

      this.metadata.getMetadata().subscribe(data => this.meta = data)

      if (results != null) {
        this.results = this.processData(results);
      }
      else {
        this.processing = true;

        this.http.get(environment.backend + 'process_files/' + params.id).subscribe((data: ProcessResponse) => {
          // Process the results.
          this.processData(data.results);
          this.processing = false;

          // Save the data for later.
          window.localStorage.setItem(item_id, JSON.stringify(data.results));
        }, err => {
          console.log(err);
        })
      }
    });
  }

  /**
   * Process the results into HTML.
   *
   * @param results
   *   The response, could be from the local storage or from an HTTP request in case it does not exists there.
   */
  protected processData(results) {
    this.activeClass = 'cash';
    let parsed_data = JSON.parse(results);
    let self = this;

    Object.keys(parsed_data).forEach(file => {
      self.tabs_maximum[file] = {};

      Object.keys(parsed_data[file]).forEach(tab => {

        Object.keys(parsed_data[file][tab]).forEach(column => {

          self.tabs_maximum[file][tab] = Object.keys(parsed_data[file][tab][column]).map(key => {
            return parseInt(key);
          })
        })
      })
    });

    return parsed_data;
  }

  public setTab(tab) {
    this.activeClass = tab;
  }

}
