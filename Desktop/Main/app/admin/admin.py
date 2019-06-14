from math import sqrt
from pymongo import MongoClient
from uuid import uuid4 as uid
from datetime import datetime as date
from random import randint

# local db
client = MongoClient('mongodb://localhost:27017/')
db = client.db_engine

def setUID():
    temp = uid()
    return temp.__str__()


class League:
    def __init__(self):
        self.leagues = {}

    def getLeague(self, league_id):
        '''
        Gets league record
        league_id: id of league (str)
        '''
        if findLeague(league_id):
            return leagues[league_id]
        return False

    def createLeague(self, game_id):
        league = {
            'game_id': game_id,
            'copper': {},
            'bronze': {},
            'silver': {},
            'gold': {},
            'platinum': {},
            'illudium': {},
            'rhodium': {},
            'diamond': {},
        }

    def updateLeague(self, league_id, key, value):
        '''
        Updates a league record
        league_id: id of league (str)
        key : key of field (str)
        value: new value to override (*)
        '''
        league = getLeague(league_id)
        if key in league:
            league[key] = value
            self.leagues[league_id] = league
            return True
        return False

    def deleteLeague(self, league_id):
        '''
        Deletes record of league
        league_id: id of league (str)
        '''
        if findLeague(league_id):
            self.leagues.pop(league_id)
            return True
        return False

    def findLeague(self, player_id):
        '''
        Looks up record of league
        league_id: id of league (str)
        '''
        if league_id in self.leagues:
            return True
        return False


class Games:
    def __init__(self):
        self.games = {}

    def addGame(self, name):
        '''
        Creates a new game
        player_id: id of player (str)
        '''
        # checks for game
        if findGame(game_id):
            return False

        game = {
            'game_id': setUID(),
            'title': name,
            'create_time': date.today().strftime('%Y/%m/%d'),
        }
        self.games[game['game_id']] = game

        # create new league
        League(game['game_id'])

        return True

    def getGame(self, game_id):
        '''
        Gets game record
        game_id: id of game (str)
        '''
        if findGame(game_id):
            return games[game_id]
        return False

    def updateGame(self, game_id, key, value):
        '''
        Updates a game record
        value: new value to override (*)
        '''
        game = getGame(game_id)
        if key in game:
            game[key] = value
            self.games[game_id] = game
            return True
        return False

    def removeGame(self, game_id):
        if findGame(game_id):
            self.games.pop(game_id)
            return True
        return False

    def findGame(self, game_id):
        '''
        Looks up record of game
        game_id: id of game (str)
        '''
        if game_id in self.games:
            return True
        return False


class Player:
    def __init__(self, username, balance=0, name=None, address=None, address2=None, city=None, state=None):
        self.players = {}

    def createPlayer(self):
        '''
        Creates a new player
        '''

        # checks for player
        if findPlayer(player_id):
            return False

        player = {
            'player_id': setUID(),
            'team_id': None,
            'ranking': None,
            'experience': None,
            'points': 0,
            'balance': balance,
            'inventory': [],
            'shipping': [],
            'games': [],
            'matches': [],
            'tournaments': [],
            'league': [],
            'username': username,
            'friends': [],
            'following': [],
            'address': {
                'name': name,
                'address': address,
                'address2': address2,
                'city': city,
                'state': state,
                'country': 'usa',
            },
            'join_date': date.today().strftime('%Y/%m/%d'),
        }
        self.players[player['player_id']] = player
        return True

    def getPlayer(self, player_id):
        '''
        Gets player record
        player_id: id of player (str)
        '''
        if findPlayer(player_id):
            return players[player_id]
        return False

    def updatePlayer(self, player_id, key, value):
        '''
        Updates a player record
        player_id: id of player (str)
        key : key of field (str)
        value: new value to override (*)
        '''
        player = getPlayer(player_id)
        if key in player:
            player[key] = value
            self.players[player_id] = player
            return True
        return False

    def deletePlayer(self, player_id):
        '''
        Deletes record of player
        player_id: id of member (str)
        '''
        if findPlayer(player_id):
            self.players.pop(player_id)
            return True
        return False

    def findPlayer(self, player_id):
        '''
        Looks up record of member
        player_id: id of member (str)
        '''
        if player_id in self.players:
            return True
        return False


class Teams:
    def __init__(self, player_id):
        self.team_id = setUID()
        self.captain = player_id
        self.members = {}
        self.games = []

    def createMember(self, player_id):
        '''
        Creates a new player for a team
        player_id: id of player (str)
        '''

        # checks for player
        if findPlayer(player_id):
            return False

        member = {
            'member_id': setUID(),
            'player_id': player_id,
            'team_id': self.team_id,
            'games': [],
            'create_time': date.today().strftime('%Y/%m/%d'),
        }
        self.members[member['member_id']] = member
        return True

    def getMember(self, player_id):
        '''
        Gets member record
        player_id: id of player (str)
        '''
        if findMember(player_id):
            return members[player_id]
        return False

    def updateMember(self, member_id, key, value):
        '''
        Updates a member record
        value: new value to override (*)
        '''
        member = getMember(member_id)
        if key in member:
            member[key] = value
            self.members[member_id] = member
            return True
        return False

    def deleteMember(self, member_id):
        '''
        Deletes record of match
        member_id: id of member (str)
        '''
        if findMember(member_id):
            self.members.pop(member_id)
            return True
        return False

    def findMember(self, member_id):
        '''
        Looks up record of member
        member_id: id of member (str)
        '''
        if member_id in self.members:
            return True
        return False


class Ranking:
    def __init__(self):
        self.ranking = {}


class Match:
    def __init__(self):
        self.matches = {}

    def createMatch(self, red, blue, points, tourney=None, league=None):
        '''
        Creates a match based on two user inputs.
        red: Individual/Team ID 1 (str)
        blue: Individual/Team ID 2 (str)
        points: How many points the match is worth (int)
        tourney: If match is linked to a tournament (Optional: str)
        league: Whether this is a league match. (Optional: str)
        '''
        match = {
            'match_id': setUID(),
            'players': [red, blue],
            'create_time': date.today().strftime('%Y/%m/%d'),
            'completed_time': None,
            'title': name,
            'value': points,
            'winner': None,
            'tournament': tourney,
            'league': league,
        }
        self.matches[match['match_id']] = match

        return match

    def getMatch(self, match_id):
        '''
        Gets new record
        match_id: id of match (str)
        '''
        if findMatch(match_id):
            return matches[match_id]
        return False

    def updateMatch(self, match_id, key, value):
        '''
        Updates a match record with new data
        match_id: id of match (str)
        key: key of field (str)
        value: new value to override (*)
        '''
        match = getMatch(match_id)
        if key in match:
            match[key] = value
            self.matches[match_id] = match
            return True
        return False

    def deleteMatch(self, match_id):
        '''
        Deletes record of match
        match_id: id of match (str)
        '''
        if findMatch(match_id):
            self.matches.pop(match_id)
            return True
        return False

    def findMatch(self, match_id):
        '''
        Looks up record of match
        match_id: id of match (str)
        '''

        if match_id in self.matches:
            return True
        return False


class Tournament:
    def __init__(self):
        self.tournaments = {}

    def _roundGenerator(self, input):
        return

    def createTournament(self, total, points=None):
        '''
        Creates a tournament based on inputs.
        total: all registered player_id/team_id (list)
        points: amount of points the tournament is worth (Optional: int)
        '''

        # fields for tournament generator
        players = total
        rounds = 1
        brackets = 2 ** rounds

        while brackets < len(players):
            rounds += 1
        while len(players) < brackets:
            players.append('None')

        # create tourney
        tourney = {
            'tournament_id': setUID(),
            'players': players,
            'create_time': date.today().strftime('%Y/%m/%d'),
            'completed_time': None,
            'value': points,
            'rounds': rounds,
            'winner': None,
            'matches': {k: [] for k in list(range(1, rounds + 1))},
            'brackets': brackets,
        }

        active = list(players)
        while len(active):
            tourney['matches'][1].append(
                self.createMatch(active.pop(randint(0, len(active))), active.pop(randint(0, len(active))), 0,
                                 tourney['tournament_id']))

        self.tournaments[tourney['tournament_id']] = tourney

        return tourney

    def getTournament(self, tourney_id):
        '''
        Gets new record of tourney
        tourney_id: id of tourney (str)
        '''
        if findTournament(tourney_id):
            return tournaments[tourney_id]
        return False

    def updateTournament(self, match_id, key, value):
        '''
        Updates a match record with new data
        match_id: id of match (str)
        key: key of field (str)
        value: new value to override (*)
        '''
        match = getMatch(match_id)
        if key in match:
            match[key] = value
            matches[match_id] = match
            return True
        return False

    def deleteTournament(self, tourney_id):
        '''
        Deletes record of Tourney
        tourney_id: id of match (str)
        '''
        if findTournament(tourney_id):
            self.tournaments.pop(tourney_id)
            return True
        return False

    def findTournament(self, tourney_id):
        '''
        Looks up record of tourney
        tourney_id: id of match (str)
        '''
        if tourney_id in self.tournaments:
            return True
        return False


class Admin:
    def __init__(self):
        self.active_matches = []
        self.completed_matches = []
