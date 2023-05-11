# collection = db["test"]
# post = {"_id":1, "name":"jekoo", "score":100}
# collection.insert_one(post)
import pymongo
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
# from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = '1234'
cluster = MongoClient("mongodb+srv://wprn1116:Z3VuxQrupXHoeoCZ@cluster0.zsnpgns.mongodb.net/?retryWrites=true&w=majority")
db = cluster["software_engineering"]

# db.marketplace.insert_one({"id":0,"coins" : 100, "coin_price" : 100})

def get_user_money(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user["money"]

def update_user_money(user_id, new_money):
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"money": new_money}})

def get_user_coins(user_id):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user["coins"]

def update_user_coins(user_id, new_coins):
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"coins": new_coins}})

def get_marketplace_data():
    return db.marketplace.find_one()




@app.route('/')
def index():
    user = None
    if session.get('user_id'):
        user = db.users.find_one({"_id": ObjectId(session.get('user_id'))})
    
    marketplace_data = db.marketplace.find_one()
    sell_posts = list(db.sell_posts.find())
    sell_posts_with_usernames = []

    for post in sell_posts:
        post_owner = db.users.find_one({"_id": post["user_id"]})
        sell_posts_with_usernames.append({
            "_id": post["_id"],
            "username": post_owner["username"],
            "coins_to_sell": post["coins_to_sell"],
            "selling_price": post["selling_price"]
        })

    return render_template('index.html', user=user, marketplace_data=marketplace_data, sell_posts=sell_posts_with_usernames)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.users.find_one({"username": username}):
            flash("Username already exists.")
        else:
            db.users.insert_one({"username": username, "password": password, "money": 0, "coins": 0})
            flash("Account created successfully!")
            return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({"username": username, "password": password})
        if user:
            session['user_id'] = str(user['_id'])
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Incorrect username or password.")
    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/buy_coins', methods=['POST'])
def buy_coins():
    coins_to_buy = int(request.form['coins_to_buy'])
    user_id = session.get('user_id')
    money = get_user_money(user_id)
    marketplace_data = get_marketplace_data()

    if marketplace_data["coins"] >= coins_to_buy:
        cost = coins_to_buy * marketplace_data["coin_price"]
        if money >= cost:
            new_money = money - cost
            update_user_money(user_id, new_money)

            user_coins = get_user_coins(user_id)
            new_coins = user_coins + coins_to_buy
            update_user_coins(user_id, new_coins)

            new_marketplace_coins = marketplace_data["coins"] - coins_to_buy
            db.marketplace.update_one({}, {"$set": {"coins": new_marketplace_coins}})

            flash("Coins purchased successfully!")
        else:
            flash("Not enough money to buy the coins.")
    else:
        flash("Not enough coins available in the marketplace.")

    return redirect(url_for('index'))

@app.route('/sell_coins', methods=['POST'])
def sell_coins():
    coins_to_sell = int(request.form['coins_to_sell'])
    selling_price = int(request.form['selling_price'])
    user_id = session.get('user_id')
    user_coins = get_user_coins(user_id)

    if user_coins >= coins_to_sell:
        sell_post = {
            "user_id": user_id,
            "coins_to_sell": coins_to_sell,
            "selling_price": selling_price
        }
        db.sell_posts.insert_one(sell_post)
        flash("Sell post created successfully!")
    else:
        flash("Not enough coins to sell.")

    return redirect(url_for('index'))

@app.route('/add_money', methods=['POST'])
def add_money():
    amount_to_add = int(request.form['amount_to_add'])
    user_id = session.get('user_id')
    money = get_user_money(user_id)
    new_money = money + amount_to_add
    update_user_money(user_id, new_money)
    flash("Money added successfully!")
    return redirect(url_for('index'))

@app.route('/withdraw_money', methods=['POST'])
def withdraw_money():
    amount_to_withdraw = int(request.form['amount_to_withdraw'])
    user_id = session.get('user_id')
    money = get_user_money(user_id)

    if money >= amount_to_withdraw:
        new_money = money - amount_to_withdraw
        update_user_money(user_id, new_money)
        flash("Money withdrawn successfully!")
    else:
        flash("Not enough money to withdraw.")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
