from flask import flash, session, jsonify,Response, abort
from flask import render_template
from flask import  request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm, CraftingForm,CraftDataForm,SearchForm
from . import admin_bp
from .data import Admin
from ..decorator import permission_required
from .admin import db
from werkzeug.utils import secure_filename
import json,os
from .config import SUPER_SECRET_KEY
# signup page

NAMES = ['Weapon','Armor','Tools','Trinket','Jewelry','Food','Charms','Building','Clothing','Electronics',
         'Watches','Toys','Giftcards','Furniture','Fighting','Racing','Sports','RPG','FPS','Random','Gems','Chests']
upload_to = os.path.join(os.path.dirname(__file__),"static")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@admin_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Create new admin user """
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = {
            'uid': Admin.setUID(),
            'id': form.username.data,
            'email': form.email.data,
            'username': form.username.data,
            'pw': Admin.setHash(form.pw.data),
            'has_perm': form.has_perm.data
        }
        db.Admins.insert_one(new_user)
        flash('Congratulations {}, you are now a registered admin!'.format(form.username.data))
        return redirect(url_for('admin.login'))
    return render_template('admin/signup.html', title='Register', form=form)


# login page

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Admin User login"""
    form = LoginForm()
    if form.validate_on_submit():
        user = db.Admins.find_one({'username': form.username.data})
        if user != None and Admin.checkPassword(user['pw'], form.pw.data):
            verify = Admin(user['username'])
            login_user(verify)
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            return render_template('admin/index.html')
            # return redirect(url_for('admin.home'))
        flash('Invalid Username or Password. Please try again.')
        return redirect(url_for('admin.login'))
    return render_template('admin/signin.html', title='Login', form=form)



#crafting
@admin_bp.route('/add_craft', methods=['GET', 'POST'])
def craft():
    try:
        form = CraftingForm(request.form)
        if form.validate():
            product_NAME = form.product_name.data
            list= []
            for i in db.Recipe.find():
                for j in i:
                    if j == "_id" or j == "recipe_name":
                        continue
                    else:
                        if i[j] == product_NAME:
                            list.append(i["recipe_name"])
                            continue
                        else:
                            continue

            if not list :
                recipe_ref =None
            else:
                recipe_ref = list

            filename =""
            craft_name= form.craft_name.data
            if 'product_image' not in request.files:
                error= 'No file part'
                return Response(json.dumps({"error": error}), status=400)
            file = request.files['product_image']

            if file.filename == '':
                error = 'No selected file'
                return Response(json.dumps({"error": error}), status=400)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(upload_to, filename))
            if craft_name != None or craft_name != "":
                if craft_name in NAMES:
                    add_item = {
                        '_id': db.Craft.find().count() + 1,
                        'product_img': filename,
                        'product_name':form.product_name.data,
                        'recipe':recipe_ref,
                        'possible_amount':form.possible_amount.data,
                        'amount_awarded':form.amount_awarded.data,
                        'per_of_dropRate':form.per_of_dropRate.data,
                        'value':form.value.data,
                        'craft_name':form.craft_name.data
                    }
                    db.Craft.insert_one(add_item)
                    craft_data = db.Craft.find().sort( [("_id", -1)] ).limit(1)
                    get_data_item = ""
                    for i in craft_data:
                        get_data_item = {
                            'product_img': i["product_img"],
                            'product_name': i["product_name"],
                            'recipe': i["recipe"],
                            'possible_amount': i["possible_amount"],
                            'amount_awarded': i["amount_awarded"],
                            'per_of_dropRate': i["per_of_dropRate"],
                            'value': i["value"],
                            'craft_name': i["craft_name"]
                            }
                    return jsonify(get_data_item)
                else:
                    error = "craft name should be in {}".format(NAMES)
                    return Response(json.dumps({"error":error}), status=400)
            else:
                error ="you have to enter craft name!!!!!!!!!"
                return Response(json.dumps({"error": error}), status=400)
        else:
            return Response(json.dumps({"error": form.errors}), status=400)
    except Exception as e:
        return e




@admin_bp.route('/crafting', methods=['GET', 'POST'])
def crafting():
    form = CraftDataForm(request.form)
    if form.validate():
        craft_name = form.craft_name.data
        if craft_name in NAMES:
            counter = 1
            get_data_item = {}
            for i in db.Craft.find({"craft_name":craft_name}):
                get_data_item["data {}".format(counter)] = {
                    'product_img': i["product_img"],
                    'product_name': i["product_name"],
                    'recipe': i["recipe"],
                    'possible_amount': i["possible_amount"],
                    'amount_awarded': i["amount_awarded"],
                    'per_of_dropRate': i["per_of_dropRate"],
                    'value': i["value"],
                    'craft_name': i["craft_name"]
                }
                counter += 1
            return jsonify(get_data_item)

        elif craft_name == 'all':
            counter = 1
            get_data_item = {}
            for i in db.Craft.find():

                get_data_item["data {}".format(counter)] = {
                    'product_img': i["product_img"],
                    'product_name': i["product_name"],
                    'recipe': i["recipe"],
                    'possible_amount': i["possible_amount"],
                    'amount_awarded': i["amount_awarded"],
                    'per_of_dropRate': i["per_of_dropRate"],
                    'value': i["value"],
                    'craft_name': i["craft_name"]
                }
                counter += 1
            return jsonify(get_data_item)
        else:
            error = "craft name should be 'all' or  in {}".format(NAMES)
            return Response(json.dumps(error), status=400)
    else:

        return Response(json.dumps(form.errors),status=400)



@admin_bp.route('/total_craft', methods=['GET', 'POST'])
def total_craft():
    #Getting values of all tables
    try:
        craft_value = []
        for i in db.Craft.find():
            craft_value.append(int(i["value"]))
        craft_Sum = sum(craft_value)

    #######Getting awarded amount of all tables

        craft_award = []
        for i in db.Craft.find():
            craft_award.append(int(i["amount_awarded"]))
        craft_awardSum = sum(craft_award)

    ###########Getting total items

        craft_items = []
        for i in db.Craft.find():
            craft_items.append(i)
        craft_itemslen = len(craft_items)

        return jsonify({"total_value":craft_Sum,"total_amount_awarded":craft_awardSum,"total_items":craft_itemslen})

    except Exception as e:
        return Response(json.dumps(e),status=400)

@admin_bp.route('/add_recipe', methods=['GET', 'POST'])
def recipe():
    data = [{k:request.form[k]} for k in request.form]
    rcp_name = {}
    for i in range(len(data)):
        if 'recipe_name' in data[i]:
            recipe_name = db.Recipe.find_one({'recipe_name': data[i]['recipe_name']})
            if recipe_name:
                return Response(json.dumps("recipe name already exists, Try another one!!!!"),status=400)
            else:
                rcp_name = data[i]
        elif list(data[i].keys())[0] in NAMES:
            continue
        else:
            return Response(json.dumps("Invalid key/value of, key should be in {} ".format(NAMES)), status=400)

    if rcp_name['recipe_name'] != None or rcp_name['recipe_name'] != "" :
        add_item = {
            '_id': db.Recipe.find().count() + 1,
            'recipe_name': rcp_name['recipe_name'],
        }
        for i in range(len(data)):
            if list(data[i].keys())[0] == 'recipe_name':
                continue
            else:
                add_item[list(data[i].keys())[0]] = data[i][list(data[i].keys())[0]]

        db.Recipe.insert_one(add_item)

        recipe_data = db.Recipe.find().sort([("_id", -1)]).limit(1)
        get_data_item = ""

        for i in recipe_data:
            return jsonify(i)
    else:
        error = "recipe name already exists, Try another one!!!!"
        return Response(json.dumps({"error":error}), status=400)



@admin_bp.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm(request.form)
    if form.validate():
        key = form.search.data

        data = db.Craft.find({"product_name":key})
        if data.count() != 0:
            counter = 1
            get_data_item = {}
            for i in data:
                get_data_item["data {}".format(counter)] = {
                    'product_img': i["product_img"],
                    'product_name': i["product_name"],
                    'recipe': i["recipe"],
                    'possible_amount': i["possible_amount"],
                    'amount_awarded': i["amount_awarded"],
                    'per_of_dropRate': i["per_of_dropRate"],
                    'value': i["value"],
                    'craft_name': i["craft_name"]
                }
                counter += 1
            return jsonify(get_data_item)
        else:
            error="not found"
            return Response(json.dumps({"error":error}), status=400)

# logout
@admin_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('admin.login'))


# Home
@admin_bp.route('/', methods=['GET', 'POST'])
@permission_required(perms_list=["admin-level1"])
def home():
    return render_template('admin/index.html')


# Examples
"""
You should remove these examples
"""
# Test1
@admin_bp.route('/test1/', methods=['GET', 'POST'])
@permission_required(perms_list=["admin-level1","admin-level2","admin-level3","admin-level4","admin-level5"])
def test1():
    return jsonify(Page="Test1 for permission level 1,2,3,4,5")


# Test2
@admin_bp.route('/test2/', methods=['GET', 'POST'])
@permission_required(perms_list=["admin-level2"])
def test2():
    return jsonify(Page="Test2 for permission level 2")


# Test3
@admin_bp.route('/test3/', methods=['GET', 'POST'])
@permission_required(perms_list=["admin-level2,admin-level3,admin-level4"])
def test3():
    return jsonify(Page="Test3 for permission level 2,3,4")

# End of examples

# Error handling
@admin_bp.errorhandler(404)
def not_found_error(error):
    return render_template('admin/404.html'), 404


# Internal handling
@admin_bp.errorhandler(500)
def internal_error(error):
    return render_template('admin/500.html'), 500
