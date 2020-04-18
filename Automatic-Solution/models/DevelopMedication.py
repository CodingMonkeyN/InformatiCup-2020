class DevelopMedication():
    type: str = "developMedication"
    base_cost: int = 20
    cost_multiplier: int = 0
    dependencies = ['pathogen']