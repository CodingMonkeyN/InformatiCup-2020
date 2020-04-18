import {IAction} from '../action';

export class PutUnderQuarantine implements IAction {
    type: string = "putUnderQuarantine"
    base_cost: number = 20
    cost_multiplier: number = 10
    dependencies = ["city", "rounds"]

    constructor(){}
}