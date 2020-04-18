class CloseAirportHandler:
    type: str = "closeAirport"
    base_cost: int = 15
    cost_multiplier: int = 5
    dependencies = ["city", "rounds"]
