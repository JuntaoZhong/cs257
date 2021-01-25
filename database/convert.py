import csv 

#read files ("ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal")


class a_row:
	"""object that takes in every element in a row of given csv file"""
	def __init__(self, athe_ID, athe_name, sex, age, height, weight, team, NOC, game, year, season, city, sport_category, detailed_event, medal):
		self.athe_ID = athe_ID
		self.athe_name = athe_name
		self.sex = sex
		self.age = age
		self.height = height
		self.weight = weight
		self.team = team
		self.NOC = NOC
		self.game = game
		self.year = year
		self.season = season
		self.city = city
		self.sport_category = sport_category
		self.detailed_event = detailed_event
		self.medal = medal


def create_one_map_one_table(all_rows, option): 
	""" returns a 2D array and dictionary of one_map_one style data, given a list of row objects as a parameter applicable to 
		option 1: [team] : ID, country_team (United State)
		option 2: [sport_category] : ID, sport_category (swimming)
		option 3: [detailed_event] : ID, sport_event (swimming man 100m freestyle)
		option 4: [medal] : ID, Gold/Silver/Bronze/NA
	"""
	table = []
	dictionary = {}
	index = 1
	option = (option.strip()).lower()

	if option != "team" and option != "sport_category" and option != "detailed_event" and option != "medal":
		print("your option for one_map_one table is not valid!")
		return 

	for a_row in all_rows:
		str_data = getattr(a_row, option)
		if str_data not in dictionary:
			this_row = [index, str_data]
			table.append(this_row)
			dictionary[str_data] = index
			index = index + 1
	return table, dictionary


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
	# repetition checking set
	athletes_dict = {}
	for a_row in all_rows:
		an_athlete = athlete(a_row.athe_name, a_row.athe_ID)
		if an_athlete not in athletes_dict:
			this_row = [a_row.athe_ID, a_row.athe_name, a_row.sex]
			athletes_table.append(this_row)
			athletes_dict[an_athlete] = a_row.athe_ID
	return athletes_table, athletes_dict

# create an country table: ID, abrivated name, fully spelled country name (later),
def create_NOC_table(all_rows): 
	"""returns a 2D array and dictionary of NOC ID and NOC names given a list of row objects as a parameter"""
	NOC_table = []
	NOC_dict = {}
	index = 1
	for a_row in all_rows: 
		if a_row.NOC not in NOC_dict: 
			this_row = [index, a_row.NOC]
			NOC_table.append(this_row)
			#country_set.add(a_row)
			NOC_dict[a_row.NOC] = index
			index = index + 1
	return NOC_table, NOC_dict
		
#make object combining year, season, and city 
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

# create an Olympic games table: ID, year, season, city
def create_olympic_games_table(all_rows):
	"""returns 2D array and dictionary of olympic game ID, and olympic """
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

def create_main_events_table(athlete_dict, team_dict, NOC_dict, olympic_games_dict, sport_category_dict, detailed_event_dict, medal_dict, all_rows):
	""" return main events table(that displays all the IDs accordingly) given the dictionary of each of the elements in the table as a parameter.
		main table: event_ID (huge), athlete_ID, Age(unchanged), Height(unchanged), Weight (unchanged), 
		team_ID, country_table_ID, Olympics_game_ID, sport_category_ID, detailed_events_ID
	"""
	main_events_table = []
	index = 1
	for row_obj in all_rows:
		# make athlete object to find its id from the dictionary
		an_athlete = athlete(row_obj.athe_name, row_obj.sex)
		athlete_id = athlete_dict[an_athlete]
		
		team_id = team_dict[row_obj.team]
		sport_category_id = sport_category_dict[row_obj.sport_category]
		detailed_event_id = detailed_event_dict[row_obj.detailed_event]
		medal_id = medal_dict[row_obj.medal]
		NOC_id = NOC_dict[row_obj.NOC]
		
		an_oly_game = olympic_game(row_obj.year, row_obj.season, row_obj.city)
		oly_game_id = olympic_games_dict[an_oly_game]
	
		# athlete Age	Height	Weight remains as they are
		this_row = [index, athlete_id, row_obj.age, row_obj.height, row_obj.weight, team_id, NOC_id, oly_game_id, sport_category_id, detailed_event_id, medal_id]
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

def print_table(table_list, file_name, header_list):
	"""print method to print the tables into a csv file given the table list, file name and the header of the individual columns """
	# example header_list ["ID", "country_three_letter", "full country_name"]
	num_col = len(table_list[0])
	if num_col != len(header_list):
		print("yooo! the number of cols between your list and header_list doesn't match!")
		print(num_col)
		print(len(header_list))
		return

	outfile = open(file_name, 'w')
	outfile.write(make_csv_row(header_list))

	# write actual data
	for row in table_list:
		outfile.write(make_csv_row(row))
	outfile.close()

def main():
	"""create all the individual csv files"""
	all_rows = []
	with open('athlete_events.csv') as file:
		read_in_file = list((csv.reader(file, skipinitialspace=True)))
	
	for row in read_in_file[1:]:
		if len(row) > 1:
			this_row = a_row(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],
			row[8], row[9], row[10], row[11], row[12], row[13], row[14])
			all_rows.append(this_row)
	
	athlete_table, athlete_dict = create_athlete_table(all_rows)
	athlete_header =["athlete_ID", "athlete_name", "sex"]
	print_table(athlete_table, "athletes_table.csv", athlete_header)

	team_table, team_dict = create_one_map_one_table(all_rows, "team")
	sport_categories_table, sport_categories_dict = create_one_map_one_table(all_rows, "sport_category")
	detailed_events_table, detailed_events_dict = create_one_map_one_table(all_rows, "detailed_event")
	medals_table, medals_dict = create_one_map_one_table(all_rows, "medal")

	teams_header, sport_categories_header, detailed_events_header, medals_header = ["ID", "Team"], ["ID", "sport_category"], ["ID", "detailed_event"], ["ID", "medal"]
	print_table(team_table, "teams_table.csv", teams_header)
	print_table(sport_categories_table, "sport_categories_table.csv", sport_categories_header)
	print_table(detailed_events_table, "detailed_events_table.csv", detailed_events_header)
	print_table(medals_table, "medals_table.csv", medals_header)

	NOC_table, NOC_dict = create_NOC_table(all_rows)
	NOC_header = ["ID", "NOCs"]
	print_table(NOC_table, "NOCs_table.csv", NOC_header)

	olympic_table, olympic_dict = create_olympic_games_table(all_rows)
	olympic_header = ["ID", "year", "season", "city"]
	print_table(olympic_table, "olympic_games_table.csv", olympic_header)

	main_table_header = ["event_ID", "athlete_ID", "age", "height", "weight", "team_ID", "NOC_ID", "oly_game_ID", "sport_category_ID", "detailed_event_ID", "medal_ID"]
	main_events_table = create_main_events_table(athlete_dict, team_dict, NOC_dict, olympic_dict, sport_categories_dict, detailed_events_dict, medals_dict, all_rows)
	print_table(main_events_table, "main_events_table.csv", main_table_header)

if __name__ == '__main__':
    main()



'''
# create an country table: ID, abrivated name, fully spelled country name (later),
def create_team_table(all_rows): 
	"""returns a 2D array and dictionary of team ID and team names given a list of row objects as a parameter"""
	teams_table = []
	#country_set = set()
	teams_dict = {}
	index = 0

	for a_row in all_rows: 
		if a_row.team not in teams_dict: 
			index = index + 1
			this_row = [index, a_row.team]
			teams_table.append(this_row)
			#country_set.add(a_row)
			teams_dict[a_row.team] = index
	return teams_table, teams_dict
'''
'''
# sport_events_table: ID, event, the sport it belongs to
class sport_event: 
	"""sport_event object that takes in sport name and category of the event """
	def __init__(self, sport_category, detailed_event):
		self.sport_category = sport_category
		self.detailed_event = detailed_event
	def __hash__(self):
		return hash(self.detailed_event)
	def __eq__(self, other):
		return self.detailed_event == other.detailed_event


def create_sport_events_table(all_rows):
	"""returns 2D array and dictionary of sport events ID and sport events object given a list of row objects as a parameter"""
	sport_events_table = []
	sport_events_dict = {}
	index = 0
	for a_row in all_rows:
		a_sport_event = sport_event(a_row.sport_category, a_row.detailed_event)
		if a_sport_event not in sport_events_dict:
			index = index + 1
			this_row = [index, a_row.sport_category, a_row.detailed_event]
			sport_events_table.append(this_row)
			sport_events_dict[a_sport_event] = index
	return sport_events_table, sport_events_dict	

# main table: event_ID (huge), athlete_ID, Age(unchanged), Height(unchanged), Weight (unchanged), team_ID, country_table_ID, Olympics_game_ID, Sport_events_ID
def create_main_events_table(athlete_dict, team_dict, NOC_dict, olympic_games_dict, sport_events_dict, all_rows):
	"""return main events table(that displays all the IDs accordingly) given the dictionary of each of the elements in the table as a parameter."""
	main_events_table = []
	index = 1
	for row_obj in all_rows:
		# make athlete object to find its id from the dictionary
		an_athlete = athlete(row_obj.athe_name, row_obj.sex)
		athlete_id = athlete_dict[an_athlete]
		
		team_id = team_dict[row_obj.team]
		NOC_id = NOC_dict[row_obj.NOC]
		
		an_oly_game = olympic_game(row_obj.year, row_obj.season, row_obj.city)
		oly_game_id = olympic_games_dict[an_oly_game]

		a_sport_event = sport_event(row_obj.sport_category, row_obj.detailed_event)
		sport_event_id = sport_events_dict[a_sport_event]
	
		# athlete Age	Height	Weight remains as they are
		this_row = [index, athlete_id, row_obj.age, row_obj.height, row_obj.weight, team_id, NOC_id, oly_game_id, sport_event_id]
		main_events_table.append(this_row)
		index = index + 1
	return main_events_table
'''

'''
	team_table, team_dict = create_team_table(all_rows)
	team_header = ["ID", "Team"]
	print_table(team_table, "team_table.csv", team_header)

	NOC_table, NOC_dict = create_NOC_table(all_rows)
	NOC_header = ["ID", "NOC"]
	print_table(NOC_table, "NOC_table.csv", NOC_header)

	olympic_table, olympic_dict = create_olympic_games_table(all_rows)
	olympic_header = ["ID", "year", "season", "city"]
	print_table(olympic_table, "olympic_games_table.csv", olympic_header)
	
	sport_events_table, sport_events_dict = create_sport_events_table(all_rows)
	sport_events_header = ["ID", "sport_category", "detailed_event"]
	print_table(sport_events_table, "sport_events_table.csv", sport_events_header)

	main_table_header = ["event_ID", "athlete_ID", "age", "height", "weight", "team_ID", "NOC_ID", "oly_game_ID", "sport_event_ID"]
	main_events_table = create_main_events_table(athlete_dict, team_dict, NOC_dict, olympic_dict, sport_events_dict, all_rows)
	print_table(main_events_table, "main_events_table.csv", main_table_header)
'''