--List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation.
SELECT NOC FROM NOCs
ORDER BY NOC;

--List the names of all the athletes from Kenya. If your database design allows it, sort the athletes by last name.
SELECT DISTINCT athlete_name, Team 
FROM athletes, teams, main_events
WHERE teams.Team LIKE '%Kenya%'
AND teams.team_ID = main_events.team_ID
AND athletes.athlete_ID = main_events.athlete_ID;

--List all the medals won by Greg Louganis, sorted by year. Include whatever fields in this output that you think appropriate.
SELECT athlete_name, medal, detailed_event, year, city
FROM athletes, medals, detailed_events, olympic_games, main_events
WHERE athletes.athlete_name LIKE '%Greg%'
AND athletes.athlete_name LIKE '%Louganis%'
AND medals.medal != 'NA'
AND athletes.athlete_ID = main_events.athlete_ID
AND medals.medal_ID = main_events.medal_ID
AND detailed_events.detailed_event_ID = main_events.detailed_event_ID
AND olympic_games.oly_game_ID = main_events.oly_game_ID
ORDER BY year;

--List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
SELECT nocs.noc, COUNT(medals.medal)
FROM nocs, medals, main_events
WHERE nocs.nocs_id = main_events.noc_ID
AND medals.medal_ID = main_events.medal_ID
AND medals.medal = 'Gold'
GROUP BY nocs.noc
ORDER BY COUNT(medals.medal) DESC;