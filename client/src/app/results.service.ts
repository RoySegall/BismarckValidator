import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../environments/environment";

@Injectable()
export class ResultsService {

  constructor(private http: HttpClient) { }

  getResults(id: string) {
    return this.http.get(environment.backend + 'process_files/' + id);
  }

}
