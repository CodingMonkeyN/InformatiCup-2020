class DeployMedication():
    type: str = "deployMedication"
    base_cost: int = 10
    cost_multiplier: int = 0
    dependencies = ['city', 'pathogen']