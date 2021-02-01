'''
Schema file for olympics-api queries.
'''

#REQUEST: /games
#SQL code for the first query:

SELECT olympic_games.oly_game_ID, year, season, city
FROM olympic_games
ORDER BY year DESC;

#REQUEST: /nocs
#query:

SELECT NOCs.NOC, NOCs.region
FROM NOCs
ORDER BY NOCs.region


#REQUEST: /medalists/games/<games_id>?[noc=noc_abbreviation]
#SQL code for the third query:

SELECT athletes.athlete_ID, athlete_name, sex, sport_category, detailed_event, medal, nocs.noc, main_events.oly_game_ID
FROM athletes, medals, main_events, nocs, detailed_events, sport_categories, olympic_games
WHERE main_events.oly_game_ID = 40
AND nocs.noc = 'USA'
AND nocs.nocs_ID = main_events.noc_ID
AND olympic_games.oly_game_ID = main_events.oly_game_ID
AND medals.medal_ID = main_events.medal_ID
AND athletes.athlete_ID = main_events.athlete_ID
AND detailed_events.detailed_event_ID = main_events.detailed_event_ID
AND sport_categories.sport_category_ID = main_events.sport_category_ID;
