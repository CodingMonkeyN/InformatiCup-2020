import {IAction} from '../action';

export class EndRoundAction implements IAction {
    type: string = "endRound"
    base_cost: number = 0
    cost_multiplier: number = 0
    dependencies = []

    constructor(){}
}