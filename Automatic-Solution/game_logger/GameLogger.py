from GameObject import GameObject
import json
import xlsxwriter
import os.path
from os import path

class GameLogger():
    game_object = None

    def __init__(self, game_object: GameObject):
        self.game_object = game_object

    def logGameState(self):
        if self.game_object.basic_game_information.round < 100:
            name = str(self.game_object.basic_game_information.round)
            for pathogen in self.game_object.extracted_game_information.pathogen_with_cities:
                name += pathogen["name"][:2]
            if not path.exists("./logs/" + name + ".xlsx"):
                if self.game_object.basic_game_information.round == 1:
                    f=open("./logs/all_logged_games.txt", "a+")
                    f.write(name[1:] + "\n")
                workbook = xlsxwriter.Workbook("./logs/" + name + ".xlsx")
                worksheet = workbook.add_worksheet()

                # worksheet.write('A1', "round")
                # worksheet.write('A2', self.game_object.basic_game_information.round)
                
                # worksheet.write('B1', "amount of pathogens")
                # worksheet.write('B2', len(self.game_object.extracted_game_information.pathogen_with_cities))
                
                #worksheet.write('C1', "infested cities")
                infected_cities = 0
                for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
                    infected_cities += len(pathogen_with_cities["infectedCities"])
                current_population = 0
                for city in self.game_object.basic_game_information.cities:
                    current_population += self.game_object.basic_game_information.cities[city]["population"]
                data = [
                    ['round', self.game_object.basic_game_information.round],
                    ['amount of pathogens', len(self.game_object.extracted_game_information.pathogen_with_cities)],
    	            ['infected cities', infected_cities],
                    ['current population', current_population/3025]
                ]

                for pathogen_with_cities in self.game_object.extracted_game_information.pathogen_with_cities:
                    data += [["D: " + str(pathogen_with_cities["duration"]) + "  " +"I: " + str(pathogen_with_cities["infectivity"]) + "  " + "L: " + str(pathogen_with_cities["lethality"]) + "   " + "M: " + str(pathogen_with_cities["mobility"]) + "  " + pathogen_with_cities["name"], len(pathogen_with_cities["infectedCities"])]]
                
                column = 0
                row = 0

                for array in data:
                    row = 0
                    for value in array:
                        worksheet.write(row, column, value)
                        row += 1
                    column += 1
                worksheet.write('C2', infected_cities)
                workbook.close()

