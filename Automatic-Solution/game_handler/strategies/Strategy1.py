from GameObject import GameObject
from game_handler import ActionDependencySolver
from models import SavePoints, DevelopMedication, DevelopVaccine
from game_handler.strategies import Strategy, Foreseer
from random import randrange

class Strategy1(Strategy.Strategy):
    

    def __init__(self):
        self.description = {"name": "Medi/Vacc", "desc": "Trying to develop medication and vaccination for the most severe pathogens and deploy them to the cities with highest populations"}


    def implement(self, game_object: GameObject, min_lethality = 0):
        # Check Recursion Basis
        if min_lethality < -3:
            return {"type": "endRound"}

        medication_can_be_developed = self.checkIfMedicationCanBeDeveloped(game_object, min_lethality)
        vaccine_can_be_developed = self.checkIfVaccineCanBeDeveloped(game_object, min_lethality)

        # Priority 1: Develop Vaccine
        if vaccine_can_be_developed == True: 
            return self.developVaccine(game_object)
        # Priority 2: Develop Medication
        elif medication_can_be_developed == True:
            return self.developMedication(game_object)
        else:
            # Priority 3: Select other useful action
            action = Foreseer.Foreseer(game_object).selectAction(game_object)
            if not action == None:
                return action
            elif (len(game_object.extracted_game_information.pathogens_with_vaccination_available) != 0 and len(game_object.extracted_game_information.pathogens_with_medication_available) != 0):
                return self.implement(game_object, min_lethality-1)
            else:
                return self.fill_action(game_object, SavePoints.SavePoints()) 

    

    def developVaccine(self, game_object: GameObject):
        if game_object.basic_game_information.points >= 40:
            selected_action = DevelopVaccine.DevelopVaccine()
            return self.fill_action(game_object, selected_action)
        else:
            selected_action = SavePoints.SavePoints()
            return self.fill_action(game_object, selected_action) 

    def developMedication(self, game_object: GameObject):
        if game_object.basic_game_information.points >= 20:
            selected_action = DevelopMedication.DevelopMedication()
            return self.fill_action(game_object, selected_action)
        else:
            selected_action = SavePoints.SavePoints()
            return self.fill_action(game_object, selected_action)

    def checkIfMedicationCanBeDeveloped(self, game_object: GameObject, min_lethality):
        for pathogen in game_object.extracted_game_information.pathogen_with_cities:
            if pathogen["lethality"] > min_lethality and len(pathogen["infectedCities"]) > 0:
                if not(pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_in_development or pathogen["name"] in game_object.extracted_game_information.pathogens_with_medication_available):
                    return True
        return False

    def checkIfVaccineCanBeDeveloped(self, game_object: GameObject, min_lethality):
        for pathogen in game_object.extracted_game_information.pathogen_with_cities:
            if pathogen["lethality"] > min_lethality and len(pathogen["infectedCities"]) > 0:
                if not(pathogen["name"] in game_object.extracted_game_information.pathogens_with_vaccination_in_development or pathogen["name"] in game_object.extracted_game_information.pathogens_with_vaccination_available):
                    return True
        return False