from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import SavePoints
from game_handler.strategies import Strategy


class Strategy3(Strategy.Strategy):

    def __init__(self):
        self.description = {"name": "Save Tokio", "desc": "Save biggest City if only 1 lethal pathogen"}

    def implement(self, game_object: GameObject, min_lethality = 0):
        # ROUND 1: QUARANTINE
        if game_object.basic_game_information.points >= 40:
            return self.SaveTokio(game_object)
        elif game_object.basic_game_information.points < 30:
           return self.fill_action(game_object, SavePoints.SavePoints())

    def SaveTokio(self, game_object: GameObject):
        cities = game_object.basic_game_information.cities
        cities = sorted(cities, key=lambda city: cities[city]["population"])
        city = game_object.basic_game_information.cities[cities.pop()]
        max_rounds = int((game_object.basic_game_information.points-20)/10)
        if max_rounds > 1:
            if max_rounds > 4:
                max_rounds = 4
            quarantine = None
            if "events" in city:
                for event in city["events"]:
                    if event["type"] == "quarantine":
                        quarantine = event
            if not quarantine:
                return {"type": "putUnderQuarantine", "city": city["name"], "rounds": max_rounds}
            else:
                return {"type": "endRound"}
        else:
            return {"type": "endRound"}
