-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
\c tournament;
\i tournament.sql;

create table players(
	id serial primary key, 
	name text
	);
	
create table standings(
	id serial primary key, 
	totalmatches int, 
	wins int, 
	loss int, 
	player_id int references players(id)
	);
	
create table matches(
	id serial primary key,
	player1_id int references players(id),
	player2_id int references players(id),
	winner int
	);