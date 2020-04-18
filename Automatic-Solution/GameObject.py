class BasicGameInformation():
    round: int = None
    outcome: str = None
    points: int = None
    cities = None
    events = None
    def __init__(self, game_json):
        self.round = game_json["round"]
        self.outcome = game_json["outcome"]
        self.points = game_json["points"]
        self.cities = game_json["cities"]
        self.mapCityStateValuesToNumerical()
        self.events = game_json["events"]
    
    def mapCityStateValuesToNumerical(self):
        for city in self.cities:
            self.cities[city]["economy"] = self.stateValueToNumerical(self.cities[city]["economy"])
            self.cities[city]["government"] = self.stateValueToNumerical(self.cities[city]["government"])
            self.cities[city]["hygiene"] = self.stateValueToNumerical(self.cities[city]["hygiene"])
            self.cities[city]["awareness"] = self.stateValueToNumerical(self.cities[city]["awareness"])


    def stateValueToNumerical(self, state):
        switcher =  {
            '--': -2,
            '-': -1,
            'o': 0,
            '+': 1,
            '++': 2
        }
        return switcher.get(state, 0)

class ExtractedGameInformation():
    cities_with_events = None
    global_events = None
    pathogen_with_cities = None
    pathogen_vaccine_status = None
    pathogen_medication_status = None
    pathogens_with_medication_in_development = None
    pathogens_with_vaccination_in_development = None
    pathogens_with_medication_available = None
    pathogens_with_vaccination_available = None
    def setCitiesWithEvents(self, cities_with_events):
        self.cities_with_events = cities_with_events
    def setGlobalEvents(self, global_events):
        self.global_events = global_events
    def setPathogenWithCities(self, pathogen_with_cities):
        self.pathogen_with_cities = pathogen_with_cities
    def setPathogenVaccineStatus(self, pathogen_vaccine_status):
        self.pathogen_vaccine_status = pathogen_vaccine_status
    def setPathogenMedicationStatus(self, pathogen_medication_status):
        self.pathogen_medication_status = pathogen_medication_status
    
    def setPathogenWithMedicationInDevelopment(self, pathogens_with_medication_in_development):
        self.pathogens_with_medication_in_development = pathogens_with_medication_in_development
    def setPathogenWithVaccinationInDevelopment(self, pathogens_with_vaccination_in_development):
        self.pathogens_with_vaccination_in_development = pathogens_with_vaccination_in_development
    def setPathogenWithMedicationAvailable(self, pathogens_with_medication_available):
        self.pathogens_with_medication_available = pathogens_with_medication_available
    def setPathogenWithVaccinationAvailable(self, pathogens_with_vaccination_available):
        self.pathogens_with_vaccination_available = pathogens_with_vaccination_available

class GameObject():
    basic_game_information: BasicGameInformation = None
    extracted_game_information: ExtractedGameInformation = None

    def __init__(self, basic_game_information: BasicGameInformation, extracted_game_information: ExtractedGameInformation):
        self.basic_game_information = basic_game_information
        self.extracted_game_information = extracted_game_information