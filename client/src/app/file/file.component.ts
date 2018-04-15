import {Component, OnInit, Input} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {MetadataService} from "../metadata.service";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {ResultsService} from "../results.service";
import {ResultsInterface} from "../ResultsInterface";

@Component({
  selector: 'op-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.scss']
})
export class FileComponent implements OnInit {

  id = '';
  results = [];
  processing = false;
  activeClass = '';
  tabs_maximum = {};
  meta = {};
  filename = '';

  @Input() name: string;

  constructor(private route: ActivatedRoute, private http: HttpClient, private metadata: MetadataService, private resultsService: ResultsService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.id = params.id;
      this.filename = params.file;
      this.metadata.getMetadata().subscribe(data => {
        this.meta = data;

        this.resultsService.getResults(params.id).subscribe((response: ResultsInterface) => {

          let results = response.results;

          if (results != null) {
            this.processing = true;
            this.results = this.processData(results, this.filename);
            this.processing = false;
          }
          else {
            this.processing = true;

            this.http.get(environment.backend + 'process_files/' + params.id).subscribe((data: ProcessResponse) => {
              // Process the results.
              this.processData(data.results, this.filename);
              this.processing = false;
            }, err => {
              console.log(err);
            })
          }
        });
      });
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
    let self = this;

    self.tabs_maximum[file] = {};

    Object.keys(results[file]).forEach(tab => {

      Object.keys(results[file][tab]).forEach(column => {

        self.tabs_maximum[tab] = Object.keys(results[file][tab][column]).map(key => {
          return parseInt(key);
        })
      })
    });

    return results[file];
  }

  public setTab(tab) {
    this.activeClass = tab;
  }

}
