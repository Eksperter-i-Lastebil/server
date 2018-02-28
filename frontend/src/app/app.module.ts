import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HttpHeaders } from '@angular/common/http';
import {FormsModule, FormControl, ReactiveFormsModule} from '@angular/forms';

import { AppComponent } from './app.component';
import { AgmCoreModule } from '@agm/core';
import { TripsService } from './trips.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyCI_x52g169wIOv7HbXB-fb6fVObUCcr08',
      libraries: ["places"]
    })
  ],
  providers: [TripsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
