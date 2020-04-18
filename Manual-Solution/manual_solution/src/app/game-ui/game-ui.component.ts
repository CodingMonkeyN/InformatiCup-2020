import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-game-ui',
  templateUrl: './game-ui.component.html',
  styleUrls: ['./game-ui.component.css']
})
export class GameUIComponent implements OnInit {

  city: any;

  events: any;

  game_state: any;

  pathogen: any;

  colors: any = [];
  
  colorDef = ['#FF00FF', '#34495E', '#F5CBA7', '#b2ffff', '#808000', '#6e4667', '#776a5e', '#ccccff', '#00ff8c', '#ded6dd'];

  numberOfPathogens: number;

  colorsSet = false;

  reset = false;


  onSelectedCityChanged(selectedCity: any):void{
    this.city = selectedCity;
  }

  onCurrentRoundChanged(currentRound: any): void {
    if(currentRound){
      this.reset = false;
      this.game_state = currentRound;
    }else{
      this.reset = true;
    }
     
  }

  onGlobalEventChanged(globalEvents: any): void {
    this.numberOfPathogens = 0;
    this.colors = [];
    for(var i in globalEvents){
      if(globalEvents[i].type == 'pathogenEncountered'){
        this.colors.push({
          name: globalEvents[i].pathogen.name,
          color: this.colorDef[this.numberOfPathogens] /*globalEvents[i].pathogen.color*/
        });
        this.numberOfPathogens = this.numberOfPathogens+1;
      }
              
    }
     this.events = globalEvents;
     
  }

  onSelectedPathogenChanged(selectedPathogen: any): void{
    this.pathogen = selectedPathogen;
  }


  constructor() { }

  ngOnInit() {
  }

}
