-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--\c tournament;
--\i tournament.sql;
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
	
CREATE OR REPLACE VIEW public.initial_pairs AS 
	SELECT table1.id AS id1, table1.player_id AS player_id1, table2.id AS id2, table2.player_id AS player_id2
	FROM 
	(SELECT t1.*, ROW_NUMBER() OVER (ORDER BY t1.player_id) AS trow_num1 FROM (SELECT standings.* FROM standings LIMIT (SELECT COUNT(*)/2 FROM standings)) AS t1) AS table1,
	(SELECT t2.*, ROW_NUMBER() OVER (ORDER BY t2.player_id) AS trow_num2 FROM (SELECT standings.* FROM standings LIMIT (SELECT COUNT(*)/2 FROM standings) OFFSET (SELECT COUNT(*)/2 FROM standings)) AS t2) AS table2
	WHERE table1.trow_num1 = table2.trow_num2;
	
CREATE OR REPLACE VIEW public.sort_by_wins AS
	SELECT * FROM standings ORDER BY wins DESC, loss;