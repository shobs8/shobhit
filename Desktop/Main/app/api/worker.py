import pika
import time
from . import db
import random
from datetime import datetime as date
import pymongo

import redis
from . import api

r = redis.Redis(
    host='localhost',
    port="6379", 
    db=0)


UserMatches = db.UserMatches
Users = db.Users

def callback(ch, method, properties, body):
    print(" >>>>>>>>>>>>>>>>>>>>>>>> [x] Received %r from RabbitMQ" % body)
    time.sleep(body.count(b'.'))
    message = body.decode("utf-8").split('#')
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(" <<<<<<<<<<<<<<<<<<<<<<<< [x] Done for one queue from RabbitMQ")

    # Process for queue got
    if message[0] == "Join":
        match = UserMatches.find_one({'id':message[1]})
        if match:
            arrMember = match['members']
            arrMember.append(message[2])
            print("         ---> arrMember: ", arrMember)
            
            if match['players'] == match['cur_players'] + 1:
                creator = arrMember[0]
                members = ",".join(arrMember[1:])                

                winIndex = random.randint(0,len(arrMember)-1)
                print(" >>>>>>>>>>>>>>>>>>>> Started match:[%s] => Creator:[%s], Member:[%s], len:[%d], winIndex:[%d]" % (message[1], creator, members, len(arrMember), winIndex))
                winId = arrMember[winIndex]
                winner = winId;

                for mid in arrMember:
                    member = Users.find_one({'id':mid})
                    matches = member['matches']
                    matches.append(message[1])
                    update_user = {
                        'matches': matches
                    }
                    Users.update_one({"id":mid},{"$set":update_user},upsert=True)

                    if mid == winId:
                        print("         >>>>>>> Winner: [%s]" % member['username'])
                        winner = member['username']

                update_match = {
                    'cur_players' : match['cur_players'] + 1,
                    'members' : arrMember,
                    'completed_time' : date.today().strftime('%Y/%m/%d'),
                    'winner' : winner,
                }
                UserMatches.update_one({"id":message[1]},{"$set":update_match},upsert=True)

                return;

            update_match = {
                'cur_players' : match['cur_players'] + 1,
                'members' : arrMember
            }
            UserMatches.update_one({"id":message[1]},{"$set":update_match},upsert=True)


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' -------> [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                        queue='task_queue')

    channel.start_consuming()


def cache_to_db():
    print(" >>>>>>>>>>>>>>>>>>>>>>>> Cache to DB")

    for key in r.keys():
        value = r.get(key)
        
        db.redis.update_one(
            {
                'Key': key.decode('ASCII')
            },
            {
                "$set": {
                    'Value': value.decode('ASCII')
                }
            },
            upsert=True
        )

    print(" >>>>>>>>>>>>>>>>>>>>>>>> Done")


def db_to_cache():
    print(" >>>>>>>>>>>>>>>>>>>>>>>> DB to Cache")
    for document in db.collection.find():
        r.set(document['Key'], document['Value'])
    print(" >>>>>>>>>>>>>>>>>>>>>>>> Done")