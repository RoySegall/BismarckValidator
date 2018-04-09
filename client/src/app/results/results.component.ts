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

  results = [];
  id = '';
  stats = {};

  constructor(private route: ActivatedRoute, private http: HttpClient, private metadata: MetadataService) {
  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.id = params.id;

      // Todo: handle if not found.
      this.results = JSON.parse(window.localStorage.getItem('results_' + params.id));
      this.stats = {
        'filesCount': Object.keys(this.results).length,
        'errors': [
          {'text': 'מטבע לא מזוהה - שקל חדש', 'times': 5},
          {'text': 'מטבע לא מזוהה - כתר שבדי', 'times': 10},
          {'text': 'אחרי 0 צריכים להיות 2 מספרים', 'times': 9},
          {'text': 'DD/MM/YYYY הוא לא פורמט תקין', 'times': 30},
        ],
      };
    });
  }
}
