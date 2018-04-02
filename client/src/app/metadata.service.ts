import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from "../environments/environment";

@Injectable()
export class MetadataService {

  constructor(private http: HttpClient) { }

  metadata = {}

  getMetadata() {
    return this.http.get(environment.backend + 'metadata');
  }

}
