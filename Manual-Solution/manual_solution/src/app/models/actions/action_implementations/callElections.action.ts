import {IAction} from '../action';

export class CallElections implements IAction {
    type: string = "callElections"
    base_cost: number = 3
    cost_multiplier: number = 0
    dependencies = ['city']

    constructor(){}
}