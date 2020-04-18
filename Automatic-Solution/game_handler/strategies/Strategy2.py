from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import SavePoints, DeployMedication
from game_handler.strategies import Strategy


class Strategy2(Strategy.Strategy):

    def __init__(self):
        self.description = {"name": "Shut Down", "desc": "Shut down best pathogen -> hope for others to spread"}


    def implement(self, game_object: GameObject):
        # ROUND 1: QUARANTINE
        if game_object.basic_game_information.round == 1 and game_object.basic_game_information.points >= 30:
            return self.shutdown_pathogen(game_object)
        elif game_object.basic_game_information.round == 1 and game_object.basic_game_information.points < 30:
            selected_action = SavePoints.SavePoints()
            return self.fill_action(game_object, selected_action)
        # ROUND 2: MEDICATION Development
        elif game_object.basic_game_information.round > 1 and game_object.basic_game_information.points >= 20:
            all_pathogens = self.determine_best_pathogen_to_shutdown(game_object)
            all_pathogens.pop(0)
            for pathogen in all_pathogens:
                if not(pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_in_development or pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_available):
                    return  {"type": "developMedication", "pathogen": pathogen["name"]} 
        elif game_object.basic_game_information.round > 1 and game_object.basic_game_information.points < 20 and not self.shouldDeployMedication(game_object):
            selected_action = SavePoints.SavePoints()
            return self.fill_action(game_object, selected_action)
        if game_object.basic_game_information.points >= 10 and self.shouldDeployMedication(game_object):
            for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
                if len(pathogen_with_cities["infectedCities"]) < 3 and not len(pathogen_with_cities["infectedCities"]) == 0:
                    city_name = pathogen_with_cities["infectedCities"][0]
                    city = game_object.basic_game_information.cities[city_name]
                    if "events" in city:
                        for event in city["events"]:
                            if event["type"] == "outbreak" and event["pathogen"]["name"] == pathogen_with_cities["name"] and pathogen_with_cities["name"] in game_object.extracted_game_information.pathogens_with_medication_available:
                                return {"type": "deployMedication", "pathogen": pathogen_with_cities["name"], "city": city_name}
            if game_object.basic_game_information.points >= 20 and len(self.determine_best_pathogen_to_shutdown(game_object)) == 1:
                if game_object.basic_game_information.points >= 20:
                    pathogen = self.determine_best_pathogen_to_shutdown(game_object)[0]
                    if not(pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_in_development or pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_available):
                        return  {"type": "developMedication", "pathogen": pathogen["name"]}
                    elif game_object.basic_game_information.points >= 35:
                        action = DeployMedication.DeployMedication()
                        return self.fill_action(game_object, action, strategy=2)

        return {"type": "endRound"}
            



    def shutdown_pathogen(self, game_object: GameObject):
        best_pathogens_to_select_with_cities = self.determine_best_pathogen_to_shutdown(game_object)
        best_pathogens_to_select_with_cities.pop(0)
        return {"type": "putUnderQuarantine", "city": best_pathogens_to_select_with_cities[0]["infectedCities"][0], "rounds": 2}

    def determine_best_pathogen_to_shutdown(self, game_object: GameObject):
        # Gewichtung?
        pathogens_with_cities = game_object.extracted_game_information.pathogen_with_cities
        for pathogen in pathogens_with_cities:
            if len(pathogen["infectedCities"]) == 0:
                pathogens_with_cities.remove(pathogen)
        
        pathogens_with_cities = sorted(pathogens_with_cities, reverse=True, key=lambda pathogen: (pathogen["mobility"], pathogen["lethality"], pathogen["duration"], pathogen["infectivity"]))
        if len(pathogens_with_cities) > 1:
            pathogens_with_cities = self.sortIfSameMobility(pathogens_with_cities)
        return pathogens_with_cities


    def sortIfSameMobility(self, pathogens):
        tmpLethality = pathogens[1]["lethality"]
        tmpMobility = pathogens[1]["mobility"]
        tmpInfectivity = pathogens[1]["infectivity"]
        for pathogen in pathogens:
            if pathogen["mobility"] == tmpMobility:
                if pathogen["lethality"] > tmpLethality:
                    pathogens.remove(pathogen)
                    pathogens.insert(1, pathogen)
                    tmpLethality = pathogen["lethality"]
                if pathogen["lethality"] == tmpLethality:
                    if pathogen["infectivity"] < tmpInfectivity:
                        pathogens.remove(pathogen)
                        pathogens.insert(1, pathogen)
                        tmpInfectivity = pathogen["infectivity"]
        return pathogens

    def shouldDeployMedication(self, game_object: GameObject):
        if len(game_object.extracted_game_information.pathogen_with_cities) < 259:
            return True
        else:
            return False