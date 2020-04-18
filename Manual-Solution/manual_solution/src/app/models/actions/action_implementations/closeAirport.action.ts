import {IAction} from '../action';

export class CloseAirport implements IAction {
    type: string = "closeAirport"
    base_cost: number = 15
    cost_multiplier: number = 5
    dependencies = ["city", "rounds"]

    constructor(){}
}