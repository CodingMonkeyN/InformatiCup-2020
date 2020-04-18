import {IAction} from '../action';

export class DevelopVaccine implements IAction {
    type: string = "developVaccine"
    base_cost: number = 40
    cost_multiplier: number = 0
    dependencies = ['pathogen']

    constructor(){}
}