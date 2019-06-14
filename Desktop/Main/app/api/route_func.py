import pika, random
from hashlib import md5
import os, sys, string

import math 

# Function to calculate the Probability 
def Probability(rating1, rating2):   
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)) 
    
# Function to calculate Elo rating 
# K is a constant. 
# d determines whether 
# Player A wins or Player B.  
def EloRating(Ra, Rb, K, d): 
    # To calculate the Winning 
    # Probability of Player B 
    Pb = Probability(Ra, Rb) 
  
    # To calculate the Winning 
    # Probability of Player A 
    Pa = Probability(Rb, Ra) 
  
    # Case->1 When Player A wins 
    # Updating the Elo Ratings 
    if (d == 1) : 
        Ra = Ra + K * (1 - Pa) 
        Rb = Rb + K * (0 - Pb) 
  
    # Case->2 When Player B wins 
    # Updating the Elo Ratings 
    else : 
        Ra = Ra + K * (0 - Pa) 
        Rb = Rb + K * (1 - Pb) 
  
    print("Updated Ratings:-") 
    print("Ra =", round(Ra, 6)," Rb =", round(Rb, 6)) 

    return [Ra, Rb]

def send_task(cmd, msg, pid):
    ''' Process for Rabbitmq '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    message = '%s#%s#%s' % (cmd, msg, pid)
    print("     ---> message: ",message)
    channel.basic_publish(exchange='',
                        routing_key='task_queue',
                        body=message,
                        properties=pika.BasicProperties(
                            delivery_mode = 2, # make message persistent
                        ))
    print(" [x] Sent %r" % message)
    connection.close()

def avatar(email, size):
    ''' sets avatar logo taken from gravastar '''
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

def generate_brackets_double_elimination(teams):
    pass

def generate_brackets_round_robin(teams):
    pass

def get_new_ref_id():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))

def allowed_file(filename):
    ''' method for choosing form file path '''
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_duplicate_participants(team_list):
    seen = set()
    seen_add = seen.add
    return [x for x in team_list if not (x in seen or seen_add(x))]

def generate_brackets_single_elimination(team_fixture, depth, number_of_players, team_list):
    advanced = 2 ** (depth + 2)
    for i in range(2):
        team_index = team_list.index(team_fixture[i])
        if advanced - team_index <= number_of_players:
            team_fixture[i] = [team_fixture[i], team_list[advanced-team_index-1]]
            generate_brackets_single_elimination(team_fixture[i], depth + 1, number_of_players, team_list)

def generate_brackets(bracket_data):
    tournament_type = bracket_data.get('tournament_type')
    bracket_size = bracket_data.get('bracket_size')

    if bracket_size == 'size':
        number_of_participants = bracket_data.get('number_of_participants')
        team_list = [x for x in range(1, int(number_of_participants)+1)]
    else:
        participants_team = bracket_data.get('participants_team')
        team_list = participants_team.strip().split('\r\n')
        team_list = remove_duplicate_participants(team_list)

    team_fixture = []
    if tournament_type == 'single elimination':
        team_fixture = team_list[:2]
        generate_brackets_single_elimination(team_fixture, 0, len(team_list), team_list)

    elif tournament_type == 'double elimination':
        data = generate_brackets_double_elimination(team_list)

    else:
        data = generate_brackets_round_robin(team_list)

    return team_fixture
