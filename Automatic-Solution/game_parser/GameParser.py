from GameObject import GameObject, BasicGameInformation, ExtractedGameInformation
import json
import copy
class GameParser():
    def __init__(self):
        pass

    def build_game_object(self, game_json):
        basic_game_information = BasicGameInformation(game_json)
        extracted_game_information = ExtractedGameInformation()
        self.fill(extracted_game_information, game_json)
        game_object = GameObject(basic_game_information, extracted_game_information)
        return game_object

    def fill(self, extracted_game_information, game_json):
        extracted_game_information.setCitiesWithEvents(self.extractCitiesWithEvents(game_json))
        extracted_game_information.setGlobalEvents(self.extractGlobalEvents(game_json))
        extracted_game_information.setPathogenWithCities(self.extractPathogenWithCities(game_json))
        extracted_game_information.setPathogenVaccineStatus(self.extractPathogenVaccineStatus(game_json))
        extracted_game_information.setPathogenMedicationStatus(self.extractPathogenMedicationStatus(game_json))
        extracted_game_information.setPathogenWithMedicationInDevelopment(self.extractPathogensWithMedicationInDevelopment(game_json))
        extracted_game_information.setPathogenWithVaccinationInDevelopment(self.extractPathogensWithVaccinationInDevelopment(game_json))
        extracted_game_information.setPathogenWithMedicationAvailable(self.extractPathogensWithMedicationAvailable(game_json))
        extracted_game_information.setPathogenWithVaccinationAvailable(self.extractPathogensWithVaccinationAvailable(game_json))

    def extractCitiesWithEvents(self, game_json):
        cities_with_events = []
        for city in game_json["cities"]:
            if("events" in game_json["cities"][city] and len(game_json["cities"][city]["events"]) > 0):
               cities_with_events.append({"name":city,"events":game_json["cities"][city]["events"]})#game_json["cities"][city])
        return cities_with_events

    def extractPathogenVaccineStatus(self, game_json):
        pathogen_vaccine_status = {"NoVaccine":[],"VaccineInDevelopment":[],"VaccineAvailable":[]}
        for events in game_json["events"]:
            if(events["type"]=="vaccineAvailable"):
                temp = copy.deepcopy(events["pathogen"].get("name"))
                pathogen_vaccine_status["VaccineAvailable"].append(temp)
            else:
                if(events["type"]=="vaccineInDevelopment"):
                    temp = copy.deepcopy(events["pathogen"].get("name"))
                    pathogen_vaccine_status["VaccineInDevelopment"].append(temp) 
        for events in game_json["events"]:
            if(events["type"]=="pathogenEncountered"):
                temp = copy.deepcopy(events["pathogen"].get("name"))
                if(temp not in pathogen_vaccine_status["VaccineInDevelopment"] and temp not in pathogen_vaccine_status["VaccineAvailable"]):
                    pathogen_vaccine_status["NoVaccine"].append(temp)
        return pathogen_vaccine_status
    
    def extractPathogenMedicationStatus(self, game_json):
        pathogen_medication_status = {"NoMedication":[],"MedicationInDevelopment":[],"MedicationAvailable":[]}
        for events in game_json["events"]:
            if(events["type"]=="medicationAvailable"):
                temp = copy.deepcopy(events["pathogen"].get("name"))
                pathogen_medication_status["MedicationAvailable"].append(temp)
            else:
                if(events["type"]=="medicationInDevelopment"):
                    temp = copy.deepcopy(events["pathogen"].get("name"))
                    pathogen_medication_status["MedicationInDevelopment"].append(temp) 
        for events in game_json["events"]:
            if(events["type"]=="pathogenEncountered"):
                temp = copy.deepcopy(events["pathogen"].get("name"))
                if(temp not in pathogen_medication_status["MedicationInDevelopment"] and temp not in pathogen_medication_status["MedicationAvailable"]):
                    pathogen_medication_status["NoMedication"].append(temp)
        return pathogen_medication_status

    def extractPathogenWithCities(self, game_json):
        pathogen_with_cities = []
        for events in game_json["events"]:
            if(events["type"]=="pathogenEncountered"):
                temp = copy.deepcopy(events["pathogen"])
                pathogen_with_cities.append(temp)
        for pathogen in pathogen_with_cities:
            pathogen["infectedCities"] = []
        for city in game_json["cities"]:
            if("events" in game_json["cities"][city] and len(game_json["cities"][city]["events"]) > 0):
                for event in game_json["cities"][city]["events"]:    
                    if(event.get("type") == "outbreak" or event.get("type") == "bioTerrorism"):
                        for pathogen in pathogen_with_cities:
                            if(pathogen.get("name") == event["pathogen"].get("name")):
                                pathogen["infectedCities"].append(city)
        for pathogen in pathogen_with_cities:
            pathogen["infectedCities"] = list(dict.fromkeys(pathogen["infectedCities"]))
        result = []
        for pathogen in pathogen_with_cities:
            if len(pathogen["infectedCities"]) > 0:
                result += [pathogen]
        '''
        for pathogen in pathogen_with_cities:
            pathogen["mobility"] = self.stateValueToNumerical(pathogen["mobility"])
            pathogen["duration"] = self.stateValueToNumerical(pathogen["duration"])
            pathogen["lethality"] = self.stateValueToNumerical(pathogen["lethality"])
            pathogen["infectivity"] = self.stateValueToNumerical(pathogen["infectivity"])
        '''
        return result

    def extractGlobalEvents(self, game_json):
        global_events = []
        #global_pathogen_events = []
        #global_non_pathogen_events = []
        #global_pathogen_event_types = ["pathogenEncountered"]
        for events in game_json["events"]:
            if events["type"] == "pathogenEncountered":
                events["pathogen"]["mobility"] = self.stateValueToNumerical(events["pathogen"]["mobility"])
                events["pathogen"]["duration"] = self.stateValueToNumerical(events["pathogen"]["duration"])
                events["pathogen"]["lethality"] = self.stateValueToNumerical(events["pathogen"]["lethality"])
                events["pathogen"]["infectivity"] = self.stateValueToNumerical(events["pathogen"]["infectivity"])
            #if(events["type"] in global_pathogen_event_types):# and len(game_json["events"][events]["events"]) > 0):
            global_events.append(events)
            #else:
                #global_non_pathogen_events.append(events)
        #global_events.append(global_pathogen_events)
        #global_events.append(global_non_pathogen_events)
        return global_events

    def extractPathogensWithMedicationInDevelopment(self, game_json):
        pathogens_with_medication_in_development = []
        for event in game_json["events"]:
            if(event["type"] == "medicationInDevelopment"):
                pathogens_with_medication_in_development += [event["pathogen"]["name"]]
        return pathogens_with_medication_in_development

    def extractPathogensWithVaccinationInDevelopment(self, game_json):
        pathogens_with_vaccination_in_development = []
        for event in game_json["events"]:
            if(event["type"] == "vaccineInDevelopment"):
                pathogens_with_vaccination_in_development += [event["pathogen"]["name"]]
        return pathogens_with_vaccination_in_development


    def extractPathogensWithMedicationAvailable(self, game_json):
        pathogens_with_medication_available = []
        for event in game_json["events"]:
            if(event["type"] == "medicationAvailable"):
                pathogens_with_medication_available += [event["pathogen"]["name"]]
        return pathogens_with_medication_available   

    def extractPathogensWithVaccinationAvailable(self, game_json):
        pathogens_with_vaccination_available = []
        for event in game_json["events"]:
            if(event["type"] == "vaccineAvailable"):
                pathogens_with_vaccination_available += [event["pathogen"]["name"]]
        return pathogens_with_vaccination_available   

    def build_json_from_object(self, game_object: GameObject):
        res_json = {}
        res_json["basic_game_information"] = game_object.basic_game_information.__dict__
        res_json["extracted_game_information"] = game_object.extracted_game_information.__dict__
        return res_json


    def stateValueToNumerical(self, state):
        switcher =  {
            '--': -2,
            '-': -1,
            'o': 0,
            '+': 1,
            '++': 2
        }
        return switcher.get(state, 0)
