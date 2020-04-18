from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import DeployMedication, DeployVaccine
from random import randrange
from game_handler.strategies import Strategy

class Foreseer():
    game_object = None

    def __init__(self, game_object: GameObject):
        self.game_object = game_object

    def shouldDevelopVaccine(self):
        return True

    def shouldDevelopMedication(self):
        return True
        
    def selectAction(self, game_object: GameObject):
        actions = self.forseeActionValues(game_object)
        if len(actions) == 0:
            return None
        else:
            return actions.pop()["action"]

    def forseeActionValues(self, game_object: GameObject):
        actions = []
        action = self.shouldDeployVaccine()
        if action["points"] != -1:
            actions += [action]
        action = self.shouldDeployMedication()
        if action["points"] != -1:
            actions += [action]
        actions = sorted(actions, key=lambda action: action["points"])
        return actions


    def shouldDeployVaccine(self):
        if len(self.game_object.extracted_game_information.pathogens_with_vaccination_available) > 0 and self.game_object.basic_game_information.points >= 5:
            if self.game_object.basic_game_information.round <= 20 or self.game_object.basic_game_information.round > 20 and self.game_object.basic_game_information.points - 5 >= 40:
                action = self.mockAction(DeployVaccine.DeployVaccine())
                if action == None or action["type"] == "endRound":
                    return {"points": -1}
                points = 0
                city = self.game_object.basic_game_information.cities[action["city"]]
                points = city["population"] / 5  # RANDOM FAKTOR; SOLLTE ANGEPASST WERDEN
                current_population = self.calculateCurrentPopulation()
                points_relative_to_population = points/current_population * 100
                # print(str(points_relative_to_population*5) + "% of Population vaccinated (If Vaccination)")
                r = randrange(1, 100)
                if points_relative_to_population > 0.1 and (r > 15 or self.calculateCurrentPopulation()/756371 < 0.6):
                    return {"points": points_relative_to_population, "action": action}
                else:
                    return {"points": 0.05, "action": {"type": "endRound"}}
            return {"points": -1}
        else:
            return {"points": -1}
        
    def shouldDeployMedication(self):
        if len(self.game_object.extracted_game_information.pathogens_with_medication_available) > 0 and self.game_object.basic_game_information.points >= 10:
            if self.game_object.basic_game_information.round <= 20 or self.game_object.basic_game_information.round > 20 and self.game_object.basic_game_information.points - 10 >= 40:
                action = self.mockAction(DeployMedication.DeployMedication())
                if action == None or action["type"] == "endRound":
                    return {"points": -1}
                points = 0
                for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
                    if pathogen_with_cities["name"] == action["pathogen"]:
                        city = self.game_object.basic_game_information.cities[action["city"]]
                        for event in city["events"]:
                            if event["type"] == "outbreak":
                                points = int(city["population"]*event["prevalence"]*0.4)
                current_population = self.calculateCurrentPopulation()
                points_relative_to_population = points/current_population * 100
                # print(str(points_relative_to_population) + "% of Population saved (If Medication)")
                if points_relative_to_population > 0.02:
                    return {"points": points_relative_to_population, "action": action}
                else:
                    return {"points": -1}
            else:
                return {"points": -1}
        else:
            return {"points": -1}
    
    def mockAction(self, action):
        strategy = Strategy.Strategy()
        action = strategy.fill_action(self.game_object, action)
        return action


    def calculateCurrentPopulation(self):
        result = 0
        for city_name in self.game_object.basic_game_information.cities:
            result += self.game_object.basic_game_information.cities[city_name]["population"]
        return result

    def calculateDeathsWhileDoingNothing(self):
        # Lukas tolle Funktion hier bitte
        pass

    def calculateDeathsWhileDoingMedication(self):
        totalLifesSafed = 0
        for pathogen_with_medication_available in self.game_object.extracted_game_information.pathogens_with_medication_available:
            for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
                if pathogen_with_medication_available == pathogen_with_cities["name"]:
                    for city_name in pathogen_with_cities["infectedCities"]:
                        city = self.game_object.basic_game_information.cities[city_name]
                        totalLifesSafed += int(city["population"]*0.4)
        return self.calculateCurrentPopulation - totalLifesSafed

    def calcaulateDeathsWhileDoingVaccine(self):
        pass
        


        