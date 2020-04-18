from GameObject import GameObject
from game_handler import ActionDependencySolver

class DeployVaccineHandler():
    action = {"type": "deployVaccine"}
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
        pathogens = self.determineRelevantPathogens()
        cities = self.determineRelevantCities()
        if self.game_object.basic_game_information.points >= 35:
            for city_name in cities:
                city = self.game_object.basic_game_information.cities[city_name]

                for pathogen in pathogens:
                    if self.checkIfCityIsViable(city, pathogen):
                        self.buildAction(city, pathogen)
                        #print("Possibly saved through Vaccination: " + str(city["population"]))
                        return self.action
        return {"type": "endRound"}

    def determineRelevantPathogens(self):
        action_dependency_solver = ActionDependencySolver.ActionDependencySolver(self.game_object)
        pathogens = action_dependency_solver.determineBestPathogenForDeployment()
        possible_pathogens = self.removePathogensWithoutVaccine(pathogens)
        return possible_pathogens
    
    def determineRelevantCities(self):
        action_dependency_solver = ActionDependencySolver.ActionDependencySolver(self.game_object)
        best_cities_to_deploy_vaccine = action_dependency_solver.determineBestCitiesToDeployVaccine()
        return best_cities_to_deploy_vaccine


    def buildAction(self, city, pathogen):
        self.action["city"] = city["name"]
        self.action["pathogen"] = pathogen

    def checkIfCityIsViable(self, city, pathogen):
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            if pathogen_with_cities["name"] == pathogen and len(pathogen_with_cities["infectedCities"]) == 0:
                return False
        if "events" in city:
            same_pathogen_active = False
            vaccineDeployed = False
            was_already_infected_by_that_pathogen = False
            for event in city["events"]:
                if event["type"] == "outbreak" and event["pathogen"]["name"] == pathogen:
                    same_pathogen_active = True
                if event["type"] == "vaccineDeployed" and event["pathogen"]["name"] == pathogen:
                    vaccineDeployed = True
                if event["type"] == "medicationDeployed" and  event["pathogen"]["name"] == pathogen:
                    was_already_infected_by_that_pathogen = True
            return not vaccineDeployed and not same_pathogen_active and not was_already_infected_by_that_pathogen
        else:
            return True

    def removePathogensWithoutVaccine(self, pathogens):
        pathogens_to_remove = []
        for pathogen in pathogens:
            if pathogen not in self.game_object.extracted_game_information.pathogens_with_vaccination_available:
                pathogens_to_remove += [pathogen]
        for pathogen in pathogens_to_remove:
            pathogens.remove(pathogen)
        return pathogens

    def calculateExpectedValue(self):
        pathogens = self.determineRelevantPathogens()
        cities = self.determineRelevantCities()
        for city_name in cities:
            city = self.game_object.basic_game_information.cities[city_name]
            for pathogen in pathogens:
                if self.checkIfCityIsViable(city, pathogen):
                    return int(city["population"])
        return 0