from GameObject import GameObject
from game_handler import ActionDependencySolver
from game_handler.actions import DeployMedicationHandler, DeployVaccineHandler, DevelopMedicationHandler, DevelopVaccineHandler
from models import ApplyHygienicMeasures, SavePoints
from random import randrange

class Strategy():

    description = ""

    def __init__(self):
        pass

    def getDescription(self):
        return self.description


    def determine_possible_actions(self, game_object: GameObject, actions_to_choose_from):
        actions_to_choose_from = actions_to_choose_from
        actions_to_remove = []
        for action in actions_to_choose_from:
            if (action.base_cost + action.cost_multiplier*1) > game_object.basic_game_information.points:
                actions_to_remove += [action]
        for action in actions_to_remove:
            actions_to_choose_from.remove(action) 
        return actions_to_choose_from

    def select_random_action(self, game_object):
        actions_to_choose_from = [ApplyHygienicMeasures.ApplyHygienicMeasures()] # CloseAirport.CloseAirport(), CloseConnection.CloseConnection(), CallElections.CallElections(), ExertInfluence.ExertInfluence(), LaunchCampaign.LaunchCampaign(), PutUnderQuarantine.PutUnderQuarantine(),  ApplyHygienicMeasures.ApplyHygienicMeasures(),  DeployVaccine.DeployVaccine(), DevelopVaccine.DevelopVaccine(), 
        actions_to_choose_from = self.determine_possible_actions(game_object, actions_to_choose_from)
        if len(actions_to_choose_from) >= 1:
            selected_action = actions_to_choose_from[randrange(len(actions_to_choose_from))]
            return selected_action
        else:
            return SavePoints.SavePoints()

    def fill_action(self, game_object: GameObject, selected_action, strategy = 0):
        action = {"type": "endRound"}
        action["type"] = selected_action.type
        if "city" in selected_action.dependencies:
            city_names = []
            for city_name in game_object.basic_game_information.cities:
                city_names.append(city_name)
            action["city"] = city_names[randrange(len(city_names))]
        if "rounds" in selected_action.dependencies:
            max_rounds = int((game_object.basic_game_information.points-selected_action.base_cost)/selected_action.cost_multiplier)
            if max_rounds == 1:
                action["rounds"] = 1
            elif max_rounds > 1:
                action["rounds"] = randrange(1, max_rounds)
            else:
                return self.fill_action(game_object, self.select_random_action(game_object))
        if action["type"] == "closeAirport":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToCloseAirport()
            found_city = action_dependency_solver.findViableCity(best_cities_to_select, "airportClosed")
            if found_city == None:
                self.select_random_action(game_object)
            else:
                action["city"] = found_city
        elif action["type"] == "putUnderQuarantine":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToPutUnderQuarantine()
            found_city = action_dependency_solver.findViableCity(best_cities_to_select, "quarantine")
            if found_city == None:
                return self.fill_action(game_object, self.select_random_action(game_object))
            else:
                action["city"] = found_city
        elif action["type"] == "exertInfluence":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToExertInfluence()
            action["city"] = best_cities_to_select.pop()
        elif action["type"] == "callElections":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToCallElections()
            action["city"] = best_cities_to_select.pop()
        elif action["type"] == "applyHygienicMeasures":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToApplyHygienicMeasures()
            if len(best_cities_to_select) > 0:
                action["city"] = best_cities_to_select.pop()
            else:
                return {"type": "endRound"} #self.fill_action(game_object, self.select_random_action(game_object))
        elif action["type"] == "launchCampaign":
            action_dependency_solver = ActionDependencySolver.ActionDependencySolver(game_object)
            best_cities_to_select = action_dependency_solver.determineBestCitiesToLaunchCampaign()
            action["city"] = best_cities_to_select.pop()
        elif action["type"] == "developMedication":
            handler = DevelopMedicationHandler.DevelopMedicationHandler(game_object)
            return handler.handleStrategy(strategy)
        elif action["type"] == "developVaccine":
            handler = DevelopVaccineHandler.DevelopVaccineHandler(game_object)
            return handler.handleStrategy(strategy)
        elif action["type"] == "deployVaccine":
            handler = DeployVaccineHandler.DeployVaccineHandler(game_object)
            return handler.handleStrategy(strategy)
        elif action["type"] == "deployMedication":
            handler = DeployMedicationHandler.DeployMedicationHandler(game_object)
            return handler.handleStrategy(strategy)
            
        return action