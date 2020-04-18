from GameObject import GameObject
from models import *
from game_handler import ActionDependencySolver
from game_handler.strategies import Strategy1, Strategy11, Strategy2, Strategy3, Strategy4

class ProceduralGameHandler():
    actions = [EndRoundAction.EndRoundAction(), SavePoints.SavePoints(), ApplyHygienicMeasures.ApplyHygienicMeasures(), CallElections.CallElections(), CloseAirport.CloseAirport(), CloseConnection.CloseConnection(), DeployMedication.DeployMedication(), DeployVaccine.DeployVaccine(), DevelopMedication.DevelopMedication(), DevelopVaccine.DevelopVaccine(), ExertInfluence.ExertInfluence(), LaunchCampaign.LaunchCampaign(), PutUnderQuarantine.PutUnderQuarantine()]
    strategy = {}
    def __init__(self):
        pass

    def evaluateGameAndSelectAction(self, game_object: GameObject):
        global strategy
        #strategy = Strategy2.Strategy2()
        #return strategy.implement(game_object)
        action = self.chooseStrategy(game_object)
        action["strategy"] = strategy.description
        return action



    def chooseStrategy(self, game_object: GameObject):#
        global strategy
        infectedCities = 0
        for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
            infectedCities += len(pathogen_with_cities["infectedCities"])
        if infectedCities < 259:
            if self.checkIfStrategie4IsViable(game_object):
                strategy = Strategy4.Strategy4()
                return strategy.implement(game_object)
            if self.checkIfStrategie3IsViable(game_object):
                strategy = Strategy3.Strategy3()
                return strategy.implement(game_object)
            # Priority 1: Shutdown new Pathogen
            if(game_object.basic_game_information.round != 1):
                if self.checkIfStrategie11IsViable(game_object):
                    strategy = Strategy11.Strategy11()
                    return strategy.implement(game_object, game_object.extracted_game_information.pathogen_with_cities)
                if self.checkIfStrategie2IsViable(game_object):
                    strategy = Strategy2.Strategy2()
                    return strategy.implement(game_object)                
            if game_object.basic_game_information.round == 1:
                if self.checkIfStrategie2IsViable(game_object):
                    strategy = Strategy2.Strategy2()
                    return strategy.implement(game_object)


        if self.checkIfStrategie3IsViable(game_object):
            strategy = Strategy3.Strategy3()
            return strategy.implement(game_object)
        if self.checkIfStrategie2IsViable(game_object):
            strategy = Strategy2.Strategy2()
            return strategy.implement(game_object)
        
        strategy = Strategy1.Strategy1()
        return strategy.implement(game_object)


    def checkIfStrategie4IsViable(self, game_object: GameObject):
        if len(game_object.extracted_game_information.pathogen_with_cities) > 1:
            for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
                if pathogen_with_cities["name"] == "Admiral Trips":
                    if len(pathogen_with_cities["infectedCities"]) == 1:
                        return True
        return False

    def checkIfStrategie2IsViable(self, game_object: GameObject):
        pathogens = self.evaluatePathogens(game_object)
        if len(pathogens) > 1:
            for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
                if len(pathogen_with_cities["infectedCities"]) == 1:
                    for pathogen in pathogens:
                        if pathogen["pathogen"]["mobility"] > 0 or pathogen["pathogen"]["mobility"] == 0 or pathogen["pathogen"]["lethality"] == 2:
                            return True
        return False

    def checkIfStrategie11IsViable(self, game_object: GameObject):
        if not game_object.basic_game_information.round == 1:
            for pathogen_with_cities in game_object.extracted_game_information.pathogen_with_cities:
                if len(pathogen_with_cities["infectedCities"]) == 1:
                    for global_event in game_object.extracted_game_information.global_events:
                        if global_event["type"] == "pathogenEncountered":
                            if global_event["pathogen"]["name"] == pathogen_with_cities["name"]:
                                if global_event["round"] == game_object.basic_game_information.round:
                                    return True
                                    # if this is true for different pathogens, further evaluation is necessary
                                    # city = game_object.basic_game_information.cities[pathogen_with_cities["name"]]
                                    # if "events" in city:
                                    #     for event in city["events"]:                        
                                    #         if (event["type"] == "outbreak") or event["type"] == "bioterrorism"):
                                    #             return True
        return False

    def checkIfStrategie3IsViable(self, game_object: GameObject):
        if len(game_object.extracted_game_information.pathogen_with_cities) == 1:
            for pathogen_with_city in game_object.extracted_game_information.pathogen_with_cities:
                # Safe City with most Population
                if pathogen_with_city["name"] == "Admiral Trips" and len(pathogen_with_city["infectedCities"]) > 0:
                    for global_event in game_object.extracted_game_information.global_events:
                        if global_event["type"] == "pathogenEncountered":
                            if global_event["round"] < 5:
                                if game_object.basic_game_information.round < 5:
                                    return True
        return False


    def evaluatePathogens(self, game_object: GameObject):
        events = []
        for event in game_object.extracted_game_information.global_events:
            if event["type"] == "pathogenEncountered":
                events.append(event)
        # Sort Events ordered by lethality > mobility > infectivity > duration
        pathogens_ordered = sorted(events, reverse=True, key=lambda pathogen: (pathogen["pathogen"]["mobility"], pathogen["pathogen"]["lethality"], pathogen["pathogen"]["infectivity"], pathogen["pathogen"]["duration"]))
        if len(pathogens_ordered) > 1:
            pathogens_ordered = self.sortIfSameMobility(pathogens_ordered)
        return pathogens_ordered

    def sortIfSameMobility(self, pathogens):
        tmpLethality = pathogens[1]["pathogen"]["lethality"]
        tmpMobility = pathogens[1]["pathogen"]["mobility"]
        tmpInfectivity = pathogens[1]["pathogen"]["infectivity"]
        for pathogen in pathogens:
            if pathogen["pathogen"]["mobility"] == tmpMobility:
                if pathogen["pathogen"]["lethality"] > tmpLethality:
                    pathogens.remove(pathogen)
                    pathogens.insert(1, pathogen)
                    tmpLethality = pathogen["pathogen"]["lethality"]
                if pathogen["pathogen"]["lethality"] == tmpLethality:
                    if pathogen["pathogen"]["infectivity"] < tmpInfectivity:
                        pathogens.remove(pathogen)
                        pathogens.insert(1, pathogen)
                        tmpInfectivity = pathogen["pathogen"]["infectivity"]
        return pathogens

            



    