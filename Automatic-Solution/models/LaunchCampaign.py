class LaunchCampaign():
    type: str = "launchCampaign"
    base_cost: int = 3
    cost_multiplier: int = 0
    dependencies = ['city']