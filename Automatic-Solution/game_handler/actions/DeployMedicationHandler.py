from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import DeployMedication, DeployVaccine, DevelopMedication, DevelopVaccine, EndRoundAction

class DeployMedicationHandler():
    action = {"type": "deployMedication"}
    game_object: GameObject

    def __init__(self, game_object: GameObject):
        self.game_object = game_object

    def handleStrategy(self, strategy):
        if strategy == 1:
            return self.defaultHandling()
        if strategy == 2:
            return self.defaultHandling()
        else:
            return self.defaultHandling()

        

    def defaultHandling(self):
        city_names = self.determineRelevantCities()
        if len(city_names)>0:
            for city_name in city_names:
                city = self.game_object.basic_game_information.cities[city_name]
                for event in city["events"]:
                    if self.checkIfCityInfectedAndMedicationAvailable(event):
                        self.buildAction(city, event["pathogen"]["name"])
                        #print("--------")
                        #print(event["prevalence"])
                        #print("--------")
                        #print("Saved through Medication: " + str(int(city["population"]*(event["prevalence"]/0.4))))
                        return self.action

        return {"type": "endRound"}

    def checkIfCityInfectedAndMedicationAvailable(self, event):
        return event["type"] == "outbreak" and event["pathogen"]["name"] in self.game_object.extracted_game_information.pathogens_with_medication_available

    def buildAction(self, city, pathogen):
        self.action["city"] = city["name"]
        self.action["pathogen"] = pathogen

    def determineRelevantCities(self):
        action_dependency_solver = ActionDependencySolver.ActionDependencySolver(self.game_object)
        best_cities_to_deploy_medication = action_dependency_solver.determineBestCitiesToDeployMedication()
        return best_cities_to_deploy_medication

    def calculateExpectedValue(self):
        city_names = self.determineRelevantCities()
        for city_name in city_names:
            city = self.game_object.basic_game_information.cities[city_name]
            for event in city["events"]:
                if self.checkIfCityInfectedAndMedicationAvailable(event):
                    return int(city["population"]*event["prevalence"]*0.4)
        return 0