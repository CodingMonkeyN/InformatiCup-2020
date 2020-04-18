class CloseConnection():
    type: str = "closeConnection"
    base_cost: int = 3
    cost_multiplier: int = 3
    dependencies = ["city", "toCity", "rounds"]
