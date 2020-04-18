import {IAction} from '../action';

export class DevelopMedication implements IAction {
    type: string = "developMedication"
    base_cost: number = 20
    cost_multiplier: number = 0
    dependencies = ['pathogen']

    constructor(){}
}