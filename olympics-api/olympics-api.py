'''

olympics-api.py
Authors: Ann Beimers and Jimmy Zhong, 31 Jan, 2021

'''

import json
import urllib
import sys
import argparse
import flask
import psycopg2

app = flask.Flask(__name__)

'''
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
'''

def execute_query(connection, query):
    ''' Given the full query string (in form of a list), and a connection object
    Execute query and return cursor object for the print function
    '''
    try:
        cursor = connection.cursor()
        query_command = "\n".join(query)
        print(query_command)
        cursor.execute(query_command)
        return cursor
    except Exception as search_not_sucessful:
        print(search_not_sucessful)
        exit()

def connect_database():
    ''' return a connection object to the postgres database, which is then used/passed down for querying
    '''
    from config import database
    from config import user
    from config import password
    try:
        connection = psycopg2.connect(database = database, user= user, password = password)
        print("connection successful!")
        return connection
    except Exception as e:
        print(e)
        exit()

@app.route('/')
def hello():
    return 'Hello, user of olympics database.'

@app.route('/medalists/games/<game_id>')
def get_medalists_all(game_id):
    query = ["SELECT athletes.athlete_ID, athlete_name, sex, sport_category, detailed_event, medal",
    "FROM athletes, medals, main_events, nocs, detailed_events, sport_categories, olympic_games",
    "WHERE main_events.oly_game_ID = " + str(game_id),
    "AND nocs.noc_ID = main_events.noc_ID",
    "AND olympic_games.oly_game_ID = main_events.oly_game_ID",
    "AND medals.medal_ID = main_events.medal_ID",
    "AND athletes.athlete_ID = main_events.athlete_ID",
    "AND detailed_events.detailed_event_ID = main_events.detailed_event_ID",
    "AND sport_categories.sport_category_ID = main_events.sport_category_ID",
    "ORDER BY CASE medal",
    "WHEN 'Gold' THEN 1",
    "WHEN 'Silver' THEN 2",
    "WHEN 'Bronze' THEN 3",
    "ELSE 4",
    "END;"]

    possible_noc_contrain = flask.request.args.get('noc')
    if possible_noc_contrain:
        query.insert(3, "AND nocs.noc = '{}'".format(str(possible_noc_contrain)))
    db_connection = connect_database()
    query_result = list(execute_query(db_connection, query))
    output_list_of_dicts = []
    for row in query_result:
        athlete_id, athlete_name, sex, sport_category, detailed_event, medal = row
        this_dict = {'athlete_id': athlete_id, 'athlete_name': athlete_name, 'athlete_sex': sex, 'sport': sport_category, 'event': detailed_event, 'medal': medal}
        output_list_of_dicts.append(this_dict)
    return json.dumps(output_list_of_dicts)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser('an olympics database api')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)


'''
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
'''