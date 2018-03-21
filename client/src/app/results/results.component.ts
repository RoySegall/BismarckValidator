import {Component, OnInit, Injectable} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {HttpClient} from '@angular/common/http';
import {environment} from "../../environments/environment";


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

  constructor(private route: ActivatedRoute, private http: HttpClient) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      let item_id = 'results_' + params.id;

      let results = window.localStorage.getItem(item_id);

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
    let parsed_results = results;
    this.activeClass = 'cash';

    return JSON.parse(results);
  }

  public setTab(tab) {
    this.activeClass = tab;
  }

}
