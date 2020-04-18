declare var require: any;
import { Component, OnInit, Output, EventEmitter, Input, OnChanges } from '@angular/core';
import { Chart } from 'angular-highcharts';
import BoostModule from 'highcharts/modules/boost';

interface IPopulation {
  population: number;
}
 
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnChanges {

  @Output() selectedCity: EventEmitter<any> = new EventEmitter<any>();
  @Input()
  set cities (cities: any) {
    if(cities){
      this.currentCities = cities;
      if(!this.mapBuild){
        this.buildMapData(cities);
      }else {
        
        if(!this.connectionDrawn){
          for(var index in this.chartObjekt.ref.series){ 
            this.updateCityData(this.chartObjekt.ref.series[index], cities);
          }
        }        
        if(this.connectionDrawn){
          this.updateConnectionDrawnCities(cities)
        }        
        this.chartObjekt.ref.redraw(false);
      }
      this.calculateCurrentPopulation(cities);
    }else{
      this.resetMap();
    }
    
  }
  @Input() currentRound: number;
  @Input() outcome: string;
  @Input()
  set pathogen(pathogen: any) {
     if(this.chartObjekt.ref){
        this.setVisible(false);
        for(var index in this.chartObjekt.ref.series){
          if(this.chartObjekt.ref.series[index].userOptions.data[0].events){
            for(var i in this.chartObjekt.ref.series[index].userOptions.data[0].events){
              if(this.chartObjekt.ref.series[index].userOptions.data[0].events[i].type == 'outbreak' && this.chartObjekt.ref.series[index].userOptions.data[0].events[i].pathogen && this.chartObjekt.ref.series[index].userOptions.data[0].events[i].pathogen.name == pathogen.pathogen){
                this.chartObjekt.ref.series[index].update({
                  visible: true
                }, false, false)
              }
            }
          }           
        }
        this.chartObjekt.ref.redraw(false);
     }     
  }
  @Input() colors: any;

  @Input() 
  set reset(reset: boolean) {
    if(reset){
      this.resetMap();
    }
  };

  @Input() events: any;

    chartObjekt: any;
    cityPopulationDic: { [name: string]: IPopulation } = {};
    dictionaryBuild = false;
    mapBuild = false;
    connectionDrawn = false;
    currentPopulation: number = 0;
    maxPopulation: number = 0;
    currentPopulationPercentage = 100.0;
    cityWithMostPop = {name: '', population: 0}
    drawConnectionData: any;
    currentlySelectedCity = null;
    currentCities = [];   
  

  createChart(){
    this.chartObjekt = new Chart({
      chart: {
        plotBackgroundImage: 'http://paul-reed.co.uk/images/atlas1.jpg',
        animation: false,
        spacing: [0,0,0,0],
        events: {
          click: function(e){
            this.selectedCity.emit(null);
            this.setVisible(true);
            this.removeDrawnConnection();
            for(var index in this.chartObjekt.ref.series){
              this.updateCityData(this.chartObjekt.ref.series[index], this.currentCities);
            }
            this.chartObjekt.ref.redraw(false);
          }.bind(this)
        }
      },
      title: {text: ''},
     xAxis: {
       min: -180,
       max: 180,
       visible: false
     },
     yAxis: {
       min: -90,
       max: 90,
       visible: false
     },
     tooltip: {
       pointFormat: ''
     },
     series: [],
     legend: {enabled: false},
     credits: {enabled: false},
     plotOptions: {
       series: {
         color: '#000000',
         stickyTracking: false,
         states: {
           hover: {
             enabled: false
           },
           inactive: {
            opacity: 1
          }
         },
         marker: {symbol: 'triangle-down'},
         events: {
           click: function(e){
             this.currentlySelectedCity = e.point.options
             this.selectedCity.emit(this.currentlySelectedCity);
             if(this.currentlySelectedCity.connections){
              this.drawConnection(e.point, this.currentlySelectedCity.connections);
             }             
           }.bind(this)
         }
       }      
     }
 
    });
   }
  constructor() {
    this.createChart();
  }
 
 ngOnChanges(){
   
  }

  resetMap(){
    if(this.chartObjekt.ref){
      this.chartObjekt.ref.series = [];
      this.currentRound = null;
      this.currentPopulation = null;
      this.currentPopulationPercentage = null;
      this.outcome = null;
      this.cityPopulationDic = {};
      this.dictionaryBuild = false;
      this.mapBuild = false;
      this.connectionDrawn = false;
      this.currentPopulation = 0;
      this.maxPopulation = 0;
      this.currentPopulationPercentage = 100.0;
      this.cityWithMostPop = {name: '', population: 0}
      this.currentlySelectedCity = null;
      this.currentCities = [];  
      this.chartObjekt.ref.destroy();
      this.createChart();
    }
    
  }

  setPathogenColor(events, seriesColor){
    let color = seriesColor;
    this.colors.filter(x => {     
      for(var i in events){
        if(events[i].pathogen && events[i].type == 'outbreak'){
            if((x.name == events[i].pathogen.name)){
              color = x.color;
            }
        }
      }        
    });
    return color;
    
  }


  buildMapData(cities){
      for(let key in cities){    
        if(!this.dictionaryBuild){
          this.cityPopulationDic[key] = {population: cities[key].population};
        }
        this.maxPopulation += cities[key].population;
        let tmpCity = {name: key, population: cities[key].population}
        if(tmpCity.population > this.cityWithMostPop.population){
          this.cityWithMostPop = tmpCity;
        }
        let tmpCities = cities;    
        tmpCities[key].data = [];
        tmpCities[key].data.push({
          x: tmpCities[key].longitude, 
          y: tmpCities[key].latitude, 
          name: tmpCities[key].name, 
          population: tmpCities[key].population,
          connections: tmpCities[key].connections,
          events: tmpCities[key].events,
          economy: tmpCities[key].economy,
          government: tmpCities[key].government,
          hygiene: tmpCities[key].hygiene,
          awareness: tmpCities[key].awareness
        });
        //delete tmpCities[key].latitude;
        //delete tmpCities[key].longitude;
        let lineColor = this.seriesColor(key, tmpCities[key].population);
        if(tmpCities[key].events){
          for(var i in tmpCities[key].events){
            if(tmpCities[key].events[i].pathogen){
              lineColor = this.setPathogenColor(tmpCities[key].events, this.seriesColor(key, tmpCities[key].population));
            }
          }          
        }
        this.chartObjekt.addSeries({
          type: 'line',
          name: key,
          hover: {enabled: false},
          marker: {fillColor: this.seriesColor(key, tmpCities[key].population), lineColor: lineColor, lineWidth: 2},
          data: tmpCities[key].data, 
        }, false, false);
      }   
      this.chartObjekt.ref.redraw(false);
      this.dictionaryBuild = true;
      this.mapBuild = true;
     
  }

  calculateCurrentPopulation(cities){
    this.currentPopulation = 0;
    for(let key in cities){
      this.currentPopulation += cities[key].population;
    }
    this.currentPopulationPercentage = Math.round(((this.currentPopulation / this.maxPopulation) * 100)) * 100 / 100;
  }

  updateCityData(series, cities){
    for(let key in cities){
      if(key == series.name){
        let city = cities[key];
        let newData = [];
        newData.push({
          x: city.longitude, 
          y: city.latitude, 
          name: city.name, 
          population: city.population,
          connections: city.connections,
          events: city.events,
          economy: city.economy,
          government: city.government,
          hygiene: city.hygiene,
          awareness: city.awareness
        })
        let lineColor = this.seriesColor(key, city.population);
        if(city.events){
          for(var i in city.events){
            if(city.events[i].pathogen){
              lineColor = this.setPathogenColor(city.events, this.seriesColor(key, city.population));
            }
          }          
        }
        series.update({
          marker: {fillColor: this.seriesColor(key, city.population), lineColor: lineColor},
          data: newData
        }, false, false)
      }
    }
    
  }
  updateConnectionDrawnCities(cities){
    for(let index in this.chartObjekt.ref.series){
      let series = this.chartObjekt.ref.series[index];
      let newData = [];
      if(series.name == 'connection'){
        for(let i in series.userOptions.data){
          let cityName = series.userOptions.data[i].name;
          if(this.currentlySelectedCity.name == cityName){
            if(this.currentlySelectedCity.population != cities[cityName].population 
              || this.currentlySelectedCity.events != cities[cityName].events 
              || this.currentlySelectedCity.economy != cities[cityName].economy 
              || this.currentlySelectedCity.government != cities[cityName].government
              || this.currentlySelectedCity.hygiene != cities[cityName].hygiene
              || this.currentlySelectedCity.awareness != cities[cityName].awareness){
              this.currentlySelectedCity = cities[cityName];
              this.selectedCity.emit(this.currentlySelectedCity);
            }            
          }
          newData.push({
            x: cities[cityName].longitude, 
            y: cities[cityName].latitude, 
            name: cities[cityName].name, 
            population: cities[cityName].population,
            connections: cities[cityName].connections,
            color:  this.seriesColor(cityName, cities[cityName].population),
            events: cities[cityName].events,
            economy: cities[cityName].economy,
            government: cities[cityName].government,
            hygiene: cities[cityName].hygiene,
            awareness: cities[cityName].awareness
          })
        }        
        series.update({
          data: newData
        }, false, false)
      }
    }
  }

  drawConnection(point, connections){    
    if(!this.connectionDrawn){
      let data = [];
      if(connections.length > 0){
        for(var i in connections){      
          let result = this.chartObjekt.ref.series.filter(series => series.name == connections[i])[0];
          let resultPointData = result.userOptions.data[0];
          data.push({
            x: point.x, 
            y: point.y, 
            name: point.name, 
            color: point.series.userOptions.marker.fillColor,
            population: point.population,
            connections: point.connections,
            events: point.events,
            economy: point.economy,
            government: point.government,
            hygiene: point.hygiene,
            awareness: point.awareness
          });
          data.push({
            x: resultPointData.x, 
            y: resultPointData.y, 
            name: resultPointData.name, 
            color: result.userOptions.marker.fillColor,
            population: resultPointData.population,
            connections: resultPointData.connections,
            events: resultPointData.events,
            economy: resultPointData.economy,
            government: resultPointData.government,
            hygiene: resultPointData.hygiene,
            awareness: resultPointData.awareness
          });
        }
      }else{
        data.push({
          x: point.x, 
          y: point.y, 
          name: point.name, 
          color: point.series.userOptions.marker.fillColor,
          population: point.population,
          connections: point.connections,
          events: point.events,
          economy: point.economy,
          government: point.government,
          hygiene: point.hygiene,
          awareness: point.awareness
        });
      }      
      this.setVisible(false);    
      this.chartObjekt.ref.addSeries({
        type: 'line',
        name: 'connection',
        data: data
      },true, false);
    }
    this.connectionDrawn = true;    
  }

  removeDrawnConnection(){
    for(var index in this.chartObjekt.ref.series){
      let series = this.chartObjekt.ref.series[index];
      if(series.name == 'connection'){
        series.remove(false, false);
      }
    }
    this.chartObjekt.ref.redraw(false);
    this.connectionDrawn = false;
  }

  setVisible(bool){
    for(var index in this.chartObjekt.ref.series){
      let series = this.chartObjekt.ref.series[index];
        series.update({visible: bool}, false, false);
    }
    this.chartObjekt.ref.redraw(false);
  }
 
 comparePopulationDiff(key, currentPopulation){
    if(this.cityPopulationDic[key].population == currentPopulation){
      return 0
    }else if((currentPopulation / this.cityPopulationDic[key].population * 100) > 75){
      return 1
    }else if((currentPopulation / this.cityPopulationDic[key].population * 100) > 50 ){
      return 2
    }else if((currentPopulation / this.cityPopulationDic[key].population * 100) > 25){
      return 3
    }else if((currentPopulation / this.cityPopulationDic[key].population * 100) > 0){
      return 4
    }
 }



 seriesColor(key, currentPopulation){
  switch (this.comparePopulationDiff(key, currentPopulation)) {
    case 0: // Population at 100%
      return "#39ff14"
    case 1: // Population > 75%
      return "#d4ff14"
    case 2: // Population  > 50%
      return "#ffd900"
    case 3: // Populatiuon > 25%
      return "#ff7300"
    case 4: // Populatiuon > 0%
      return "#FF0000"
  }
 }


  
  
 
}
 

