DROP TABLE IF EXISTS athletes;
CREATE TABLE athletes (
    athlete_ID INT NOT NULL,
    athlete_name text,
    sex text
);
\copy athletes from 'athletes_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER


DROP TABLE IF EXISTS main_events;
CREATE TABLE main_events (
	event_ID INT NOT NULL,
	athlete_ID INT NOT NULL,
	age INT,
	height decimal,
	weight decimal,
	team_ID INT,
	NOC_ID INT,
	oly_game_ID INT NOT NULL,
	sport_category_ID INT NOT NULL,
	detailed_event_ID INT NOT NULL,
	medal_id INT
);
\copy main_events from 'main_events_table.csv' DELIMITER ',' CSV NULL 'NA' HEADER


DROP TABLE IF EXISTS teams;
CREATE TABLE teams (
    team_ID INT NOT NULL,
    Team text
);
\copy teams from 'teams_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER

DROP TABLE IF EXISTS NOCs;
CREATE TABLE NOCs (
    NOC_ID INT NOT NULL,
    NOC text,
    region text,
    notes text
);
\copy NOCs from 'NOCs_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER

DROP TABLE IF EXISTS sport_categories;
CREATE TABLE sport_categories (
    sport_category_ID INT NOT NULL,
    sport_category text
);
\copy sport_categories from 'sport_categories_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER

DROP TABLE IF EXISTS detailed_events;
CREATE TABLE detailed_events (
    detailed_event_ID INT NOT NULL,
    detailed_event text
);
\copy detailed_events from 'detailed_events_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER

DROP TABLE IF EXISTS medals;
CREATE TABLE medals (
    medal_ID INT NOT NULL,
    medal text
);
\copy medals from 'medals_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER

DROP TABLE IF EXISTS olympic_games;
CREATE TABLE olympic_games (
	oly_game_ID INT NOT NULL,
	year INT NOT NULL,
	season text,
	city text
);
\copy olympic_games from 'olympic_games_table.csv' DELIMITER ',' CSV NULL AS 'NULL' HEADER
