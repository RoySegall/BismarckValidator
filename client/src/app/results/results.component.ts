import { Component, OnInit, Injectable } from '@angular/core';
import {Router, ActivatedRoute} from "@angular/router";

@Component({
  selector: 'op-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})

@Injectable()
export class ResultsComponent implements OnInit {

  results = [];

  constructor(private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.params.subscribe(params => {

      let results = window.localStorage.getItem('results_' + params.id);

      if (results != null) {
        let parsed_results = JSON.parse(results);

        Object.keys(parsed_results).forEach(file => {
          let file_results = '<b>' + file + '</b>:';

          Object.keys(parsed_results[file]).forEach(tab => {
            file_results += '<div><b>' + tab + '</b><div>';

            Object.keys(parsed_results[file][tab]).forEach(line => {
              file_results += line + '<ul>';

              Object.keys(parsed_results[file][tab][line]).forEach(item => {
                Object.keys(parsed_results[file][tab][line][item]).forEach(error => {
                  file_results += '<li>' + parsed_results[file][tab][line][item][error] + '</li>';
                });
              });

              file_results += '</ul>';
            });

            file_results += '</div></div>';
          });

          this.results.push(file_results);
        });
      }
    });
  }

}
