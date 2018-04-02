import {Component, OnInit, Input} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {MetadataService} from "../metadata.service";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Component({
  selector: 'op-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.scss']
})
export class FileComponent implements OnInit {

  results = [];
  processing = false;
  activeClass = '';
  tabs_maximum = {};
  meta = {};
  filename = '';

  @Input() name: string;

  constructor(private route: ActivatedRoute, private http: HttpClient, private metadata: MetadataService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let item_id = 'results_' + params.id;
      this.filename = params.file;
      let results = window.localStorage.getItem(item_id);
      this.metadata.getMetadata().subscribe(data => this.meta = data)

      if (results != null) {
        this.results = this.processData(results, this.filename);
      }
      else {
        this.processing = true;

        this.http.get(environment.backend + 'process_files/' + params.id).subscribe((data: ProcessResponse) => {
          // Process the results.
          this.processData(data.results, this.filename);
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
   * @param file
   *   The name of the file.
   */
  protected processData(results, file) {
    this.activeClass = 'cash';
    let parsed_data = JSON.parse(results);
    let self = this;

    self.tabs_maximum[file] = {};

    Object.keys(parsed_data[file]).forEach(tab => {

      Object.keys(parsed_data[file][tab]).forEach(column => {

        self.tabs_maximum[tab] = Object.keys(parsed_data[file][tab][column]).map(key => {
          return parseInt(key);
        })
      })
    });

    return parsed_data[file];
  }

  public setTab(tab) {
    this.activeClass = tab;
  }

}
