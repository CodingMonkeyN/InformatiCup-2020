import {IAction} from '../action';

export class LaunchCampaign implements IAction {
    type: string = "launchCampaign"
    base_cost: number = 3
    cost_multiplier: number = 0
    dependencies = ['city']

    constructor(){}
}