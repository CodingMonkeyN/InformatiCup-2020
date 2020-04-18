from GameObject import GameObject
from game_handler import ActionDependencySolver
from game_handler.strategies import Strategy, Foreseer
from random import randrange

class Strategy11(Strategy.Strategy):

    def __init__(self):
        self.description = {"name": "Shut down new Pathogen", "desc": "Shutting down new Pathogen"}

    def implement(self, game_object: GameObject, pathogen_with_cities):
        pathogen_with_cities = pathogen_with_cities[len(pathogen_with_cities)-1]
        city_name = pathogen_with_cities["infectedCities"][0]
        city = game_object.basic_game_information.cities[city_name]
        quarantine_event = None
        if "events" in city:
            for event in city["events"]:
                if event["type"] == "quarantine":
                    quarantine_event = event
        if quarantine_event == None:
            max_rounds = int((game_object.basic_game_information.points-20)/10)
            if max_rounds > 1:
                if max_rounds > 6:
                    max_rounds = 6
                return {"type": "putUnderQuarantine","city": city_name, "rounds": max_rounds}
            else:
                return {"type": "endRound"}
        else:
            if pathogen_with_cities["name"] in game_object.extracted_game_information.pathogens_with_medication_available: 
                if game_object.basic_game_information.points >= 10:
                    return {"type": "deployMedication", "city": city_name, "pathogen": pathogen_with_cities["name"]}
                else:
                    return {"type": "endRound"}
            else:
                if pathogen_with_cities["name"] not in game_object.extracted_game_information.pathogens_with_medication_in_development:
                    if game_object.basic_game_information.points >= 20 and (quarantine_event["untilRound"] - game_object.basic_game_information.round)*20 >= 60 :
                        return {"type": "developMedication", "pathogen": pathogen_with_cities["name"]}
                    else:
                        return {"type": "endRound"}
                else:
                    return {"type": "endRound"}
        return {"type": "endRound"}
                    
            
