import {IAction} from '../action';

export class DeployVaccine implements IAction {
    type: string = "deployVaccine"
    base_cost: number = 5
    cost_multiplier: number = 0
    dependencies = ['city', 'pathogen']

    constructor(){}
}