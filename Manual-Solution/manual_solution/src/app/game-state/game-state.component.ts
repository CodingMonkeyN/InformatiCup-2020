import { Component, OnInit, Output, EventEmitter, Input, } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Response } from '../models/response';
import { EndRoundAction } from '../models/actions/action_implementations/endRound.action';
import { IAction } from '../models/actions/action';
import { PutUnderQuarantine } from '../models/actions/action_implementations/putUnderQuarantine.action';
import { CloseAirport } from '../models/actions/action_implementations/closeAirport.action';
import { CloseConnection } from '../models/actions/action_implementations/closeConnection.action';
import { DeployVaccine } from '../models/actions/action_implementations/deployVaccine.action';
import { DevelopVaccine } from '../models/actions/action_implementations/developVaccine.action';
import { DevelopMedication } from '../models/actions/action_implementations/developMedication.action';
import { DeployMedication } from '../models/actions/action_implementations/deployMedication.action';
import { ExertInfluence } from '../models/actions/action_implementations/exertInfluence.action';
import { CallElections } from '../models/actions/action_implementations/callElections.action';
import { ApplyHygienicMeasures } from '../models/actions/action_implementations/applyHygienicMeasures.action';
import { LaunchCampaign } from '../models/actions/action_implementations/launchCampaign.action';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import {map, startWith} from 'rxjs/operators';

@Component({
  selector: 'app-game-state',
  templateUrl: './game-state.component.html',
  styleUrls: ['./game-state.component.css']
})

export class GameStateComponent implements OnInit {
  title = 'informaticup';
  // game_state = {"round": 4, "points": 30}

  @Output() currentRound: EventEmitter<any> = new EventEmitter<any>();
  @Output() globalEvents: EventEmitter<any> = new EventEmitter<any>();

  @Input()
  set city(city: any) {
    if(city){
      this.action_information.city = city.name;
    }else{
      this.action_information.city = null;
    }
    
  }

  cityControl = new FormControl();
  filteredCities: Observable<string []>;

  cities = null 
  action_information = {
    'city': null,
    'toCity': null,
    'rounds': null,
    'pathogen': null
  }

  actions = [
    new PutUnderQuarantine(),
    new CloseAirport(),
    new CloseConnection(),
    new DevelopVaccine(),
    new DeployVaccine(),
    new DevelopMedication(),
    new DeployMedication(),
    new ExertInfluence(),
    new CallElections(),
    new ApplyHygienicMeasures(),
    new LaunchCampaign()
    
  ]
  selected_action: IAction = null

  json: Response;

  action_chosen = false

  pathogens = []

  points = 0;

  gameStarted = false;

  showResult = false;

  actionBuild = false;

  result: number = 0;

  loaded: boolean;

  citiesLoaded: boolean = false;

  gamemodeSelected: boolean = false;

  citiesForFilter = [];

  gamemode: string;

  gameActions = [];

  gameRounds = [];

  pause: boolean = false;

  pauseState: string = "Pause";

  currentStrategy = null;

  strategyTooltip = null;

  round = null;

  gameFinished = false;

  waitingForNextRound = false;





  constructor(private apiService: ApiService){
    this.loaded = false;
  }
  
  ngOnInit() {

  }

  private _filter(value: string): string[] {
    let filterValue = ''
    if(value != null){
      filterValue = value.toLowerCase();
    }
    

    return this.citiesForFilter.filter(option => option.toLowerCase().startsWith(filterValue));
  }

  selectGamemode(gamemode){
    this.gamemode = gamemode
    if(this.gamemode == 'Automatic'){
      if(this.pause){
        this.pauseGame();
        this.getRoundData();
      }
      
    }
    this.gamemodeSelected = true;
  }

  startGame(){
    this.apiService.startGame().subscribe(result => {
      if(result.success){
        this.gameStarted = true;
        this.loaded = false;
        this.getRoundData();
      }
    });    
  }

  actionSwitch(){
    this.action_information = {
      'city': null,
      'toCity': null,
      'rounds': null,
      'pathogen': null
    }
  }

  resetGame(){
    this.currentRound.emit(null);
    this.globalEvents.emit(null);
    this.gameActions = [];
    this.gameStarted = false;
    this.gamemodeSelected = false;
    this.gameFinished = false;
    this.round = null;
    this.loaded = false;
  }

  getRoundData() {
    if(!this.gameFinished){
      this.apiService.getRoundData().subscribe(roundData => {
        if(roundData != null) {
            this.loaded = true;
            this.waitingForNextRound = false;
            this.showResult = true;
            this.delay(2000).then(t => this.showResult = false);
            this.points = roundData.points;
            this.currentRound.emit(roundData);
            this.round = roundData.round;
            this.buildAction(roundData.cities, roundData.events);      
            this.globalEvents.emit(roundData.events);
            this.json = roundData;
            if(roundData.outcome != "pending"){
              this.gameFinished = true;
            }
            if(this.gamemode == 'Automatic'){          
              this.apiService.getAIAction(roundData).subscribe(action => {
                this.currentStrategy = action.strategy.name;
                this.strategyTooltip = action.strategy.desc;
                this.sendAIAction(action);              
              })
            }
        }else{
          this.delay(500).then(t => this.getRoundData())        
        }      
      });
    }    
  }

  sendAIAction(action){
    if(!this.pause){
      this.gameActions.unshift({action: this.parseActionToString(action), strategy: action.strategy.name, round: this.round});
      this.apiService.sendAction(action).subscribe( x => {
      if(x.success){
        this.result = 1;
      }else{
        this.result = 2;        
      }
      this.reset();
      this.delay(500).then(t => this.getRoundData())
      this.waitingForNextRound = true;
    });
    }    
  }

  parseActionToString(action) {
    let finalString = "Typ: " + action.type;
    if(action.pathogen){
      finalString += ", Pathogen: " + action.pathogen;
    }
    if(action.city){
      finalString += ", City: " + action.city;
    }    
    if(action.toCity){
      finalString += ", To City: " + action.toCity;
    }
    if(action.rounds){
      finalString += ", Rounds: " + action.rounds;
    }
    return finalString; 
  }

  pauseGame(){    
    if(this.pause){
      this.pauseState = "Pause";
    }else{
      this.pauseState = "Resume";
    }
    this.pause = !this.pause;
  }

  buildAction(cities, events){
    this.cities = cities;
    this.pathogens = [];
    if(!this.citiesLoaded){
      for(var key in cities){
        this.citiesForFilter.push(key);
      }
      this.citiesLoaded = true;
    }
    this.filteredCities = this.cityControl.valueChanges
      .pipe(
        startWith(''),
        map(value => this._filter(value))
      );
    for(let event of events){
      if(event['type']=="pathogenEncountered"){
        this.pathogens.push(event["pathogen"])
      }
    }
    this.actionBuild = true;
  }

  submitAction(){
    let json = this.buildJson()
    this.loaded = false;
    this.gameActions.unshift({action: this.parseActionToString(json), round: this.round});
    this.apiService.sendAction(json).subscribe( x => {
      if(x.success){
        this.result = 1;
      }else{
        this.result = 2;        
      }
      this.reset();
      this.delay(500).then(t => this.getRoundData())
      this.waitingForNextRound = true;
    });

    // Hier muss theoretisch noch abgefangen werden ob die City richtig geschrieben ist

    /*this.apiService.sendAction(json).subscribe();
    this.reset();
    this.delay(500).then(t => this.getRoundData()); */
  }

  reset(){
    this.action_information.city = null;
  }

  resetAll(){
    this.selected_action = null;
    this.action_information.city = null;
    this.action_information.pathogen = null;
    this.action_information.rounds = null;
    this.action_information.toCity = null;
  }

  endRound(){
    this.loaded = false;
    /*this.apiService.sendAction({"type": "endRound"}).subscribe(x =>{
      if(x){
        this.result = 1;
      }else{
        this.result = 2;        
      }
      this.selected_action = null
      this.delay(500).then(t => this.getRoundData())
    }) */
    
    this.gameActions.unshift({action: this.parseActionToString({"type": "endRound"}), round: this.round});
    this.apiService.sendAction({"type": "endRound"}).subscribe();
    this.reset();
    this.delay(500).then(t => this.getRoundData());
  }

  buildJson(){
    let json = {'type': this.selected_action.type}
    
    if(this.action_information.city && this.action_information.toCity){
      json['fromCity'] = this.action_information.city
      json['toCity'] = this.action_information.toCity
    }
    else if(this.action_information.city){
      json['city'] = this.action_information.city
    }
    if(this.action_information.pathogen){
      json['pathogen'] = this.action_information.pathogen
    }
    if(this.action_information.rounds){
      json['rounds'] = this.action_information.rounds
    }
    return json
  }

  delay(ms: number) {
    return new Promise( resolve => setTimeout(resolve, ms) );
  }
  
}
