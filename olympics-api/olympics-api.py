'''

olympics-api.py
Authors: Ann Beimers and Jimmy Zhong, 31 Jan, 2021

'''

import json

API_BASE_URL: 'http://localhost:5000'

def object_list_to_json_list(list_of_objects):
	json_string = json.dumps(list_of_objects)

def get_games():
	url = f'{API_BASE_URL}/games'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    game_list = json.loads(string_from_server)
    result_list = []
    for game_dictionary in game_list:
        id = game_dictionary.get('id', 0)
        year = game_dictionary.get('year', 0)
        season = game_dictionary.get('season', '')
		city = game_dictionary.get('city', '')
        result_list.append({'id':id, 'year':year, 'season':season, 'city':city})
    return result_list

def get_nocs():
	url = f'{API_BASE_URL}/nocs'
    data_from_server = urllib.request.urlopen(url).read()
    string_from_server = data_from_server.decode('utf-8')
    nocs_list = json.loads(string_from_server)
    result_list = []
    for nocs_dictionary in nocs_list:
        abbreviation = game_dictionary.get('abbreviation', '')
        name = game_dictionary.get('name', '')
        result_list.append({'abbreviation':abbreviation, 'name':name})
		    return result_list

def get_medalists_all(game_ID):

def get_medalists_noc(game_ID, specific_noc):


def main():
	parser = argparse.ArgumentParser(description='Get word info from the localhost:5000 API')

    parser.add_argument('action', help='', choices=['games', 'nocs', 'medalists'])

    parser.add_argument('games', help='')

    parser.add_argument('game_ID', help='')

	parser.add_argument('specific_noc', help='')

    args = parser.parse_args()

	if args.action == games:
		games_result = get_games()

	if args.action == nocs:
		nocs_result = get_nocs()

	if args.action == medalists:
		if args.specific_noc:
			medalists_result = get_medalists_noc(args.game_ID, args.specific_noc)
		else:
			medalists_result = get_medalists_all(args.game_ID)

if __name__ == '__main__':
    main(args)
