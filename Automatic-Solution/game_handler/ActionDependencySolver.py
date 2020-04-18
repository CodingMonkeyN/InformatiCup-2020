from GameObject import GameObject

class ActionDependencySolver():
    game_object: GameObject = None

    peakRounds = {
        "Admiral Trips": 0,
        "Azmodeus": 3,
        "Coccus innocuus": 4,
        "Endoictus": 6,
        "Hexapox": 4,
        "Influenza iutiubensis": 0,
        "Methanobrevibacter colferi": 0,
        "Moricillus ☠": 1,
        "N5-10": 2,
        "Neurodermantotitis": 5,
        "Phagum vidiianum": 8,
        "Plorps": 6,
        "Procrastinalgia": 13,
        "Rhinonitis": 1,
        "Saccharomyces cerevisiae mutans": 2,
        "Shanty": 3,
        "Xenomonocythemia": 2,
        "Φthisis": 5
    }

    def __init__(self, game_object: GameObject):
        self.game_object = game_object

    def determineBestCitiesToPutUnderQuarantine(self):
        infected_cities = []
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            infected_cities += pathogen_with_cities["infectedCities"]
        # could be further sorted here (cities that are longer infected, cities that have more connections, etc.)
        return infected_cities

    def determineBestCitiesToCloseAirport(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city_evaluation_object = CityEvaluationObject(city_name)
            for connection in all_cities[city_name]["connections"]:
                for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
                    if connection in pathogen_with_cities["infectedCities"]:
                        city_evaluation_object.addToSignificance(1)
            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities
    
    def determineBestConnectionsToClose(self):
        pass

    def determineBestCitiesToDeployMedication(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            for city_name in pathogen_with_cities["infectedCities"]:
                city = all_cities[city_name]
                city_evaluation_object = CityEvaluationObject(city_name)
                for event in all_cities[city_name]["events"]:
                    if event["type"] == "outbreak": #  and pathogen_with_cities["lethality"] > 0
                        if self.game_object.basic_game_information.points >= 35:
                            city_evaluation_object.addToSignificance(((pathogen_with_cities["lethality"]+3)**2).real*event["prevalence"]*(city["population"]**1.25).real)
                            city_evaluation_objects.append(city_evaluation_object)
                        elif self.checkIfCityAtPeak(city, event):
                            # print(city_name +" at peak: " + str(event["prevalence"]))
                            city_evaluation_object.addToSignificance(((pathogen_with_cities["lethality"]+3)**2).real*event["prevalence"]*(city["population"]**1.25).real)
                            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, reverse=True, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities

    def checkIfCityAtPeak(self, city, outbreak_event):
        if outbreak_event["pathogen"]["name"] in self.peakRounds:
            return self.game_object.basic_game_information.round - outbreak_event["sinceRound"] == self.peakRounds[outbreak_event["pathogen"]["name"]]+1
        else:
            return True

    def determineBestCitiesToDeployVaccine(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city = all_cities[city_name]
            city_evaluation_object = CityEvaluationObject(city["name"])
            '''
            for event in all_cities[city_name]["events"]:
            
                if event["type"] == "outbreak":                        
                    if: # nimmt zu
                        city_evaluation_object.addToSignificance(city["population"] - city["population"] * (x * event["lethality"])) # was genau bedeutet leth4ality?
                    else: # nimmt ab
                        city_evaluation_object.addToSignificance(city["population"] - city["population"] * event["prevalence"] * (x * event["lethality"])) # was genau bedeutet lethality?
                else:
                    city_evaluation_object.addToSignificance(city["population"])
            '''
            city_evaluation_object.addToSignificance(city["population"])
            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, reverse=True, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities

    def determineBestPathogenToDevelopMedicationFor(self):
        pathogen_evaluation_objects = []
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            pathogen_evaluation_object = PathogenEvaluationObject(pathogen_with_cities["name"])
            # Infectivity, Duration, etc. relevant?
            # if pathogen_with_cities["lethality"] > 0
            if len(pathogen_with_cities["infectedCities"]) > 0:
                pathogen_evaluation_object.addToSignificance(pathogen_with_cities["lethality"]) # len(pathogen_with_cities["infectedCities"])
                pathogen_evaluation_objects.append(pathogen_evaluation_object)
        pathogen_evaluation_objects = sorted(pathogen_evaluation_objects, reverse=True, key=lambda pathogen_evaluation_object: pathogen_evaluation_object.significance)
        determined_pathogens = []
        for pathogen_evaluation_object in pathogen_evaluation_objects:
            determined_pathogens.append(pathogen_evaluation_object.name)
        return determined_pathogens

    def determineBestPathogenToDevelopVaccineFor(self):
        pathogen_evaluation_objects = []
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            pathogen_evaluation_object = PathogenEvaluationObject(pathogen_with_cities["name"])
            # Infectivity, Duration, etc. relevant?
            # if pathogen_with_cities["lethality"] > 0:
            if len(pathogen_with_cities["infectedCities"]) > 0 and pathogen_with_cities["duration"] > -2:
                pathogen_evaluation_object.addToSignificance(pathogen_with_cities["lethality"]) # len(pathogen_with_cities["infectedCities"])
                pathogen_evaluation_objects.append(pathogen_evaluation_object)
        pathogen_evaluation_objects = sorted(pathogen_evaluation_objects, reverse=True, key=lambda pathogen_evaluation_object: pathogen_evaluation_object.significance)
        determined_pathogens = []
        for pathogen_evaluation_object in pathogen_evaluation_objects:
            determined_pathogens.append(pathogen_evaluation_object.name)
        return determined_pathogens

    def determineBestPathogenForDeployment(self):
        pathogen_evaluation_objects = []
        for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
            pathogen_evaluation_object = PathogenEvaluationObject(pathogen_with_cities["name"])
            # Infectivity, Duration, etc. relevant?
            if not len(pathogen_with_cities["infectedCities"]) == 0: # pathogen_with_cities["lethality"] > 0 and 
                pathogen_evaluation_object.addToSignificance(pathogen_with_cities["lethality"]) # len(pathogen_with_cities["infectedCities"])
                pathogen_evaluation_objects.append(pathogen_evaluation_object)
        pathogen_evaluation_objects = sorted(pathogen_evaluation_objects, reverse=True, key=lambda pathogen_evaluation_object: pathogen_evaluation_object.significance)
        determined_pathogens = []
        for pathogen_evaluation_object in pathogen_evaluation_objects:
            determined_pathogens.append(pathogen_evaluation_object.name)
        return determined_pathogens

    def determineBestCitiesToExertInfluence(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city_evaluation_object = CityEvaluationObject(city_name)
            city_evaluation_object.addToSignificance(all_cities[city_name]["economy"])
            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities

    def determineBestCitiesToCallElections(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city_evaluation_object = CityEvaluationObject(city_name)
            city_evaluation_object.addToSignificance(all_cities[city_name]["government"])
            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities

    def determineBestCitiesToApplyHygienicMeasures(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city = self.game_object.basic_game_information.cities[city_name]
            if not (city["hygiene"] == 2 or city["hygiene"] == 1):
                if "events" in city:
                    for event in city["events"]:
                        if event["type"] == "outbreak":
                            city_evaluation_object = CityEvaluationObject(city_name)
                            city_evaluation_object.addToSignificance(((city["hygiene"]-0.5)**0.7).real*city["population"]*event["prevalence"])
                            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
            #result = self.game_object.basic_game_information.cities[city_evaluation_object.name]
            #print(str(result["hygiene"]) + "  " + str(result["population"]))
        return determined_cities

    def determineBestCitiesToLaunchCampaign(self):
        all_cities = self.game_object.basic_game_information.cities
        city_evaluation_objects = []
        for city_name in all_cities:
            city_evaluation_object = CityEvaluationObject(city_name)
            city_evaluation_object.addToSignificance(all_cities[city_name]["awareness"])
            city_evaluation_objects.append(city_evaluation_object)
        city_evaluation_objects = sorted(city_evaluation_objects, key=lambda city_evaluation_object: city_evaluation_object.significance)
        determined_cities = []
        for city_evaluation_object in city_evaluation_objects:
            determined_cities.append(city_evaluation_object.name)
        return determined_cities

    def findViableCity(self, city_array, event_to_check):
        city_found = False
        city = None
        while city_found == False and len(city_array)>0:
            city = city_array.pop()
            city_found = True # Lets assume, changes to False if not true
            if("events" in self.game_object.basic_game_information.cities[city]):
                for event in self.game_object.basic_game_information.cities[city]["events"]:
                    if event["type"] == event_to_check:
                        city_found = False
            else:
                city_found = True
        return city
            


class CityEvaluationObject():
    name: str
    significance: int

    def __init__(self, name: str):
        self.significance = 0
        self.name = name

    def addToSignificance(self, significanceChange: float):
        self.significance += significanceChange

    def getSignificance(self):
        return self.significance

class PathogenEvaluationObject():
    name: str
    significance: int

    def __init__(self, name: str):
        self.significance = 0
        self.name = name

    def addToSignificance(self, significanceChange: float):
        self.significance += significanceChange

    def getSignificance(self):
        return self.significance


def compareBySignificance(cev1: CityEvaluationObject, cev2: CityEvaluationObject):
    if cev1.getSignificance() < cev2.getSignificance():
        return -1
    elif cev1.getSignificance() > cev2.getSignificance():
        return 1
    else:
        return 0
