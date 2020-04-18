import {IAction} from '../action';

export class ApplyHygienicMeasures implements IAction {
    type: string = "applyHygienicMeasures"
    base_cost: number = 3
    cost_multiplier: number = 0
    dependencies = ['city']

    constructor(){}
}