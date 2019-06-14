from . import db
from uuid import uuid4 as uid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from time import time
from hashlib import md5
from datetime import datetime
import operator
import itertools
import collections
from .cache import cache
import json, copy
import redis

# Redis Database Connection
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

Users = db.Users

class User:
    def __init__(self, username, email):
        self.username = username
        usr = Users.find_one({'username':username})
        self.id = usr['id']
        self.urole = "member"
        self.is_authenticated = True
        self.permission = "universal"

    def _createUser(self, new_user):
        '''
        Creates a new user
        new_user: info of new user (array)
        '''
        # checks for player
        if _validate_username(new_user['username']):
            return False
        '''
        new_user = {
            #'id' : str(uid()),
            'id' : setUID(),
            'firstname' : newuser['firstname'],
            'lastname' : newuser['lastname'],
            'email' : newuser['email'],
            'username' : newuser['username'],
            'pw' : setHash(newuser['pw']),
            'state' : newuser['state'],
            'zip' : newuser['zip'],
            'city' : newuser['city'],
            'country' : newuser['country'],
            'gender' : newuser['gender'],
            'timezone' : newuser['timezone'],
        }
        '''
        Users.insert_one(new_user)
        return True

    def _getUser(self):
        '''
        Gets member record
        username: username of user (str)
        '''
        if self.username:
            user = Users.find_one({'username':self.username})
            return {
                'firstname' : user['firstname'],
                'lastname' : user['lastname'],
                'email' : user['email'],
                'username' : user['username'],
                'state' : user['state'],
                'zip' : user['zip'],
                'city' : user['city'],
                'country' : user['country'],
                'gender' : user['gender'],
                'timezone' : user['timezone'],
            }
        return False

    def _updateUser(self, update_user):
        '''
        Updates a member record
        value: new value to override (*)
        '''
        '''
        update_user = {
            'firstname' : form.firstname.data,
            'lastname' : form.lastname.data,
            'email' : form.email.data,
            'username' : form.username.data,
            'state' : form.state.data,
            'zip' : form.zip.data,
            'city' : form.city.data,
            'country' : form.country.data,
            'gender' : form.gender.data,
            'timezone' : form.timezone.data,
        }
        '''
        user = Users.find_one({'username':self.username})
        Users.update_one({"id":user['id']},{"$set":update_user},upsert=True)
        return True

    def _deleteUser(self, username):
        '''
        Deletes record of match
        username: username of member (str)
        '''
        if _validate_username(username):
            Users.delete_one({'username':username})
            return True
        return False

    def _avatar(self, size):
        user = Users.find_one({'username':self.username})
        digest = md5(user['email'].lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def _validate_username(self, name):
        ''' validates if a user exists '''
        user = Users.find_one({'username':name})
        if user is not None:
            return False

    def _validate_email(self, email):
        ''' validates if a email exists '''
        email = Users.find_one({'email':email})
        if email is not None:
            return False

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


    # login manager
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        #print("<<<User get_id: ",self.username)
        return self.username

    # get the role type of the user
    def get_urole(self):
        return self.urole

    def has_perm(self):
        return self.permission

    # set uid
    @staticmethod
    def setUID():
        temp = uid()
        return temp.__str__()

    # password hash
    @staticmethod
    def setHash(pw):
        return generate_password_hash(pw)
    @staticmethod
    def checkPassword(hash, pw):
        return check_password_hash(hash, pw)
    @staticmethod
    def validate_username(name):
        ''' validates if a user exists '''
        user = Users.find_one({'username':name})
        if user is not None:
            return False
        return True
    @staticmethod
    def validate_email(email):
        ''' validates if a email exists '''
        email = Users.find_one({'email':email})
        if email is not None:
            return False
        return True
    @staticmethod
    def createUser(new_user):
        '''
        Creates a new user
        new_user: info of user (array)
        '''
        # checks for player
        if validate_username(newuser['username']):
            return False
        Users.insert_one(new_user)
        return True
    @staticmethod
    def getUser(username):
        '''
        Gets user record
        username: username of user (str)
        '''
        user = Users.find_one({'username':username})
        if user:
            return {
                'firstname' : user['firstname'],
                'lastname' : user['lastname'],
                'email' : user['email'],
                'username' : user['username'],
                'state' : user['state'],
                'zip' : user['zip'],
                'city' : user['city'],
                'country' : user['country'],
                'gender' : user['gender'],
                'timezone' : user['timezone'],
            }
        return False
    @staticmethod
    def updateUser(update_user):
        '''
        Updates a user record
        value: new value to override (*)
        '''
        Users.update_one({"username":update_user['username']},{"$set":update_user},upsert=True)
        return True
    @staticmethod
    def deleteUser(username):
        '''
        Deletes record of match
        username: username of member (str)
        '''
        if validate_username(username):
            Users.delete_one({'username':username})
            return True
        return False
    @staticmethod
    def avatar(username, size):
        user = Users.find_one({'username':username})
        if user is not None:
            digest = md5(user['email'].lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        return ""
    @staticmethod
    def validate_username(name):
        ''' validates if a user exists '''
        user = Users.find_one({'username':name})
        if user is not None:
            return False
        return True
    @staticmethod
    def validate_email(email):
        ''' validates if a email exists '''
        email = Users.find_one({'email':email})
        if email is not None:
            return False
        return True


class Admin:
    def __init__(self, username):
        self.username = username

    # login manager
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username

    # set uid
    @staticmethod
    def setUID():
        temp = uid()
        return temp.__str__()

    # password hash
    @staticmethod
    def setHash(pw):
        return generate_password_hash(pw)
    @staticmethod
    def checkPassword(hash, pw):
        return check_password_hash(hash, pw)


# Set Nested Dictionary
def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value

class PlayerQueued:
    '''
    Uses a hashmap to Store and Retrieve Queued Player
    '''

    def __init__(self):
        # Create Player Queues
        if r.get('playerqueued'):
            pass
        else:
            r.set('playerqueued', '{}')

        # create pqmap
        if r.get('pqmap'):
            pass
        else:
            r.set('pqmap', '{}')


    def findPQMAP(self, game_id, league_id, wager_amount, player_id, state):
        '''
        Returns T/F if item is in PQMAP based on game_id, league_id, wager_amount, player_id
        game_id = Game Id ( UID )
        league_id = League Id ( UID )
        player_id = Player Id ( UID )
        wager_amount = Money for wager ( Integer )
        state = status of Queued
        '''
        mconvert = r.get('pqmap')
        pqmap = json.loads(mconvert)

        if pqmap.get(game_id,{}). \
            get(league_id,{}). \
            get(wager_amount,{}). \
            get(state, {}). \
            get(player_id):
            return True

        return False


    def findPlayerQueued(self, id):
        '''
        Returns T/F if item is in playerqueued based on ID
        id = UID of playerqueued
        '''
        convert = r.get('playerqueued')
        playerqueued = json.loads(convert)

        if id in playerqueued:
            return True
        return False


    def getQueuedPlayer(self, id):
        '''
        Retrieves playerqueued based on ID
        id = UID of playerqueued
        '''
        if self.findPlayerQueued(id):
            convert = r.get('playerqueued')
            playerqueued = json.loads(convert)
            return playerqueued[id]
        raise Exception('Record Not Found.')
        return


    def getPQID(self, game_id, league_id, wager_amount, player_id, state):
        '''
        Retrieves ID of PlayerQueued
        game_id = Game Id ( UID )
        league_id = League Id ( UID )
        player_id = Player Id ( UID )
        wager_amount = Money for wager ( Integer )
        state = status of Queued
        '''
        if self.findPQMAP(game_id, league_id, wager_amount, player_id, state):
            mconvert = r.get('pqmap')
            pqmap = json.loads(mconvert)
            return pqmap[game_id][league_id][wager_amount][state][player_id]
        raise Exception('Record Not Found.')
        return


    def getPQMAP(self):
        '''
        Retrieves PQMAP
        '''
        mconvert = r.get('pqmap')
        pqmap = json.loads(mconvert)
        return pqmap

    def getPlayerQueued(self):
        '''
        Retrieves PlayerQueued
        '''
        convert = r.get('playerqueued')
        player_queued = json.loads(convert)
        return player_queued


    

    def createPlayerQueued(self, game_id, league_id, wager_amount, player_id, state):
        '''
        Creates PlayerQueued. Returns True if Valid.
        game_id = Game Id ( UID )
        league_id = League Id ( UID )
        player_id = Player Id ( UID )
        wager_amount = Money for wager ( Integer )
        state = status of Queued
        '''
        if self.findPQMAP(game_id, league_id, wager_amount, player_id, state):
            raise NameError("Duplicated Queued already exists.")
            return

        player_queued = {
            'id' : uid().__str__(),
            'game_id': game_id,
            'league_id': league_id,
            'wager_amount': wager_amount,
            'player_id': player_id,
            'created_time': datetime.now().__str__(),
            'state': state
            }

        # store values
        convert = r.get('playerqueued')
        playerqueued = json.loads(convert)
        playerqueued[player_queued['id']] = player_queued
        r.set('playerqueued', json.dumps(playerqueued))

        # stores id lookup
        pqmap = self.getPQMAP()

        # Update the PQMap
        nested_set(pqmap, [game_id, league_id, wager_amount, state, player_id], player_queued['id'])
        r.set('pqmap', json.dumps(pqmap))
        return True


    def updatePlayerQueued(self, id, state):
        '''
        Updates PlayerQueued entry
        '''
        if self.findPlayerQueued(id):

            player_queue = self.getQueuedPlayer(id)
            player_queued = self.getPlayerQueued()

            game = player_queue['game_id']
            league = player_queue['league_id']
            player = player_queue['player_id']
            wager_amount = player_queue['wager_amount']
            previous_state=player_queue['state']

            pqmap = self.getPQMAP()
            pqmap[game][league][wager_amount][previous_state].pop(player)
            if state not in pqmap[game][league][wager_amount]:
                pqmap[game][league][wager_amount][state] = {}
            pqmap[game][league][wager_amount][state][player]=player_queue['id']

            player_queue['state']=state
            player_queued.pop(id)
            player_queued[player_queue['id']]=player_queue

            r.set('playerqueued', json.dumps(player_queued))
            r.set('pqmap', json.dumps(pqmap))

            return True
        raise Exception('Record Not Found.')
        return

    def deletePlayerQueued(self, id):
        '''
        Deletes a category or thread within a category. Returns True if valid.
        id: UID of board name (str)
        thread_id: ID of thread to be deleted (str)
        '''
        player_queue = self.getQueuedPlayer(id)
        player_queued = self.getPlayerQueued()

        if self.findPQMAP(id):
            #process
            player_queued.pop(player_queue['id'])
            # process
            pqmap = self.getPQMAP()

            game = player_queue["game_id"]
            league = player_queue["league_id"]
            wager_amount = player_queue["wager_amount"]
            state = player_queue["state"]
            player = player_queue["player_id"]

            pqmap[game][league][wager_amount][state].pop(player)

            r.set('playerqueued', json.dumps(player_queued))
            r.set('pqmap', json.dumps(pqmap))
            return True
        raise Exception('Record Not Found.')
        return


    def findCandidate(self, game_id, league_id, wager_amount, player):
        candidates = self.getCandidates(game_id, league_id, wager_amount, "waiting", player)

        cand_with_date={}
        if len(candidates) > 0:
            for cand in candidates:
                cand_data = self.getQueuedPlayer(candidates[cand])
                cand_with_date[cand_data['id']]=cand_data['created_time']
            
            sorted_cands = sorted(cand_with_date, key=lambda kv: kv[1], reverse=True)
            return sorted_cands[0]
        else:
            return False


    def getCandidates(self, game_id, league_id, wager_amount,state, player):

        pqmap = self.getPQMAP()
        if pqmap.get(game_id,{}).get(league_id,{}).get(wager_amount,{}).get(state):
            candidates = copy.deepcopy(pqmap.get(game_id,{}).get(league_id,{}).get(wager_amount,{}).get(state))
            if candidates.get(player):
                candidates.pop(player)
            return candidates
        raise Exception('Record Not Found.')
        return


class MatchQueues:

    '''
    Uses a hashmap to Store and Retrieve Match Queue
    '''

    def __init__(self):
        # Create Match Queues
        if r.get('matchqueues'):
            pass
        else:
            r.set('matchqueues', '{}')

        # create mqmap
        if r.get('mqmap'):
            pass
        else:
            r.set('mqmap', '{}')


    def findMQMAP(self, player1_queue, player2_queue, state):
        '''
        Returns T/F if item is in MQMAP based on Queues of Players
        
        player1_queue = Id of First PlayerQueue
        player2_queue = Id of Second PlayerQueue
        state = State of Match Queues
        '''
        mconvert = r.get('mqmap')
        mqmap = json.loads(mconvert)

        if mqmap.get(state, {}).get(player1_queue, {}).get(player2_queue):
            return True
        return False


    def findMatchQueue(self, id):
        '''
        Returns T/F if item is in matchqueue based on ID
        id = UID of matchqueue
        '''
        convert = r.get('matchqueues')
        matchqueues = json.loads(convert)

        if id in matchqueues:
            return True
        return False


    def getMatchQueue(self, id):
        '''
        Retrieves matchqueue based on ID
        id = UID of matchqueue
        '''
        if self.findMatchQueue(id):
            convert = r.get('matchqueues')
            matchqueues = json.loads(convert)
            return matchqueues[id]
        raise Exception('Record Not Found.')
        return


    def getMQID(self, player1_queue, player2_queue, state):
        '''
        Retrieves ID of MatchQueues
        
        player1_queue = Id of First PlayerQueue
        player2_queue = Id of Second PlayerQueue
        state = State of Match Queues
        '''
        if self.findMQMAP(player1_queue,player2_queue, state):
            mconvert = r.get('mqmap')
            mqmap = json.loads(mconvert)
            return mqmap[state][player1_queue][player2_queue]
        raise Exception('Record Not Found.')
        return


    def getMQMAP(self):
        '''
        Retrieves MQMAP
        '''
        mconvert = r.get('mqmap')
        mqmap = json.loads(mconvert)
        return mqmap

    def getMatchQueues(self):
        '''
        Retrieves MatchQueues
        '''
        convert = r.get('matchqueues')
        matchqueues = json.loads(convert)
        return matchqueues
    

    def createMatchQueues(self, player1_queue, player2_queue, state ):
        '''
        Creates Match Queues. Returns True if Valid.
        
        player1_queue = Id of First PlayerQueue
        player2_queue = Id of Second PlayerQueue
        state = State of Match Queues
        '''
        

        if self.findMQMAP(player1_queue, player2_queue, state):
            raise NameError("Match Queue already exists.")
            return

        new_match_queue = {
            'id' : uid().__str__(),
            'player1': player1_queue,
            'player2': player2_queue,
            'created_time': datetime.now().__str__(),
            'state': state
        }

        # store values
        convert = r.get('matchqueues')
        matchqueues = json.loads(convert)
        matchqueues[new_match_queue['id']] = new_match_queue
        r.set('matchqueues', json.dumps(matchqueues))

        # stores id lookup
        mqmap = self.getMQMAP()

        # Update MQMap
        nested_set(mqmap, [state, player1_queue, player2_queue], new_match_queue['id'])
        
        r.set('mqmap', json.dumps(mqmap))
        return True

    def updateMatchQueues(self, id, state):
        '''
        Updates MatchQueues entry
        '''
        if self.findMatchQueue(id):

            queue = self.getMatchQueue(id)
            match_queues = self.getMatchQueues()

            player1 = queue['player1']
            player2 = queue['player2']
            previous_state=queue['state']

            mqmap = self.getMQMAP()
            mqmap[previous_state].pop(player1)
            mqmap[state][player1]={ player2: queue['id'] }

            queue['state']=state
            match_queues.pop(id)
            match_queues[queue['id']]=queue

            r.set('matchqueues', json.dumps(match_queues))
            r.set('mqmap', json.dumps(mqmap))

            return True
        raise Exception('Record Not Found.')
        return

    def deleteMatchQueue(self, id):
        '''
        Deletes MatchQueues.  Returns True if valid.
        id: UID of match queue (str)
        '''
        queue = self.getMatchQueue(id)
        matchqueues = self.getMatchQueues()

        if self.findMatchQueue(id):
            #process
            matchqueues.pop(queue['id'])
            # process
            mqmap = self.getMQMAP()

            state = queue["state"]
            player1 = queue["player1"]
            player2 = queue["player2"]

            mqmap[state].pop(player1)

            r.set('matchqueues', json.dumps(matchqueues))
            r.set('mqmap', json.dumps(mqmap))
            return True
        raise Exception('Record Not Found.')
        return


class EloRating:

    '''
    Uses a hashmap to Store and Retrieve Elo Ratings
    '''

    def __init__(self):
        # Create Elo Ratings
        if r.get('elo_ratings'):
            pass
        else:
            r.set('elo_ratings', '{}')

        # create ermap
        if r.get('ermap'):
            pass
        else:
            r.set('ermap', '{}')


    def findERMAP(self, game_id, league_id, player_id):
        '''
        Returns T/F if item is in ERMAP based on Game, League, Player
        
        game_id = Id of Game
        league_id = Id of League
        player_id = Id of Player
        '''
        mconvert = r.get('ermap')
        ermap = json.loads(mconvert)
        
        if ermap.get(game_id, {}).get(league_id, {}).get(player_id):
            return True
        return False


    def findEloRating(self, id):
        '''
        Returns T/F if item is in elorating based on ID
        id = UID of elorating
        '''
        convert = r.get('elo_ratings')
        elo_ratings = json.loads(convert)

        if id in elo_ratings:
            return True
        return False


    def getEloRating(self, id):
        '''
        Retrieves elorating based on ID
        id = UID of elorating
        '''
        if self.findEloRating(id):
            convert = r.get('elo_ratings')
            elo_ratings = json.loads(convert)
            return elo_ratings[id]
        raise Exception('Record Not Found.')
        return


    def getERID(self, game_id, league_id, player_id):
        '''
        Retrieves ID of Elo Rating
        
        game_id = Id of Game
        league_id = Id of League
        player_id = Id of Player
        '''
        if self.findERMAP(game_id, league_id, player_id):
            mconvert = r.get('ermap')
            ermap = json.loads(mconvert)
            return ermap[game_id][league_id][player_id]
        raise Exception('Record Not Found.')
        return


    def getERMAP(self):
        '''
        Retrieves ERMAP
        '''
        mconvert = r.get('ermap')
        ermap = json.loads(mconvert)
        return ermap

    def getEloRatings(self):
        '''
        Retrieves EloRatings
        '''
        convert = r.get('elo_ratings')
        elo_ratings = json.loads(convert)
        return elo_ratings


    def createEloRating(self, game_id, league_id, player_id, rating):
        '''
        Creates Elo Rating. Returns True if Valid.
        
        game_id = Id of Game
        league_id = Id of League
        player_id = Id of Player
        '''

        if self.findERMAP(game_id, league_id, player_id):
            raise NameError("Elo Rating already exists.")
            return

        new_elo_rating = {
            'id' : uid().__str__(),
            'game': game_id,
            'league': league_id,
            'player': player_id,
            'updated_time': datetime.now().__str__(),
            'rating': rating
        }

        # store values
        convert = r.get('elo_ratings')
        elo_ratings = json.loads(convert)
        elo_ratings[new_elo_rating['id']] = new_elo_rating
        r.set('elo_ratings', json.dumps(elo_ratings))

        # stores id lookup
        ermap = self.getERMAP()

        # Update the Elo Rating Hashmap
        nested_set(ermap, [game_id, league_id, player_id], new_elo_rating['id'])
        r.set('ermap', json.dumps(ermap))
        return True
    
    def updateEloRating(self, id, rating):
        '''
        Updates Elo Rating entry
        '''
        # Check updated Elo Rating instance is existing
        if self.findEloRating(id):

            elo_rating = self.getEloRating(id)
            elo_ratings = self.getEloRatings()

            elo_rating['rating']=rating
            elo_rating['updated_time']=datetime.now().__repr__()

            elo_ratings.pop(id)
            elo_ratings[elo_rating['id']]=elo_rating

            r.set('elo_ratings', json.dumps(elo_ratings))

            return True
        raise Exception('Record Not Found.')
        return

    def deleteEloRating(self, id):
        '''
        Deletes Elo Rating.  Returns True if valid.
        id: UID of elo rating (str)
        '''
        elo_rating = self.getEloRating(id)
        elo_ratings = self.getEloRatings()

        if self.findEloRating(id):
            #process
            elo_ratings.pop(elo_rating['id'])
            ermap = self.getERMAP()

            game = elo_ratings["game"]
            league = elo_ratings["league"]
            player = elo_ratings["player"]

            ermap[game][league].pop(player)

            r.set('elo_ratings', json.dumps(elo_ratings))
            r.set('ermap', json.dumps(ermap))
            return True
        raise Exception('Record Not Found.')
        return


    def find_by_game_league(self, game, league):
        '''
            Find Elo Ratings by Game and League

            Input: game_id and league_id
        '''
        # Get ERMap 
        ermap = self.getERMAP()
        data = ermap

        # Filter by Game
        if game != "":
            temp = {}
            if game in data:
                temp = {
                    game: data[game]
                }
            data = temp
        
        # Filter by League
        if league != "":
            temp = {}
            for key in data:
                if league in data[key]:
                    temp = data[key][league]
            data=temp

        return data


    def sort_by_rating(self, data):
        '''
        Sort data by Rating

        Input: data to be sorted
        Output: Sorted list of dictionaries
        '''
        temp = copy.deepcopy(data)
        result = []
        
        new_value = [ self.getEloRating(data[value]) for value in data ]
        sorted_x = sorted(new_value, key=lambda kv: kv['rating'], reverse=True)  

        for idx, val in enumerate(sorted_x):
            new_x = {
                "recid": idx + 1,
                "player": val['player'],
                "rating": val['rating'],
            }
            result.append(new_x)
        
        return result


# Social > Category/Boards Data Structure
class Tmessages:
    '''
    Uses a hashmap to store and retrieve Messages within Threads.
    '''
    def __init__(self):
        # create threads
        if r.get('tmessages'):
            pass
        else:
            dict = OrderedDict()
            r.set('tmessages', json.dumps(dict))

    def findMessage(self, id):
        '''
        Finds category messages
        id = UID of category name (str)
        '''
        convert = r.get('tmessages')
        messages = json.loads(convert)

        if id in messages:
            return True
        return False

    def getMessage(self, id):
        '''
        Retrieves thread based on ID
        id: UID of thread (str)
        '''
        if self.findMessage(id):
            convert = r.get('tmessages')
            messages = json.loads(convert)
            return messages[id]
        raise Exception('Record Not Found.')
        return

    def getMessages(self):
        '''
        Retrieves all messages
        '''
        convert = r.get('tmessages')
        messages = json.loads(convert)
        return messages

    def createMessage(self, thread_id, author, message):
        '''
        Creates messages for threads in social.html. Returns True if valid.
        thread_id: id of category thread (str)
        author: Author username (str)
        message: Text Body (str)
        '''
        messages = self.getMessages()

        message = {
            'id' : uid().__str__(),
            'thread_id' : thread_id,
            'author' : author,
            'message' : message,
            'time' : str(date.now())
            }

        messages[message['id']] = message
        r.set('tmessages', json.dumps(messages))

        # updates thread with message id
        thread = Thread()
        thread.updateThread(message['thread_id'], message_id=message['id'])
        return True

    def updateMessage(self, id, **kwargs):
        '''
        Updates thread entries
        id = UID of category name (str)
        author = updates author name (str)(keyword)
        message = updates body message of thread (str)(keyword)
        '''
        if self.findMessage(id):
            msg = self.getMessage(id)
            messages = self.getMessages()

            if 'author' in kwargs:
                # process
                author = kwargs.get('author')
                msg['author'] = author
                messages[msg['id']] = msg

                # storage
                r.set('tmessages', json.dumps(messages))
                return True

            if 'message' in kwargs:
                # process
                message = kwargs.get('message')
                msg['message'] = message
                messages[msg['id']] = msg

                # storage
                r.set('tmessages', json.dumps(messages))
                return True
        raise Exception('No Entry Found to Update.')
        return

    def deleteMessage(self, id):
        '''
        Delete a Message
        id: UID of thread (str)
        thread_id: UID of message (str)
        '''
        if self.findMessage(id):
            message = self.getMessage(id)
            messages = self.getMessages()

            # deletes message from thread
            thread = Thread()
            thread.deleteThread(message['thread_id'], message_id=message['id'])

            # deletes message from hashmap
            messages.pop(message['id'])
            r.set('tmessages', json.dumps(messages))
            return True
        raise Exception('Record Not Found.')
        return

class Thread:
    '''
    Uses a hashmap to Store and Retrieve Threads.
    '''
    def __init__(self):
        # create threads
        if r.get('threads'):
            pass
        else:
            r.set('threads', '{}')

        # create tmap
        if r.get('tmap'):
            pass
        else:
            r.set('tmap', '{}')

    def findTMAP(self, title):
        '''
        Returns T/F if item is in TMAP based on name
        title = Game title (str)
        '''
        mconvert = r.get('tmap')
        tmap = json.loads(mconvert)

        if title in tmap:
            return True
        return False

    def findThread(self, id):
        '''
        Finds category threads
        id = UID of category name (str)
        '''
        convert = r.get('threads')
        threads = json.loads(convert)

        if id in threads:
            return True
        return False

    def getTID(self, title):
        '''
        Retrieves thread ID based on name
        title: name of thread (str)
        '''
        if self.findTMAP(title):
            mconvert = r.get('tmap')
            tmap = json.loads(mconvert)
            return tmap[title]
        return False

    def getTMAP(self):
        '''
        Retrieves TMAP
        '''
        mconvert = r.get('tmap')
        tmap = json.loads(mconvert)
        return tmap

    def getThreads(self):
        '''
        Returns Thread Collection
        '''
        convert = r.get('threads')
        threads = json.loads(convert)
        return threads

    def getThread(self, id):
        '''
        Retrieves thread based on ID
        id: UID of thread (str)
        '''
        if self.findThread(id):
            convert = r.get('threads')
            threads = json.loads(convert)
            return threads[id]
        raise Exception('Record Not Found.')
        return

    def createThread(self, category_id, author, title, body, **kwargs):
        '''
        Creates board Threads for social.html. Returns True if valid.
        category_id: id of category thread (str)
        author: Author username (str)
        title: Name of thread (str)
        body: Text Body (str)

        Optional.
        hashtags = List of hashtags for message (list)
        image = object (obj)
        '''

        # checks for exisitng thread
        if self.getTID(title):
            raise NameError("A thread already exists with this name.")
            return

        thread = {
            'id' : uid().__str__(),
            'author' : author,
            'category' : category_id,
            'title' : title,
            'body' : body,
            'hashtag' : [],
            'messages' : [],
            'likes' : [],
            'image': ''
            }

        # inserts in hashtags
        if 'hashtag' in kwargs:
            hashtag = kwargs.get('hashtag')
            if not isinstance(hashtag, list):
                raise TypeError('hashtag paramater must be a list or blank.')
                return
            for x in hashtag:
                thread['hashtag'].append(x)

        # sends image to Content Delivery Network for storage
        if 'image' in kwargs:
            img = kwargs.get('image')
            # sendCDN(img)

        # process new entries
        tmap = self.getTMAP()
        threads = self.getThreads()
        
        thread['image']=img
        threads[thread['id']] = thread
        tmap[thread['title']] = thread['id']

        # store entries
        r.set('tmap', json.dumps(tmap))
        r.set('threads', json.dumps(threads))

        # updates category with new thread
        Cat = Category()
        Cat.updateCategory(category_id, thread_id=thread['id'])
        return True

    def updateThread(self, id, **kwargs):
        '''
        Updates thread entries
        id = UID of category name (str)
        message_id = Message ID of Post (str)(keyword)
        author = updates author name (str)(keyword)
        likes = user likes associated with a thread (str)(keyword)
        title = updates title of thread (str)(keyword)
        body = updates body message of thread (str)(keyword)
        hashtag = updates hashtags once per query (str)(keyword)
        '''

        threads = self.getThreads()
        thread = self.getThread(id)

        if 'message_id' in kwargs:
            # process
            message_id = kwargs.get('message_id')

            # check for duplicate entry
            if message_id in thread['messages']:
                raise Exception("Duplicate Entry")
                return

            thread['messages'].append(message_id)
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True

        if 'likes' in kwargs:
            # process
            likes = kwargs.get('likes')

            # check for duplicate entry
            if likes in thread['likes']:
                raise Exception("Duplicate Entry")
                return

            thread['likes'].append(likes)
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True

        if 'author' in kwargs:
            author = kwargs.get('author')

            # check for duplicate entry
            if author in thread['author']:
                raise Exception("Duplicate Entry")
                return

            thread['author'] = author
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True

        if 'title' in kwargs:
            title = kwargs.get('title')

            # check for duplicate entry
            if title in thread['title']:
                raise Exception("Duplicate Entry")
                return

            thread['title'] = title
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True

        if 'body' in kwargs:
            body = kwargs.get('body')

            # check for duplicate entry
            if body in thread['body']:
                raise Exception("Duplicate Entry")
                return

            thread['body'] = body
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True

        if 'hashtag' in kwargs:
            hashtag = kwargs.get('hashtag')

            # check for duplicate entry
            if hashtag in thread['hashtag']:
                raise Exception("Duplicate Entry")
                return

            thread = self.getThread(id)
            thread['hashtag'].append(hashtag)
            threads[thread['id']] = thread

            # store
            r.set('threads', json.dumps(threads))
            return True
        raise Exception('No Entry Found to Update.')
        return

    def deleteThread(self, thread_id, **kwargs):
        '''
        Delete a thread or field. One entry at a time.
        thread_id: UID of thread name (str)
        category_id: UID of category (str)
        message_id: UID of message (str)(keyword)
        likes: delete a like associated with a thread (str)(keyword)
        hashtag: hashtag name (str)(keyword)
        '''
        threads = self.getThreads()
        thread = self.getThread(thread_id)

        if 'message_id' in kwargs:
            message_id = kwargs.get('message_id')
            thread['messages'].remove(message_id)

            # storage
            threads.pop(thread_id)
            threads[thread['id']] = thread
            r.set('threads', json.dumps(threads))
            return True

        if 'likes' in kwargs:
            likes = kwargs.get('likes')
            thread['likes'].remove(likes)

            # storage
            threads.pop(thread_id)
            threads[thread['id']] = thread
            r.set('threads', json.dumps(threads))
            return True


        if 'hashtag' in kwargs:
            hashtag = kwargs.get('hashtag')
            thread['hashtag'].remove(hashtag)

            # storage
            threads.pop(thread_id)
            threads[thread['id']] = thread
            r.set('threads', json.dumps(threads))
            return True

        if self.findThread(thread_id):
            # removes from category
            cat = Category()
            cat.deleteCategory(thread['category'], thread_id)

            # removes from threads
            tmap = self.getTMAP()
            tmap.pop(thread['title'])
            threads.pop(thread_id)
            r.set('threads', json.dumps(threads))
            r.set('tmap', json.dumps(tmap))
            return True
        raise Exception('Record Not Found.')
        return

    @staticmethod
    def sendCDN(image):
        pass

    @staticmethod
    def get_current_threads_by_page(uid, page, page_by):
        th = Thread()
        threads = th.getThreads()
        paginator = Paginator(
            total=len(threads), 
            per_page=page_by, 
            current_page=page
        )
        next_page = paginator.next_page
        currents = th.getThread(uid)
        return (currents, next_page)


class Category:
    '''
    Uses a hashmap to Store and Retrieve board and threads.
    '''
    def __init__(self):
        # create categories
        if r.get('categories'):
            pass
        else:
            r.set('categories', '{}')

        # create cmap
        if r.get('cmap'):
            pass
        else:
            r.set('cmap', '{}')

    def findCMAP(self, title):
        '''
        Returns T/F if item is in CMAP based on name
        title = Game title (str)
        '''
        mconvert = r.get('cmap')
        cmap = json.loads(mconvert)

        if title in cmap:
            return True
        return False

    def findCategory(self, id):
        '''
        Returns T/F if item is in categories based on ID
        id = UID of category name (str)
        '''
        convert = r.get('categories')
        categories = json.loads(convert)

        if id in categories:
            return True
        return False


    def getCategory(self, id):
        '''
        Retrieves board category based on ID
        id: UID of board name (str)
        '''
        if self.findCategory(id):
            convert = r.get('categories')
            categories = json.loads(convert)
            return categories[id]
        raise Exception('Record Not Found.')


    def getCID(self, title):
        '''
        Retrieves ID of Game title
        title = Game title (str)
        '''
        if self.findCMAP(title):
            mconvert = r.get('cmap')
            cmap = json.loads(mconvert)
            return cmap[title]
        raise Exception('Record Not Found.')


    def getCMAP(self):
        '''
        Retrieves CMAP
        '''
        mconvert = r.get('cmap')
        cmap = json.loads(mconvert)
        return cmap

    def getCategories(self):
        '''
        Retrieves Categories
        '''
        convert = r.get('categories')
        cat = json.loads(convert)
        return cat

    def createCategory(self, title):
        '''
        Creates board Categories for social.html. Returns True if Valid.
        title: Name of board (string)
        '''
        if self.findCMAP(title):
            raise NameError("Category name already exists.")
            return

        category = {
            'id' : uid().__str__(),
            'title' : title,
            'threads' : []
            }

        # store values
        convert = r.get('categories')
        categories = json.loads(convert)
        categories[category['id']] = category
        r.set('categories', json.dumps(categories))

        # stores id lookup
        cmap = self.getCMAP()
        cmap[category['title']] = category['id']
        r.set('cmap', json.dumps(cmap))
        return True

    def updateCategory(self, id, **kwargs):
        '''
        Updates category board entry
        id = UID of category name (str)
        title = title of the category (str)(keyword)
        thread_id = id of the thread (str)(keyword)
        '''
        if self.findCategory(id):

            category = self.getCategory(id)
            categories = self.getCategories()

            # updates title
            if 'title' in kwargs:
                # process
                title = kwargs.get('title')
                cmap = self.getCMAP()
                cmap.pop(category['title'])
                category.update({'title':title})
                cmap[title] = category['id']

                # storage
                categories.pop(id)
                categories[category['id']] = category
                r.set('categories', json.dumps(categories))
                r.set('cmap', json.dumps(cmap))
                return True

            # updates threads
            if 'thread_id' in kwargs:
                # process
                thread_id = kwargs.get('thread_id')

                # check for duplicate entry
                if thread_id in category['threads']:
                    raise Exception("Duplicate Entry")
                    return
                category['threads'].append(kwargs.get('thread_id'))

                # storage
                categories.pop(id)
                categories[category['id']] = category
                r.set('categories', json.dumps(categories))
                return True

            return True
        raise Exception('Record Not Found.')
        return

    def deleteCategory(self, id, thread_id=None):
        '''
        Deletes a category or thread within a category. Returns True if valid.
        id: UID of board name (str)
        thread_id: ID of thread to be deleted (str)
        '''
        category = self.getCategory(id)
        categories = self.getCategories()

        if thread_id != None:
            if self.findCategory(id):
                #process
                category['threads'].remove(thread_id)
                categories.pop(category['id'])

                # storage
                categories[category['id']] = category
                r.set('categories', json.dumps(categories))
                return True
            raise Exception('Record Not Found.')
            return

        if self.findCategory(id):
            # process
            cmap = self.getCMAP()
            cmap.pop(category['title'])
            categories.pop(category['id'])

            # storage
            r.set('categories', json.dumps(categories))
            r.set('cmap', json.dumps(cmap))
            return True
        raise Exception('Record Not Found.')
        return

