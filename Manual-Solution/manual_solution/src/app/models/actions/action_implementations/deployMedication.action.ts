import {IAction} from '../action';

export class DeployMedication implements IAction {
    type: string = "deployMedication"
    base_cost: number = 10
    cost_multiplier: number = 0
    dependencies = ['city', 'pathogen']

    constructor(){}
}