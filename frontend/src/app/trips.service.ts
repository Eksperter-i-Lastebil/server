import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class TripsService {
  constructor(
    private http: HttpClient) { }

  update() {
    return this.http.get<Object[]>("/api");
  }

}
