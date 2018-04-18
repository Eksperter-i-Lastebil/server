import { Component, ElementRef, NgZone, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';

import { MapsAPILoader } from '@agm/core';
import { } from 'googlemaps';

import { TripsService } from './trips.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'app';
  trips = [];

  public latitude: number;
  public longitude: number;
  public searchControl: FormControl;

  @ViewChild("search")
  public searchElementRef: ElementRef;

  constructor(private tripsService: TripsService,
    private mapsAPILoader: MapsAPILoader,
    private ngZone: NgZone)
    {
    this.tripsService.update().subscribe(data => {
      this.trips = data;
      //console.log(data);
    });
    
    setInterval(()=>this.getLoop(), 5000);
  };

	ngOnInit() {
    //set google maps defaults
    //this.latitude = 37.33039592;
    //this.longitude = -122.0293017;

    //create search FormControl
    this.searchControl = new FormControl();

    //set current position
    this.setCurrentPosition();

    //load Places Autocomplete
    this.mapsAPILoader.load().then(() => {
      let autocomplete = new google.maps.places.Autocomplete(this.searchElementRef.nativeElement, {
        types: ["(cities)"]
      });
      autocomplete.addListener("place_changed", () => {
        this.ngZone.run(() => {
          //get the place result
          let place: google.maps.places.PlaceResult = autocomplete.getPlace();

          //verify result
          if (place.geometry === undefined || place.geometry === null) {
            return;
          }

          //set latitude, longitude and zoom
          this.latitude = place.geometry.location.lat();
          this.longitude = place.geometry.location.lng();
          //console.log(this.latitude + " " + this.longitude);
        });
      });
    });
  }

  public getLoop()
  {
    this.tripsService.update().subscribe(data => {
      //console.log("yeap");
      this.trips = data;
      for(var i = 0; i < this.trips.length; i++) {
        this.trips[i].type = this.trips[i].type.slice(2).toLowerCase().replace(" ", "").split(",");
      }
      //console.log(this.trips);
      });
  }

	private setCurrentPosition() {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        this.latitude = position.coords.latitude;
        this.longitude = position.coords.longitude;
      });
    }
  }

  setColor(trip)
  {
    if(trip == "stroying")
    {
      return 'tomato';
    }
    else if(trip == "broyting")
    {
      return 'Orange';
    }
    else if(trip == "fresing")
    {
      return 'DodgerBlue';
    }
    else if(trip == "salting")
    {
      return 'MediumSeaGreen';
    }
    else if(trip == "skraping")
    {
      return 'SlateBlue';
    }
  }

  setOpacity(trip)
  {
    var unix = Math.round(+new Date()/1000);
    var diff = unix - trip.time;

    //onsole.log(diff);
    //factor = trip.time/diff;
    var factor = diff/60;
    //console.log(factor);
    return 1 - factor;
    //console.log(trip.timestamp);
  }

  toFloat(number) {
    return parseFloat(number);
  }
}
