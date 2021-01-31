'''
convert.py written by Jimmy Zhong, Kyosuke Imai at Carleton College in CS Software Design under Prof Jeff Ondich 
converts an csv file called 'athlete_events.csv' into database-ready csv (with index included)
Produces 8 tables for database operation: 
athletes_table.csv; teams_table.csv; sport_categories_table.csv; detailed_events_table.csv
medals_table.csv; nocs_table.csv; olympic_games_table.csv; main_events_table.csv
'''
import csv 

class a_row:
	"""object that takes in every element in a row of given csv file"""
	def __init__(self, athe_ID, athe_name, sex, age, height, weight, team, noc,
	game, year, season, city, sport_category, detailed_event, medal):
		self.athe_ID = athe_ID
		self.athe_name = athe_name
		self.sex = sex
		self.age = age
		self.height = height
		self.weight = weight
		self.team = team
		self.noc = noc
		self.game = game
		self.year = year
		self.season = season
		self.city = city
		self.sport_category = sport_category
		self.detailed_event = detailed_event
		self.medal = medal

def create_one_map_one_table(all_rows, option): 
	""" returns a 2D array and dictionary of one_map_one style data, 
		given a list of row objects as a parameter applicable to 
		option 1: [team] : ID, country_team (United State)
		option 2: [sport_category] : ID, sport_category (swimming)
		option 3: [detailed_event] : ID, sport_event (swimming man 100m freestyle)
		option 4: [medal] : ID, Gold/Silver/Bronze/NA
	"""
	option_list = ["team", "noc", "sport_category", "detailed_event", "medal"]
	table = []
	dictionary = {}
	index = 1
	option = (option.strip()).lower()
	if option not in option_list:
		print("your option for one_map_one table is not valid!")
		return 
	for a_row in all_rows:
		str_data = str(getattr(a_row, option))
		if str_data not in dictionary:
			this_row = [index, str_data]
			table.append(this_row)
			dictionary[str_data] = index
			index = index + 1
	return table, dictionary

# noc_regions.csv
class noc: 
	def __init__(self, NOC, full_name = None, notes=None):
		self.NOC = NOC
		self.full_name = full_name
		self.notes = notes
	def __hash__(self):
		return hash(self.NOC)
	def __eq__(self, other):
		return self.NOC == other.NOC

def create_NOC_table(input_csv_file):
	noc_table = []
	noc_dict = {}
	index = 1
	with open(input_csv_file) as file:
		read_in_file = list((csv.reader(file, skipinitialspace=True)))
	read_in_file.append(['SGP', 'Singapore', 
	'Singapore is not in the noc_regions.csv, but it is in athlete_events.csv'])
	for row in read_in_file[1:]:
		if len(row) > 1:
			this_noc = noc(row[0], row[1], row[2])
			if this_noc.NOC not in noc_dict:
				noc_dict[this_noc] = index
				noc_table.append([index, this_noc.NOC, this_noc.full_name, this_noc.notes])
				index = index + 1

	return noc_table, noc_dict

class athlete:
	"""athlete object that takes in name and sex"""
	def __init__(self, name, sex):
		self.name = name
		self.sex = sex
	def __hash__(self):
		return hash(self.name)
	def __eq__(self, other):
		return self.name == other.name
def create_athlete_table(all_rows):
	"""returns a 2D array and dictionary of athelete ID, name and sex, with a list of row objects as a parameter  """
	athletes_table = []
	athletes_dict = {}
	for a_row in all_rows:
		an_athlete = athlete(a_row.athe_name, a_row.athe_ID)
		if an_athlete not in athletes_dict:
			this_row = [a_row.athe_ID, a_row.athe_name, a_row.sex]
			athletes_table.append(this_row)
			athletes_dict[an_athlete] = a_row.athe_ID
	return athletes_table, athletes_dict
		
class olympic_game:
	"""olympic game object that takes in year, season, and city of the given olympic game"""
	def __init__(self, year, season, city):
		self.year = year
		self.season = season
		self.city = city
	def __hash__(self):
		return hash((self.year, self.season))
	def __eq__(self, other):
		return (self.year, self.season) == (other.year, other.season)
def create_olympic_games_table(all_rows):
	"""returns 2D array and dictionary of olympic game ID, year, season, and the city held """
	olympic_games_table = []
	olympic_games_dict = {}
	index = 0
	for a_row in all_rows: 
		game = olympic_game(a_row.year, a_row.season, a_row.city) 
		if game not in olympic_games_dict:
			index = index + 1
			this_row = [index, a_row.year, a_row.season, a_row.city]
			olympic_games_table.append(this_row)
			olympic_games_dict[game] = index
	return olympic_games_table, olympic_games_dict

def create_main_events_table(athlete_dict, team_dict, noc_dict, olympic_games_dict, 
sport_category_dict, detailed_event_dict, medal_dict, all_rows):
	""" return main events table(that displays all the IDs accordingly) given the dictionary of 
		each of the elements in the table as a parameter.
		main table: event_ID (huge), athlete_ID, Age(unchanged), Height(unchanged), Weight (unchanged), 
		team_ID, country_table_ID, Olympics_game_ID, sport_category_ID, detailed_events_ID
	"""
	main_events_table = []
	index = 1
	for row_obj in all_rows:
		team_id = team_dict[row_obj.team]
		sport_category_id = sport_category_dict[row_obj.sport_category]
		detailed_event_id = detailed_event_dict[row_obj.detailed_event]
		medal_id = medal_dict[row_obj.medal]
		
		# make athlete object to find its id from the dictionary
		an_athlete = athlete(row_obj.athe_name, row_obj.sex)
		athlete_id = athlete_dict[an_athlete]

		an_oly_game = olympic_game(row_obj.year, row_obj.season, row_obj.city)
		oly_game_id = olympic_games_dict[an_oly_game]

		an_NOC = noc(row_obj.noc)
		noc_id = noc_dict[an_NOC]
	
		# athlete Age Height Weight remains as they are
		this_row = [index, athlete_id, row_obj.age, row_obj.height, row_obj.weight, 
		team_id, noc_id, oly_game_id, sport_category_id, detailed_event_id, medal_id]
		main_events_table.append(this_row)
		index = index + 1
	return main_events_table


def make_csv_row(this_row):
	if len(this_row) < 1:
		print("yooo! your row aint right!")
		return
	out_csv_row = str(this_row[0])
	for i in range(1, len(this_row)):
		csv_save_cell = str(this_row[i]).replace(",", "").replace('"', "(", 1)
		csv_save_cell = csv_save_cell.replace('"', ")")
		out_csv_row = out_csv_row + "," + csv_save_cell
	return (out_csv_row + '\n')	

def write_csv_table(table_list, file_name, header_list):
	"""print method to print the tables into a csv file given the table list, file name and the header of the individual columns """
	# example header_list ["ID", "country_three_letter", "full country_name"]
	num_col = len(table_list[0])
	if num_col != len(header_list):
		print("yooo! the number of cols between your list and header_list doesn't match!")
		return
	outfile = open(file_name, 'w')
	outfile.write(make_csv_row(header_list))
	# write database related tables to csv
	for row in table_list:
		outfile.write(make_csv_row(row))
	outfile.close()

def main():
	"""read-in source athlete_event.csv source, and create all the individual csv files for the database"""
	all_rows = []
	with open('athlete_events.csv') as file:
		read_in_file = list((csv.reader(file, skipinitialspace=True)))
	
	for row in read_in_file[1:]:
		if len(row) > 1:
			# read in athe_ID, athe_name, sex, age, height, weight, team, noc, 
			# game, year, season, city, sport_category, detailed_event, medal
			this_row = a_row(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
			row[8], row[9], row[10], row[11], row[12], row[13], row[14])
			all_rows.append(this_row)
	
	athlete_table, athlete_dict = create_athlete_table(all_rows)
	# header doesn't help the psql database, it's only for human(grader) readibility
	athlete_header =["athlete_ID", "athlete_name", "sex"]
	write_csv_table(athlete_table, "athletes_table.csv", athlete_header)

	olympic_table, olympic_dict = create_olympic_games_table(all_rows)
	# from now on, headers are directly passed into write_csv_table()
	write_csv_table(olympic_table, "olympic_games_table.csv", ["ID", "year", "season", "city"])

	team_table, team_dict = create_one_map_one_table(all_rows, "team")
	noc_table, noc_dict = create_NOC_table("noc_regions.csv")
	medals_table, medals_dict = create_one_map_one_table(all_rows, "medal")
	sport_categories_table, sport_categories_dict = create_one_map_one_table(all_rows, "sport_category")
	detailed_events_table, detailed_events_dict = create_one_map_one_table(all_rows, "detailed_event")

	write_csv_table(team_table, "teams_table.csv", ["ID", "Team"])
	write_csv_table(noc_table, "nocs_table.csv", ["ID", "noc", "full_name", "notes"])
	write_csv_table(medals_table, "medals_table.csv", ["ID", "medal"])
	write_csv_table(sport_categories_table, "sport_categories_table.csv", ["ID", "sport_category"])
	write_csv_table(detailed_events_table, "detailed_events_table.csv", ["ID", "detailed_event"])

	main_table_header = ["event_ID", "athlete_ID", "age", "height", "weight", "team_ID", "noc_ID", "oly_game_ID", "sport_category_ID", "detailed_event_ID", "medal_ID"]
	main_events_table = create_main_events_table(athlete_dict, team_dict, noc_dict, olympic_dict, sport_categories_dict, detailed_events_dict, medals_dict, all_rows)
	write_csv_table(main_events_table, "main_events_table.csv", main_table_header)

if __name__ == '__main__':
    main()