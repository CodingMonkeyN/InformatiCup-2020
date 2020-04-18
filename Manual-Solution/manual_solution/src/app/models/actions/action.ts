export interface IAction {
    type: string,
    base_cost: number,
    cost_multiplier: number,
    dependencies: string[]

}