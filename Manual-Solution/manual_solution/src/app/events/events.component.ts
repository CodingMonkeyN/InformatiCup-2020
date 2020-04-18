import { Component, OnInit, EventEmitter, Input, Output, OnChanges, ViewChild } from '@angular/core';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';

interface event {
  type: string;
  round: number;
  pathogen: pathogen;
  prevalence: number;
  sinceRound: number;
  untilRound: number;

}

interface pathogen {
  name: string;
  infectivity: string;
  mobility: string;
  duration: string;
  lethality: string;
}


@Component({
  selector: 'app-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.css']
})

export class EventsComponent implements OnChanges {
  displayedColumns: string[] = ['round', 'type', 'pathogen', 'infectivity', 'mobility', 'duration', 'lethality', 'prevalence', 'sinceRound', 'untilRound'];
  dataSource;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @Input() events: event;
  @Input() colors: any;
  @Output() selectedPathogen : EventEmitter<any> = new EventEmitter<any>();
  constructor() {

   }

  ngOnChanges(){    
    this.parseEventsToRowData();
    this.dataSource.paginator = this.paginator;
  }

  setStyles(row){
    if(row.type == "pathogenEncountered"){
      return {'background-color': row.color };
    }    
  }

  getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
  }

  pathogenSelected(row){
    this.selectedPathogen.emit(row); 
  }

  parseEventsToRowData(){
    
    let data = [];
    for(let i in this.events){
      let event = {};   
      if(this.events[i].pathogen){
        let color = null;
        this.colors.filter(x => {
          if(x.name == this.events[i].pathogen.name){
            color = x.color;
          }}
          );
        event = { 
          type: this.events[i].type, 
          round:  this.events[i].round,
          prevalence:  this.events[i].prevalence, 
          sinceRound:  this.events[i].sinceRound, 
          untilRound:  this.events[i].untilRound, 
          pathogen:  this.events[i].pathogen.name,
          infectivity: this.events[i].pathogen.infectivity,
          mobility: this.events[i].pathogen.mobility,
          duration: this.events[i].pathogen.duration,
          lethality: this.events[i].pathogen.lethality,
          color:  color}
      }else{
        event = { 
          type: this.events[i].type, 
          round:  this.events[i].round,
          prevalence:  this.events[i].prevalence, 
          sinceRound:  this.events[i].sinceRound, 
          untilRound:  this.events[i].untilRound, 
          pathogen: " ",
          infectivity: " ",
          mobility: " ",
          duration: " ",
          lethality: " ", 
        }
          
      }         
      data.push(event);
    }
    this.dataSource = new MatTableDataSource(data);
  }

}
