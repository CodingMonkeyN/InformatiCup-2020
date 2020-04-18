from GameObject import GameObject
from game_handler import ActionDependencySolver

class DevelopVaccineHandler():

    action = {"type": "developVaccine"}
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
        action_dependency_solver = ActionDependencySolver.ActionDependencySolver(self.game_object)
        pathogens = action_dependency_solver.determineBestPathogenToDevelopVaccineFor()
        if(len(pathogens)>0):
            for pathogen in pathogens:
                if self.checkIfPathogenIsViable(pathogen):
                    self.buildAction(pathogen)
                    return self.action
        return {"type": "endRound"}
    
    def checkIfPathogenIsViable(self, pathogen):
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            if pathogen_with_cities["name"] == pathogen and pathogen_with_cities["infectedCities"] == 0:
                return False
        return pathogen not in self.game_object.extracted_game_information.pathogens_with_vaccination_in_development and not pathogen in self.game_object.extracted_game_information.pathogens_with_vaccination_available

    def buildAction(self, pathogen):
        self.action["pathogen"] = pathogen