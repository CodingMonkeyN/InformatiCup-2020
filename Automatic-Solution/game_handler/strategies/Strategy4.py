from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import SavePoints
from game_handler.strategies import Strategy


class Strategy4(Strategy.Strategy):

    def __init__(self):
        self.description = {"name": "Kill Adi", "desc": "Isolate Admiral Trips."}

    def implement(self, game_object: GameObject, min_lethality = 0):
        # ROUND 1: QUARANTINE
        if game_object.basic_game_information.points >= 40:
            for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
                if pathogen_with_cities["name"] == "Admiral Trips":
                    city_name = pathogen_with_cities["infectedCities"][0]
                    city = game_object.basic_game_information.cities[city_name]
                    quarantine = None
                    if "events" in city:
                        for event in city["events"]:
                            if event["type"] == "quarantine":
                                quarantine = event
                    if not quarantine:
                        return {"type": "putUnderQuarantine", "city": city_name, "rounds": 2}
        return {"type": "endRound"}