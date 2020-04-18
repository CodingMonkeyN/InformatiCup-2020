import {IAction} from '../action';

export class ExertInfluence implements IAction {
    type: string = "exertInfluence"
    base_cost: number = 3
    cost_multiplier: number = 0
    dependencies = ['city']

    constructor(){}
}