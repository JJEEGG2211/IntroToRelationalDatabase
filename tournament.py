#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn=connect()
    c=conn.cursor()
    c.execute("delete from matches")
    c.execute("update standings set totalmatches=0, wins=0, loss=0")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn=connect()
    c=conn.cursor()
    c.execute("delete from standings;")
    c.execute("delete from players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn=connect()
    c=conn.cursor()
    row = c.execute("select count(*) from players;")
    cnt = c.fetchone()[0]
    
    if cnt is not None:
		count = cnt
    else:
		count = 0
    conn.close()
    return count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db=connect()
    c=db.cursor()
    c.execute("insert into players(name) values (%s);", (name,))    
    db.commit()
    c.execute("select id from players where name=%s order by id desc limit 1;", (name,))
    idOfLastAddedPlayer = c.fetchone()[0]
    db.close()
    if idOfLastAddedPlayer is not None:
        db=connect()
        c=db.cursor()
        c.execute("insert into standings(totalmatches, wins, loss, player_id) values (0,0,0,%s)", (idOfLastAddedPlayer,))
        db.commit()
        db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn=connect()
    c=conn.cursor()
    c.execute("select players.id, players.name, standings.wins, standings.totalmatches from players, standings where players.id=standings.player_id order by standings.wins desc")
    list = c.fetchall()
    conn.close()
    return list
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches(player1_id, player2_id, winner) values (%s, %s, %s)", (winner,loser,winner))
    db.commit()
    c.execute("select wins from standings where player_id=%s", (winner,))
    winsCount = c.fetchone()[0]
    winsCount += 1
    c.execute("select totalmatches from standings where player_id=%s", (winner,))
    totalGames = c.fetchone()[0]
    totalGames += 1
    c.execute("update standings set wins=%s, totalmatches=%s where player_id=%s", ((winsCount,), (totalGames,), (winner,)))
    
    c.execute("select loss from standings where player_id=%s", (loser,))
    lossCount = c.fetchone()[0]
    lossCount += 1
    c.execute("select totalmatches from standings where player_id=%s", (loser,))
    totalGames = c.fetchone()[0]
    totalGames += 1
    c.execute("update standings set loss=%s, totalmatches=%s where player_id=%s", ((lossCount,), (totalGames,), (loser,)))
    
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    c = db.cursor()
    c.execute("SELECT winners.id, p1.name, losers.id, p2.name \
    FROM winners, losers, players AS p1, players AS p2 \
    WHERE winners.rwnum = losers.rwnum AND \
    winners.player_id=p1.id AND \
    losers.player_id=p2.id")
    list = c.fetchall()
    db.close()
    #print list
    return list