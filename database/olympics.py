#!/usr/bin/env python3
'''
Written by Jimmy Zhong under Professor Jeff Ondich, CS Softwared Design
A python CLI that does very specific SQL queries 
'''
import psycopg2
import argparse
import csv
import sys

def get_parsed_arguments():
    parser = argparse.ArgumentParser(description='Do 3 types of query: ')
    parser.add_argument('-g', '--noc_gold_medal', action='store_true', help='no input value, list all NOCs and the number of gold medals they have won')
    parser.add_argument('-a', '--noc_athletes', nargs= 1, help='give me a specific NOC, I return all the athletes from it')
    parser.add_argument('-s', '--sport', nargs = 1, help='give me a sport name, I rank NOCs by gold medals obtained in this sport')
    parser.add_argument('-l', '--output_limit', metavar="num_rows", nargs = 1, help='limit the number of rows in the query output')
    parser.add_argument('-m', '--all_medals', action='store_true', help='use together with --sport, instead of sorting on gold medals, sort on all medals')
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def database_connection():
    ''' return a connection object to the postgres database, which is then used/passed down for querying
    '''
    from config import database
    from config import user
    from config import password
    try:
        connection = psycopg2.connect(database = database, user= user, password = password)
        return connection
    except Exception as fail_to_connect:
        print(fail_to_connect)
        exit()

def execute_query(connection, query):
    ''' Given the full query string (in form of a list), and a connection object
    Execute query and return cursor object for the print function
    '''
    try:
        cursor = connection.cursor()
        query_command = "\n".join(query)
        cursor.execute(query_command)
        return cursor
    except Exception as search_not_sucessful:
        print(search_not_sucessful)
        exit()

def noc_gold_medal_query(connection):
    ''' no input value, query builder to list all NOCs and the number of gold medals they have won
    '''
    query_title = "====== NOCs and numbers of gold medals they won, decreasing order ======"

    query = ["SELECT nocs.noc, COUNT(medals.medal)",
            "FROM nocs, medals, main_events",
            "WHERE nocs.nocs_id = main_events.noc_ID",
            "AND medals.medal_ID = main_events.medal_ID",
            "AND medals.medal = 'Gold'"
            "GROUP BY nocs.noc",
            "ORDER BY COUNT(medals.medal) DESC;"]
    return execute_query(connection, query), query_title

def noc_athlete_query(noc_string, connection):
    ''' query builder. Given an NOC, query all athletes under that NOC
    '''
    query_title = "====== athletes from NOC '" + noc_string + "' ======"

    query  = ["SELECT DISTINCT noc, athlete_name", 
        "FROM athletes, nocs, main_events", 
        "WHERE nocs.noc = '" + noc_string + "'",
        "AND nocs.nocs_id = main_events.noc_ID", 
        "AND athletes.athlete_ID = main_events.athlete_ID;"]
    return execute_query(connection, query), query_title

def noc_gold_medal_group_by_sport_query(sport_name, connection, order_by = "Gold"):
    ''' query builder. Given a sport name, ranks NOCs in the number of gold medals
    they won in that sport. option to rank by all medals is also available 
    '''
    query_title = "NOC, Sport Name, # Gold, # total medals ======"

    query = ["SELECT nocs.noc, sport_categories.sport_category, ",
    "COUNT(medals.medal) FILTER (WHERE medals.medal = 'Gold') AS gold_medals, ",
    "COUNT(medals.medal) FILTER (WHERE medals.medal != 'NA') AS total_medals ", 
    "FROM nocs, medals, main_events, sport_categories ", 
    "WHERE sport_categories.sport_category LIKE '%" + sport_name + "%' ",
    "AND nocs.NOCs_ID = main_events.NOC_ID ",
    "AND sport_categories.sport_category_ID = main_events.sport_category_ID ",
    "AND medals.medal_ID = main_events.medal_ID ",
    "GROUP BY nocs.noc, sport_categories.sport_category "]

    # order by total medals or gold medals
    if order_by.strip().title() == "Gold":
        query.append("ORDER BY COUNT(medals.medal) FILTER (WHERE medals.medal = 'Gold') DESC;")
    else: 
        query.append("ORDER BY COUNT(medals.medal) FILTER (WHERE medals.medal != 'NA') DESC;")
    return execute_query(connection, query), query_title

def print_cursor_result(cursor, title_string, line_limit = 50):
    ''' Print out the query result on the command prompt
    line_limit = -1: no line_limit at all
    '''
    result = list(cursor)
    line_limit = len(result) if line_limit == -1 else min(line_limit, len(result))

    print(title_string)
    if len(result) == 0:
        print("sorry, no result, are you sure your input is right?")
    for i in range(line_limit):
        row = result[i]
        line_to_print = str(row[0])
        for each in row[1:]:
            line_to_print = line_to_print + ' | ' + str(each)
        print(line_to_print)
    if line_limit > 50:
        print("Too long? use -l [int] flag to limit the output length!")

def user_query_handler(arguments, connection, output_limit):
    ''' parse users' command line argument and tidy up user search_string input
    This centralized program execute query according to the users' argument
    '''
    if arguments.noc_gold_medal:
        cursor_gold_medal, title_string = noc_gold_medal_query(connection)
        print_cursor_result(cursor_gold_medal, title_string, output_limit)
    
    if arguments.noc_athletes:
        clean_search_string = (arguments.noc_athletes)[0].strip().upper()
        if len(clean_search_string) != 3:
            print("error! you can only input a 3 letter noc code")
            return
        cursor_athlete, title_string = noc_athlete_query(clean_search_string, connection)
        print_cursor_result(cursor_athlete, title_string, output_limit)
    
    if arguments.sport:
        with open('sport_categories_table.csv') as file:
            input_all_sports = list(csv.reader(file, skipinitialspace=True))
        all_sport_string = input_all_sports[1][1]
        for row in input_all_sports[2:]:
            all_sport_string = all_sport_string + ', ' + str(row[1]) 
        
        clean_sport = (arguments.sport)[0].strip().title()
        if clean_sport not in all_sport_string:
            print("yooo, sport name no valid! here is the list of valid sports: ")
            print(all_sport_string)
            return

        medal_order_choice = "all_medals" if "all_medals" else "gold"
        cursor_sport_category, title_string = noc_gold_medal_group_by_sport_query(clean_sport, connection, medal_order_choice)
        print_cursor_result(cursor_sport_category, title_string, output_limit)

def main():
    connection = database_connection()
    arguments = get_parsed_arguments()
    
    output_length = -1 # -1 means print out all rows
    if arguments.output_limit:
        output_length = int(arguments.output_limit[0])

    user_query_handler(arguments, connection, output_length)

    connection.close()
    
if __name__ == "__main__":
    main()


