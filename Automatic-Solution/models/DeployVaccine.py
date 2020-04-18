class DeployVaccine():
    type: str = "deployVaccine"
    base_cost: int = 5
    cost_multiplier: int = 0
    dependencies = ['city', 'pathogen']
