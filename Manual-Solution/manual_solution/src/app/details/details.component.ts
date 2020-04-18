import {NestedTreeControl} from '@angular/cdk/tree';
import { Component, OnInit, Input, OnChanges, Output, EventEmitter } from '@angular/core';
import {MatTreeFlatDataSource, MatTreeFlattener} from '@angular/material/tree';
import {MatTreeNestedDataSource} from '@angular/material/tree';
import {FlatTreeControl} from '@angular/cdk/tree';

interface IConnections{
  name: string;
  children?: IConnections[];
}

interface IEvent{
  name: string;
  children?: IEvent[];
}

interface FlatNode {
  expandable: boolean;
  name: string;
  level: number;
}

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.css']
})
export class DetailsComponent implements OnChanges {

  @Input() city:any;
  @Input() cities: any;
  @Output() selectedCity: EventEmitter<any> = new EventEmitter<any>();
  @Input() reset: boolean;
  private eventTree;
  private connectionTree: IConnections[];
  private citiesOrderedByCurrentPopulation = [];

  private _connectionTransformer = (node: IConnections, level: number) => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level: level,
    };
  }

  connectionTreeControl = new FlatTreeControl<FlatNode>(
    node => node.level, node => node.expandable);
  treeFlattener = new MatTreeFlattener(
      this._connectionTransformer, node => node.level, node => node.expandable, node => node.children);

  connectionDataSource = new MatTreeFlatDataSource(this.connectionTreeControl, this.treeFlattener);


  eventTreeControl = new NestedTreeControl<IEvent>(node => node.children);
  eventDataSource = new MatTreeNestedDataSource<IEvent>();

  hasConnectionChild = (_: number, node: FlatNode) => node.expandable;
  hasEventChild = (_: number, node: IEvent) => !!node.children && node.children.length > 0;


  ngOnChanges(){
    if(this.reset){
      this.citiesOrderedByCurrentPopulation = [];
      this.cities = null;
    }
    if(this.city){
      if(this.city.connections){
        this.buildConnectionsTree();
        this.connectionDataSource.data = this.connectionTree; 
      }
      if(this.city.events){
        this.buildEventTree();
      this.eventDataSource.data = this.eventTree;
      } 
    }else{
      if(this.cities){
        let citiesOrdered = [];
        for(let key in this.cities){
          citiesOrdered.push({name: key, cityObj: this.cities[key]});
        }
        citiesOrdered.sort((obj1 ,obj2) => {
          if(obj1.cityObj.population > obj2.cityObj.population){
            return 1
          }
          if(obj1.cityObj.population < obj2.cityObj.population){
            return - 1
          }
          return 0
        })
        this.citiesOrderedByCurrentPopulation = citiesOrdered.reverse();       
      }
    }
       
  }

  buildConnectionsTree(){
    let tmpChildren: IConnections[] = [];
    if(this.city.connections){
      for(var i in this.city.connections){
        tmpChildren.push({name: this.city.connections[i]})
      }
      this.connectionTree = [{
        name: "Connections (" + tmpChildren.length + ")",
        children: tmpChildren
      }]          
    }
  }

  showCityInMap(cityObj){
    this.selectedCity.emit(cityObj);
  }

  buildEventTree(){
    let tmpEvents: IEvent[] = [];
    if(this.city.events){
      for(var i in this.city.events){
        let tmpChildren: IEvent[] = []
        let tmpPathogen: IEvent[] = []
        if(this.city.events[i].pathogen){
          tmpPathogen.push({name: "Infectivity: " + this.city.events[i].pathogen.infectivity});
          tmpPathogen.push({name: "Mobility: " + this.city.events[i].pathogen.mobility});
          tmpPathogen.push({name: "Duration: " + this.city.events[i].pathogen.duration});
          tmpPathogen.push({name: "Lethality: " + this.city.events[i].pathogen.lethality});
          tmpChildren.push({name: "Prevalence: " + this.city.events[i].prevalence});
          tmpChildren.push({name: "Since Round: " + this.city.events[i].sinceRound});
          tmpChildren.push({name: "Pathogen " + this.city.events[i].pathogen.name, children: tmpPathogen})
        }        
        tmpEvents.push({name: this.city.events[i].type, children: tmpChildren})
      }
      this.eventTree = [
        {
          name: "Events (" + tmpEvents.length + ")",
          children: tmpEvents
        }
      ]
    }
  }

}
