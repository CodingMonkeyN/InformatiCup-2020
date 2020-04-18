import {IAction} from '../action';

export class CloseConnection implements IAction {
    type: string = "closeConnection"
    base_cost: number = 3
    cost_multiplier: number = 3
    dependencies = ["city", "toCity", "rounds"]

    constructor(){}
}