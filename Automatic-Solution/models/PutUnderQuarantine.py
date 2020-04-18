class PutUnderQuarantine():
    type: str = "putUnderQuarantine"
    base_cost: int = 20
    cost_multiplier: int = 10
    dependencies = ["city", "rounds"]