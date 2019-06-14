from pymongo import MongoClient
from uuid import uuid4 as uid
from datetime import datetime
import random, pandas

''' Shell Script to Creates Pseudo Orders for Python Mongo '''

# Connect to DB
client = MongoClient('mongodb://localhost:27017/')
db = client.main_app

def createMatches(count):
    ''' Generates a Match '''
    matches = []
    users = list(db.Users.find({}))
    while count > 0:
        players = []
        for user in users:
            if random.randint(0, 1) == 1:
                players.append(user['id'])
        match = {
            'match_id' : str(uid()),
            'title' : 'Match ' + str(count),
            'players' : players,
            'observers': [],
            'create_time' : datetime.now(),
            'completed_time' : None,
            'value' : random.randint(1, 100),
            'winner' : None,
        }
        matches.append(match)
        count -= 1
    for x in matches:
        db.Matches.insert_one(x)
    return

def createGames(count):
    games = []
    while count > 0:
        game = {
            'game_id': str(uid()),
            'title': 'Game ' + str(count),
            'date': datetime.now()
        }
        games.append(game)
        count -= 1

    for x in games:
        db.Games.insert_one(x)
    return

def updateUsers():
    users = list(db.Users.find({}))
    matches = list(db.Matches.find({}))
    friends = {}
    for x in users:
        friends[x['id']] = []
    for x in users:
        for y in users:
            if random.randint(0, 1) == 1 and y['id'] != x['id']:
                if not y['id'] in friends[x['id']]:
                    friends[y['id']].append(x['id'])
                    friends[x['id']].append(y['id'])
    for x in users:
        attendedMatches = []
        for y in matches:
            if x['id'] in y['players']:
                attendedMatches.append(y['match_id'])
        db.Users.update_one({
            "id": x['id']
        }, {
            "$set": {
                "team_id": None,
                "ranking": None,
                "experience": None,
                "points": random.randint(1, 100),
                "balance": random.randint(1, 1000),
                "inventory": [],
                "shipping": [],
                "games": [],
                "matches": attendedMatches,
                "observers": [],
                "tournaments": [],
                "league": [],
                "friends": friends[x['id']],
                "following": [],
                "address": {
                    'name': '',
                    'address': '',
                    'address2': '',
                    'city': '',
                    'state': '',
                    'country': 'usa',
                },
                'join_date' : datetime.now()
            }
        })
    return
def main():
    # Get User choices
    while True:
        print("1. Matches | 2. Games | 3. Update Users")
        selection, amount = 0, 0

        try:
            selection = int(input("Please enter your choice: "))
        except:
            print("Not a valid option.")

        if selection == 1:
            try:
                amount = int(input("Please enter how many records you want: "))
            except:
                print("Not a valid option.")
            if amount > 0:
                createMatches(amount)
                break
        elif selection == 2:
            try:
                amount = int(input("Please enter how many records you want: "))
            except:
                print("Not a valid option.")
            if amount > 0:
                createGames(amount)
                break
        elif selection == 3:
            updateUsers()
            break
        else:
            print("Not a valid option. Please try again.")

if __name__ == "__main__":
    main()
    while True:
        choice = str(input("More Entries? Y or N: "))
        if choice.lower() == 'y':
            main()
        elif choice.lower() == 'n':
            print("-----Completed-----")
            break
        else:
            print("Invalid Entry.")
