from flask import render_template, \
                json, url_for, flash, redirect, request, \
                jsonify, g, Flask, send_from_directory, \
                session, json, current_app
from flask_login import login_user, logout_user, login_required, current_user
from uuid import uuid4 as uid
from datetime import datetime as date
from .forms import  RegisterForm, LoginForm, BracketGeneratorForm, \
                    CreateTournamentForm, TournamentRegistrationForm, \
                    ProfileForm, ThreadForm, SponsorshipForm
from .data import User, Thread, Category, \
                  PlayerQueued, MatchQueues, EloRating
from . import api, db
from werkzeug.utils import secure_filename
from bson import json_util
from .route_func import EloRating as EloRatingCal, send_task, avatar, allowed_file, get_new_ref_id, \
                        generate_brackets, generate_brackets_single_elimination, \
                        remove_duplicate_participants, \
                        generate_brackets_double_elimination, \
                        generate_brackets_round_robin
from .cache import cache
from flask_paginate import Pagination, get_page_args, get_page_parameter
import os, sys, string
from os.path import dirname, abspath

from ..decorator import permission_required

player_queued = PlayerQueued()
match_queues = MatchQueues()
elo_ratings = EloRating()
th = Thread()
cat = Category()

leagues = ['copper','bronze','silver','gold','platform','illudium','rhodium','diamond']

# Tournaments
@api.route('/bracket-generator', methods=['GET','POST'])
def bracket_generator():
    form = BracketGeneratorForm()
    if form.validate_on_submit():
        generate_bracket_data = form.data
        if request.args.get('ref'):
            ref = request.args.get('ref')
            stored_generate_bracket_data = db.GenerateBracket.find_one({'id':ref})
            if stored_generate_bracket_data:
                generate_bracket_data.update({'id':ref})
                db.GenerateBracket.update_one(generate_bracket_data)
            else:
                ref = get_new_ref_id()
                generate_bracket_data.update({'id':ref})
                db.GenerateBracket.insert_one(generate_bracket_data)
        else:
            ref = get_new_ref_id()
            generate_bracket_data.update({'id':ref})
            db.GenerateBracket.insert_one(generate_bracket_data)
        return redirect(url_for('bracket_generator', ref=ref))

    if request.args.get('ref'):
        ref = request.args.get('ref')
        generate_bracket_data = db.GenerateBracket.find_one({'id':ref})
        data = generate_brackets(generate_bracket_data)
        return render_template('api/bracket_display.html', title='Bracket Display', data=data)
    else:
        return render_template('api/bracket_generator.html', title='Bracket Generator', form=form)

# Tournaments
@api.route('/create-tournament', methods=['GET', 'POST'])
@login_required
def create_tournament():
    form = CreateTournamentForm()
    if form.validate_on_submit():
        pass
    return render_template('api/create_tournament.html', title='Create Tournament', form=form)

# Tournaments
@api.route('/tournament/<tournament_id>/registration', methods=["GET","POST"])
def tournament_regisration(tournament_id):
    tournament = db.Tournaments.find_one({'tournament_id':tournament_id})
    if request.method=='POST':
        form = TournamentRegistrationForm()
        if form.validate_on_submit():
            data = form.data
            tourna_id = data.get('tournament')
            email = data.get('player_email')
            if tourna_id == tournament_id and email == current_user.email:
                tournament = db.Tournaments.find_one({'tournament_id':tournament_id})
                user = db.Users.find_one({'id':current_user.username})
                players = tournament.get('players')
                if user['id'] not in players:
                    players.append(user['id'])
                    db.Tournaments.update_one(
                        {"tournament_id":tournament["tournament_id"]},
                        {"$set":{
                            "players":players
                        }
                        })
                flash("Registerd Successfully.", category="info")
                return redirect(url_for('tournament_information', tournament_id=tournament_id))
            else:
                flash("Something went wrong!! Please try again.",  category="error")
    else:
        form = TournamentRegistrationForm(player_nickname=current_user.username, player_email=current_user.email, tournament=tournament_id)

# Tournaments
@api.route('/tournament/<tournament_id>/information', methods=["GET"])
def tournament_information(tournament_id):
    tournament = db.Tournaments.find_one({'tournament_id':tournament_id})
    user_registered = False
    tournament_players = tournament.get('players')
    if current_user.username in tournament_players:
        user_registered = True
    return render_template('api/tournament.html', title='Tournament Information',tournament=tournament, page_type="info_page", user_already_registered=user_registered)

# Tournaments
@api.route('/tournaments')
def get_tournaments():
    data = db.Tournaments.find()
    tournaments = []
    for each in data:
        each.pop('_id')
        tournaments.append(each)
    return jsonify({"tournaments":tournaments})

#Chat room
@api.route('/setroom', methods=['POST'])
@login_required
def setroom():
    data = request.json
    oldRoom = session.get('chat_room', '')
    if data['type'] == 'friend':
        userId = session.get('user_id', '')
        if data['id'] > userId:
            newRoom = (data['id'] + '-' + userId)
        else:
            newRoom = (userId + '-' + data['id'])
    else:
        newRoom = data['id']

    if oldRoom == newRoom:
        return jsonify({'success': 0})
    else:
        session['chat_room'] = newRoom
        return jsonify({'success': '1', 'room': newRoom})
        # get chat history of the room

# Chat Room
@api.route('/getchat', methods=['GET'])
@login_required
def getchat():
    chathistory = db.Chat.find({'room': session.get('chat_room', '')}).sort('sent_at')
    value = ''
    for message in chathistory:
        value += (message['msg'] + '\n')
    return jsonify({'chat': value})

# home page
@api.route('/joinMatch', methods=['POST'])
@login_required
def join_match():
    if request.method == 'POST':
        item = request.json

    # add to database
    match = db.UserMatches.find_one({'id':item['id']})
    db.UserMatches.update(match,{'$set': {match['current']:'active'}})
    db.UserMatches.update(match,{'$set': {match['user_id']:current_user.get_id()}})
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response

# add the match info user matches info
@api.route('/createusermatch', methods=['POST'])
@login_required
def create_user_match():
    if request.method == 'POST':
        item = request.json

        # create new static object
        new_item = {
            'id': str(uid()),
            'current':'pending',
            'user_id': current_user.get_id(),
            'create_time' : date.today().strftime('%Y/%m/%d'),
            'members' : [current_user.get_id()],
            'completed_time' : None,
            'winner' : None,
            'players' : 2,
            'cur_players' : 1
        }

        # append dic with form post
        size = len(item)
        while size >= 0:
            new_item[item[size-1]['name']] = item[size-1]['value']
            size -= 1

        # add to database
        db.UserMatches.insert_one(new_item)

        # Process for Rabbitmq
        send_task('Create', new_item['id'], current_user.get_id())
        flash('Item Added.')
        return jsonify(success=1)

# update user match info
@api.route('/updateusermatch', methods=['POST'])
@login_required
def update_user_match():
    if request.method == 'POST':
        item = request.json
        print("++++++++++ getmatches ++++++++++++ item: ", item)
        myId = current_user.get_id()
        match = db.UserMatches.find_one({'id':item['id']})
        if myId in match['members']:
            print("---------- Player [%s] (You) are already joined into this game --------" % (myId))
            return jsonify(success=0,players=[])

        send_task('Join', item['id'], current_user.get_id())

        players = "%d / %d" % (match['cur_players']+1, match['players'])
        print(' ---> players: ', players)
        return jsonify(success=1,players=players)

# get user match info
@api.route('/getusermatch', methods=['POST'])
@login_required
def get_user_match():
    if request.method == 'POST':
        item = request.json
        #print("++++++++++ getmatches ++++++++++++ item: ", item)
        matches = db.UserMatches.find({'user_id':current_user.get_id()})
        mymatch = {}
        for match in matches:
            mymatch = {
                'console': match['console'], #"PS4", #
                'game': match['game'], #"Fortnite", #
                'input': match['input'], #'Console Controller', #
                'your_wager': match['your_wager'], #"10", #
                'game_rules': {
                    'match_length': match['game_rules']['match_length'], #"one", #
                    'game_type': match['game_rules']['game_type'], #"squads", #
                    'custom_rules': match['game_rules']['custom_rules'], #"" #
                },
                'odds_advantages': match['odds_advantages'], #"1", #
            }

            break

        print("------------- get_user_match mymatch: ", mymatch)
        if not mymatch:
            return jsonify(success=0,match=mymatch)
        return jsonify(success=1,match=mymatch)

# get matches info
@api.route('/getmatches', methods=['POST'])
@login_required
def get_matches():
    if request.method == 'POST':
        item = request.json
        print("++++++++++ getmatches ++++++++++++ item: ", item)
        matches = db.Matches.find({'user_id':current_user.get_id()})
        arrMatches = []
        for match in matches:
            arrMatches.append({"type":hist['type'], "date":hist['date'], "reason":hist['reason'],
            "adjustments":hist['adjustments'], "description":hist['description']})

        return jsonify(matches=arrMatches)

# get match schemas
@api.route('/getschemas', methods=['POST'])
@login_required
def get_schemas():
    if request.method == 'POST':
        item = request.json
        print("++++++++++ getschemas ++++++++++++ item: ", item)
        schemas = db.Schemas.find()
        arrSchemas = []
        for scheme in schemas:
            arrSchemas.append({"type":hist['type'], "date":hist['date'], "reason":hist['reason'],
            "adjustments":hist['adjustments'], "description":hist['description']})
        return jsonify(schemas=arrSchemas)

#add as observer of match
@api.route('/addobserver', methods=['POST'])
@login_required
def addobserver():
    matchId = request.json['match_id']
    userId = session.get('user_id', '')
    db.Matches.update(
        { 'match_id': matchId },
        { '$addToSet': { 'observers': userId  } }
    )
    db.Users.update(
        { 'id': userId },
        { '$addToSet': { 'observers': matchId  } }
    )
    return jsonify({'success': '1'})

#get observers of the match
@api.route('/getobservers', methods=['GET'])
@login_required
def getobservers():
    userId = session.get('user_id', '')
    user = db.Users.find_one({ 'id': userId })
    return jsonify({'observers': user['observers']})

# Inventory Item panel
@api.route('/getinven', methods=['GET', 'POST'])
@login_required
def get_inventory():
    print("\n get_inventory >>> $$$$$$$$$$$$$$$$$$")
    if request.method == 'POST':
        data = request.json
        #print("++++++++++ get_inventory itemid: ",data)
        itemid = data['id']
        user = db.Users.find_one({'id':current_user.get_id()})
        inventory = user['inventory']
        #print("     >>> inventory: ",invens)
        if itemid in user['inventory'] :
            inventory.remove(itemid)
            db.Users.update_one({'id':current_user.get_id()}, {"$set":{"inventory":inventory}}, upsert=True)
        return jsonify(success=1,msg='success')

    #request.method: GET
    user = db.Users.find_one({{'id':current_user.get_id()}})
    inventory = user['inventory']
    inventory.append('charm1.png')
    inventory.append('charm2.png')
    inventory.append('charm3.png')
    inventory.append('charm4.png')
    inventory.append('charm5.png')

    return jsonify(ok=1,msg='success',invens=inventory,ids=ids)

# home page
@api.route('/')
@login_required
@permission_required(perms_list=["universal"])
def home():
    userId = session.get('user_id', '')
    user = db.Users.find_one({'id': userId})
    games = db.Games.find({})
    matches = db.Matches.find({'match_id' : {'$in': user['matches']}})
    newMatches = db.Matches.find({'match_id' : {'$nin': user['matches']}})
    friends = db.Users.find({'id' : {'$in': user['friends']}})
    mymatches = db.UserMatches.find({'winner':None})


    return render_template('api/index.html', title='Home', fortnites=games, \
    matches=matches, newMatches=newMatches, friends=friends, mymatches=mymatches, \
    )

# Profile
@api.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    print("\n routes : profile > $$$$$$$$$$$$$$$$$$")

    # Remove this list after implementation of Game Model
    main_games = [
        { 'id':'cod', 'title':'cod'},
        { 'id':'lol', 'title':'lol'},
        { 'id':'dota', 'title':'dota'}
    ]

    curDirPath = os.path.dirname(os.path.realpath(__file__))
    UPLOAD_FOLDER = os.path.join(curDirPath,"static/upload")
    if(request.method == 'POST') and ('picture' in request.files or 'cover' in request.files):
        print(request.files)
        file_obj = request.files
        print("file_obj========================",file_obj)
        try:
            for f in file_obj:
                file = request.files.get(f)
                print("file=============================",file)
                if file.filename == '':
                    print("Noooooooooooooooooooooooooooooooo")
                    flash('No selected file')
                    return jsonify(ok=0,msg='No Selected File!')

                imgfilepath = ""
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    imgfilepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(imgfilepath)
                    # append image urls
                    fileUrl = 'static/upload/' + filename
                    print("file=================================",fileUrl)
                if 'picture' in request.files:
                    update_item = {'avatar': fileUrl}
                elif 'cover' in request.files:
                    update_item = {'cover': fileUrl}
                else:
                    update_item = {}
                db.Users.update_one({'id':current_user.get_id()}, {"$set":update_item}, upsert=True)
        except:
            return jsonify(ok=0,msg='Failed to upload user image!')

        return jsonify(ok=1,msg='success',picture_url=fileUrl)

    form = ProfileForm()
    if form.validate_on_submit():
        update_user= {
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
            'about_me': form.about_me.data
        }
        db.Users.update_one({"id":current_user.get_id()},{"$set":update_user},upsert=True)

        flash('User Profile Updated.')
        return redirect(url_for('api.profile'))

    user = db.Users.find_one({'id':current_user.get_id()})
    form.state.default = user['state']
    form.country.default = user['country']
    form.gender.default = user['gender']
    form.timezone.default = user['timezone']
    form.process()
    form.firstname.data = user['firstname']
    form.lastname.data = user['lastname']
    form.email.data = user['email']
    form.username.data = user['username']
    form.state.default = user['state']
    form.zip.data = user['zip']
    form.city.data = user['city']
    form.about_me.data = user.get('about_me', '')
    avtr = user['avatar']
    cover = user.get('cover', '')
    if avtr == "":
        avtr = avatar(user['email'],128)

    mymatches = []
    for mid in user['matches']:
        match = db.UserMatches.find_one({'id':mid})
        mymatches.append(match)

    mysponsors = db.Sponsorship.find({'user_id': current_user.get_id()})

    search = False
    PER_PAGE = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # get current user
    user_id = current_user.get_id()
    user = db.Users.find_one({'id': user_id})

    if user:
        
        # get first 10 matches of current user from db
        matches = db.UserMatches.find({'user_id': user_id}).skip((page - 1) * PER_PAGE).limit(PER_PAGE)
        matches_list = list(matches)

        pagination = Pagination(page=page,
                                per_page=PER_PAGE,
                                per_page_parameter=(((page - 1) * len(matches_list)) + PER_PAGE),
                                total=matches.count(), search=search, record_name='matches')

        # count wins and losses
        wins = db.UserMatches.count({'$and': [
            {'winner': user_id}, {'winner': {'$ne': None}}
        ]})
        losses = db.UserMatches.count({'winner': {'$ne': user_id}})

        # calculate prize of current user using pymongo aggregate method
        prize_pipeline = [{'$match': {'winner': user_id}}, {'$group': {'_id': None, 'total': {'$sum': 'your_wager'}}}]
        sum_prize = json_util.dumps(db.UserMatches.aggregate(pipeline=prize_pipeline))
        total_prize = 0
        if len(json_util.loads(sum_prize)) > 0:
            total_prize = json_util.loads(sum_prize)[0]['total']

        sponsor_form = SponsorshipForm()

        # handle POST request
        if sponsor_form.validate_on_submit():
            new_sponsorship = {
                'id': str(uid()),
                'user_id': user_id,
                'name': form.name.data,
                'email': form.email.data,
                'gender': form.gender.data,
                'card_number': form.card_number.data,
                'card_expiry_month': form.card_expiry_month.data,
                'card_expiry_year': form.card_expiry_year.data,
                'card_cvv': form.card_cvv.data,
                'message': form.message.data,
                'billing_address': form.billing_address.data,
                'zip': form.zip.data,
                'city': form.city.data,
                'state': form.state.data,
                'country': form.country.data,
                'amount': form.amount.data,
                'anonymous': form.anonymous.data,
                'every_month': form.every_month.data,
                'created_at': date.now()
            }
            db.Sponsorship.insert_one(new_sponsorship)
            # Process for Rabbitmq
            send_task('Create', new_sponsorship['id'], user_id)
            flash('Congratulations {}, you have contributed towards a success journey!'.format(form.name.data))


    return render_template(
        'api/profile.html', 
        title='Profile', 
        form=form, 
        avatar=avtr, 
        cover=cover, 
        mymatches=mymatches,
        mysponsors=mysponsors, 
        games=main_games, 
        leagues=leagues, 
        sponsor_form=sponsor_form,
        user=user, 
        matches=matches_list,
        wins=wins, 
        losses=losses, 
        total_prize=total_prize, 
        pagination=pagination, 
    )

# Crafting
@api.route('/crafting')
@login_required
def crafting():
    return render_template('api/crafting.html', title='Crafting')

# Social
@api.route('/social', methods=['GET', 'POST'])
@login_required
def social():
    user = db.Users.find_one({'id':current_user.get_id()})
    form = ThreadForm()

    threads = th.getThreads()
    categories = cat.getCategories()
    
    context = {
        'title': 'Social',
        'threads': threads,
        'categories': categories,
    }
    if form.validate_on_submit():
        image = request.files['image']
        image_name = secure_filename(image.filename)
        realpath = os.path.dirname(os.path.realpath(__file__))
        static_dir = dirname(dirname(abspath(__file__)))
        uploadpath = os.path.join('static', 'upload', 'thread', image_name)
        image_path = os.path.join(static_dir, uploadpath)
        image.save(image_path)
        print('+++++++++++')
        print(form.cat.data)
        print(user['uid'])
        print(form.title.data)
        print(form.description.data)
        print(form.hashtag.data)
        print(threads)
        print(categories)

        th.createThread(
            cat.getCID(form.cat.data),
            user['uid'],
            form.titl2e.data,
            form.description.data,
            hashtag = list(form.hashtag.data),
            image = uploadpath,
        )
        flash('Congratulations, you created {}!'.format(form.title.data))
        return redirect(url_for('api.social'))
    return render_template('api/social.html', title='Social', context=context, form=form)

@api.route('/social/category/<uid>', methods=['POST'])
@login_required
def get_category_threads(uid):
    data = json.loads(request.data)
    page = data['page']
    page_by = 5
    currents, next_page = th.get_current_threads_by_page(uid, page, page_by)
    resp = {
        'threads': currents,
        'next_page': next_page,
    }
    return json_util.dumps(resp)


@api.route('/social/thread/<uid>', methods=['POST'])
@login_required
def get_thread(uid):
    user = db.Users.find_one({'id':current_user.get_id()})
    user_uid = user['uid']
    thread = th.getThread(uid)
    return json_util.dumps(thread)


@api.route('/social/message/<uid>', methods=['POST'])
@login_required
def add_message(uid):
    file_obj = request.files
    if file_obj:
        image = file_obj['file']
        image_name = secure_filename(image.filename)
        realpath = os.path.dirname(os.path.realpath(__file__))
        uploadpath = os.path.join('static', 'upload', 'thread', image_name)
        image_path = os.path.join(realpath, uploadpath)
        image.save(image_path)

    message_content = request.form.get('message')
    message_type = int(request.form.get('type'))
    thread = request.form.get('thread')
    user = db.Users.find_one({'id':current_user.get_id()})
    pika_conf = current_app.config['PIKA_CONF']
    message = {
        'user': user['uid'],
        'thread': thread,
        'message_type': message_type,
        'message_content': message_content,
    }
    if message_type == 1:
        message['image'] = uploadpath
        message['task'] = 'create_thread_message'
        Publisher(pika_conf).publish(str(message))
    else:
        message['task'] = 'create_thread_author_message'
        Publisher(pika_conf).publish(str(message))
    return jsonify({'status': True})


@api.route('/social/thread/message/<uid>', methods=['POST'])
@login_required
def thread_message(uid):
    user = db.Users.find_one({'id':current_user.get_id()})
    user_uid = user['uid']
    data = json.loads(request.data)
    thread = th.getThread(data['thread'])
    messages = thread['messages']
    return json_util.dumps(messages)


@api.route('/social/thread/follow/<uid>', methods=['POST'])
@login_required
def thread_follow(uid):
    data = json.loads(request.data)
    user = db.Users.find_one({'id':current_user.get_id()})
    # association = ThreadFollowerAssociation(thread=data['thread'], user=user['uid']).follow()
    # Should be refactored as a property of User model.
    if db.Users.find_one({'uid': user['uid'], 'following_threads': {'$exists': False}}):
        db.Users.update({'uid': user['uid']}, {'$set': {'following_threads': []}})
    db.Users.update({'uid': user['uid']}, {'$push': {'following_threads': data['thread']}})
    return jsonify({'status': True})


@api.route('/social/thread/unfollow/<uid>', methods=['POST'])
@login_required
def thread_unfollow(uid):
    data = json.loads(request.data)
    user = db.Users.find_one({'id':current_user.get_id()})
    #association = ThreadFollowerAssociation(thread=data['thread'], user=user['uid']).unfollow()
    db.Users.update({'uid': user['uid']}, {'$pull': {'following_threads': data['thread']}})
    return jsonify({'status': True})

@api.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@api.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

# Shop
@api.route('/shop')
@login_required
def shop():
    return render_template('api/shop.html', title='Shop')

# Missions
@api.route('/missions')
@login_required
def missions():
    return render_template('api/missions.html', title='Missions')

# signup page
@api.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        print('this is working!')
    if current_user.is_authenticated:
        return redirect(url_for('api.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = {
            'uid': User.setUID(),
            'id': form.username.data,
            'firstname':form.firstname.data,
            'lastname':form.lastname.data,
            'email':form.email.data,
            'username': form.username.data,
            'pw': User.setHash(form.pw.data),
            'state': form.state.data,
            'zip': form.zip.data,
            'city': form.city.data,
            'country': form.country.data,
            'gender': form.gender.data,
            'timezone': form.timezone.data,
            'avatar': "",
            'games' : [],
            'matches' : [],
            'friends' : [],
            'inventory' : [],
        }
        db.Users.insert_one(new_user)
        flash('Congratulations {} {}, you are now a registered user!'.format(form.firstname.data, form.lastname.data))
        return redirect(url_for('api.login'))
    return render_template('api/signup.html', title='Register', form=form)

# login page
@api.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('api.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.Users.find_one({'username':form.username.data})
        if user != None and User.checkPassword(user['pw'], form.pw.data):
            verify = User(user['username'],user['email'])
            login_user(verify)
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return redirect(url_for('api.home'))
        flash('Invalid Username or Password. Please try again.')
        return redirect(url_for('api.login'))
    return render_template('api/login.html', title='Login', form=form)

# logout
@api.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('api.login'))

# Error handling
@api.errorhandler(404)
def not_found_error(error):
    return render_template('api/404.html'), 404

# Internal handling
@api.errorhandler(500)
def internal_error(error):
    return render_template('api/500.html'), 500


# Request New Queue
@api.route('/newQueue', methods=['POST'])
@login_required
def createQueue():
    if request.method == 'POST':
        item = request.json
        print("++++++++++ Request Queue ++++++++++++ item: ", item)
        request_type = item['type']

        status = "success"
        message = "Your request is located in Queue"
        # Individual Game
        if request_type == 0:
            gmid = item['game']
            gpid = item['league']
            wager = item['wager']
            user = current_user.username
            state = "waiting"

            if player_queued.findPQMAP(gmid,gpid,wager,user,state):
                status = "failure"
                message = "You already request this GAME"
            else:
                player_queued.createPlayerQueued(gmid,gpid,wager,user,state)

                # check compatible candidate
                if player_queued.findCandidate(gmid,gpid,wager,user):
                    # Find candidate in Queued
                    candidate = player_queued.findCandidate(gmid,gpid,wager,user)

                    player1 = player_queued.getPQID(gmid,gpid,wager,user,state)
                    player1_index = player1
                    player2_index = candidate

                    update_state= "active"
                    
                    player_queued.updatePlayerQueued(player1_index,update_state)
                    player_queued.updatePlayerQueued(player2_index,update_state)

                    # Generate a new Queues 
                    match_queues.createMatchQueues(player1_index, player2_index, "Waiting")

                    status='success'
                    message='Congratulations! You are paired with compatible candidate!'

        return jsonify(status=status, message=message)

DEFAULT_RATING = 1500 
ELO_CONSTANT = 32

# Listener for reporting Match Result
@api.route('/reportusermatch', methods=['POST'])
@login_required
def report_user_match():
    if request.method == 'POST':
        item = request.json

        # create new static object
        new_item = {
            'id': str(uid()),
            'current':'pending',
            'user_id': current_user.get_id(),
            'create_time' : date.today().strftime('%Y/%m/%d'),
            'members' : [current_user.get_id()],
            'completed_time' : date.now(),
            'players' : 2,
            'cur_players' : 2
        }

        # append dic with form post
        size = len(item)
        while size >= 0:
            new_item[item[size-1]['name']] = item[size-1]['value']
            size -= 1

        # add to database
        db.UserMatches.insert_one(new_item)

        # Get specific field to calculate the ELO rating
        game = new_item['game']
        league = new_item['league']
        player_two = new_item['playertwo']
        winner = new_item['winner']

        # Get the Player1's ELO Rating
        player1_rating = get_player_rating(game, league, current_user.get_id())
        player2_rating = get_player_rating(game, league, player_two)

        # Calculate new Rating
        d = 1 if winner == current_user.get_id() else -1
        new_ratings = EloRatingCal(player1_rating, player2_rating, ELO_CONSTANT, d)

        # Get Elo Rating Index
        player1_index = elo_ratings.getERID(game, league, current_user.get_id())
        player2_index = elo_ratings.getERID(game, league, player_two)
        # Update the Rating
        elo_ratings.updateEloRating(player1_index, new_ratings[0])
        elo_ratings.updateEloRating(player2_index, new_ratings[1])

    return jsonify(success=1)
# End Report Match


# Get Elo Rating of player
def get_player_rating(game, league, player):
    if elo_ratings.findERMAP(game, league, player):
        rating_id = elo_ratings.getERID(game, league, player)
        rating = elo_ratings.getEloRating(rating_id)['rating']
    else:
        rating = DEFAULT_RATING
        elo_ratings.createEloRating(game,league, player, rating)
    
    return rating


@api.route('/leaderboards')
@login_required
def leaderboards():

    main_games = [
        { 'id':'cod', 'title':'cod'},
        { 'id':'lol', 'title':'lol'},
        { 'id':'dota', 'title':'dota'}
    ]

    return render_template('api/leaderboard.html', 
        title='Leaderboard',
        leagues=leagues,
        games=main_games
    )


@api.route('/searchelorating/', methods=['POST'])
@login_required
def search_elo_rating():
    if request.method == 'POST':
        result_data =[]
        item = request.json

        filter_data = elo_ratings.find_by_game_league(item['game'], item['group'])
        result_data = elo_ratings.sort_by_rating(filter_data)
        offset = item['offset']
        limit = item['limit']
        return jsonify(success=1, result=result_data[(offset-1)*limit:offset*limit])
    return jsonify(success=1,  message="received")


# Sponsorship, Template renderer with first 10 records
@api.route('/sponsorship/<user_id>', methods=['GET', 'POST'])
def sponsorship(user_id):
    """
    get view returns first 10 records with template renderer
    post view submits the sponsorship form submission
    """
    search = False
    PER_PAGE = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # get current user
    user = db.Users.find_one({'id': user_id})

    if user:
        # get the avatar for user
        avatar = user.get('avatar', '')
        # if avatar == "":
        #     avatar = avatar(user['email'], 128)

        # get cover photo of user
        cover = user.get('cover', '')

        # get first 10 matches of current user from db
        matches = db.UserMatches.find({'user_id': user_id}).skip((page - 1) * PER_PAGE).limit(PER_PAGE)
        matches_list = list(matches)

        pagination = Pagination(page=page,
                                per_page=PER_PAGE,
                                per_page_parameter=(((page - 1) * len(matches_list)) + PER_PAGE),
                                total=matches.count(), search=search, record_name='matches')

        # count wins and losses
        wins = db.UserMatches.count({'$and': [
            {'winner': user_id}, {'winner': {'$ne': None}}
        ]})
        losses = db.UserMatches.count({'winner': {'$ne': user_id}})

        # calculate prize of current user using pymongo aggregate method
        prize_pipeline = [{'$match': {'winner': user_id}}, {'$group': {'_id': None, 'total': {'$sum': 'your_wager'}}}]
        sum_prize = json_util.dumps(db.UserMatches.aggregate(pipeline=prize_pipeline))
        total_prize = 0
        if len(sum_prize) > 0:
            total_prize = json_util.loads(sum_prize)[0]['total']

        form = SponsorshipForm()

        # handle POST request
        if form.validate_on_submit():
            new_sponsorship = {
                'id': str(uid()),
                'user_id': user_id,
                'name': form.name.data,
                'email': form.email.data,
                'gender': form.gender.data,
                'card_number': form.card_number.data,
                'card_expiry_month': form.card_expiry_month.data,
                'card_expiry_year': form.card_expiry_year.data,
                'card_cvv': form.card_cvv.data,
                'message': form.message.data,
                'billing_address': form.billing_address.data,
                'zip': form.zip.data,
                'city': form.city.data,
                'state': form.state.data,
                'country': form.country.data,
                'amount': form.amount.data,
                'anonymous': form.anonymous.data,
                'every_month': form.every_month.data,
                'created_at': date.now()
            }
            db.Sponsorship.insert_one(new_sponsorship)
            # Process for Rabbitmq
            send_task('Create', new_sponsorship['id'], user_id)
            flash('Congratulations {}, you have contributed towards a success journey!'.format(form.name.data))

        return render_template('api/sponsorship.html', title='Sponsorship', form=form, user=user, matches=matches_list,
                               wins=wins, losses=losses, total_prize=total_prize, pagination=pagination, avatar=avatar,
                               cover=cover)
    else:
        # handle /favico request
        return jsonify({'none': 'none'})


# sponsorship, api which fetches next 10 records on each pagination call
@api.route('/sponsorship-infinite/<user_id>', methods=['GET'])
def sponsorship_infinite(user_id):
    PER_PAGE = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # get the next 10 records for matches
    matches = db.UserMatches.find({'user_id': user_id}).skip((page - 1) * PER_PAGE).limit(PER_PAGE)
    matches_list = list(matches)

    matches_str = json_util.dumps(matches_list)
    return jsonify(matches=json.loads(matches_str), page=page)

