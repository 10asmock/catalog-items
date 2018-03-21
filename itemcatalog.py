from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;' \
              'height: 300px;' \
              'border-radius: 150px;' \
              '-webkit-border-radius: 150px;' \
              '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/categories/JSON')
def showcategoriesJSON():
    category = session.query(Category).all()
    return jsonify(Category = [i.serialize for i in category])


@app.route('/categories/<int:category_id>/items/JSON')
def showCatalogJSON(category_id):
    category = session.query(Category).filter_by(id = category_id)
    items = session.query(CatalogItem).filter_by(category_id=category_id)
    return jsonify(CatalogItem = [i.serialize for i in items])


@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def catalogItemJSON(category_id, item_id):
    catalogItem = session.query(CatalogItem).filter_by(id = item_id).one()
    return jsonify(catalogItem = catalogItem.serialize)


# Show all categories
@app.route('/')
@app.route('/categories/', methods=['GET','POST'])
def showCategories():
    category = session.query(Category).all()
    return render_template('categories.html', category = category)


# Create a new category
@app.route('/categories/new/', methods=['GET','POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name = request.form['name'],
            user_id=login_session['user_id'])
            session.add(newCategory)
            session.commit()
            return redirect(url_for('showCategories', category = newCategory))
    else:
            return render_template('newCategory.html', category = id)


# Edit an existing category
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        return redirect(url_for('showCategories', category_id = category_id))
    else:
        return render_template('editCategory.html', category_id = category_id,
                               category = editedCategory)


# Delete an existing category
@app.route('/categories/<int:category_id>/delete/',
            methods = ['GET','POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedCategory = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        return redirect(url_for('showCatalogItems'))
    else:
        return render_template('deleteCategory.html', category_id = category_id, category = deletedCategory)


# Show all catalog items for a specific category
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items', methods = ['GET','POST'])
def showCatalogItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category_id).all()
    return render_template('catalog.html', category = category, items = items)


# Create a new catalog item for a specific category
@app.route('/categories/<int:category_id>/items/new',
            methods = ['GET','POST'])
def newCatalogItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCatalogItem = CatalogItem(name=request.form['name'], description=request.form['description'],
        price=request.form['price'], category_id=category_id)
        session.add(newCatalogItem)
        session.commit()
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('newcatalogitem.html', category_id = category_id)

# Edit a catalog item for a specific category
@app.route('/categories/<int:category_id>/items/<int:item_id>/edit/',
            methods = ['GET','POST'])
def editCatalogItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCatalogItem = session.query(CatalogItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form["name"]:
            editedCatalogItem.name = request.form["name"]
        if request.form["price"]:
            editedCatalogItem.price = request.form["price"]
        if request.form["description"]:
            editedCatalogItem.description = request.form["description"]
        session.add(editedCatalogItem)
        session.commit()
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('editcatalogitem.html', category_id=category_id, item_id = item_id, item = editedCatalogItem)


# Delete a catelog item of a specific category
@app.route('/categories/<int:category_id>/items/<int:item_id>/delete/',
            methods = ['GET','POST'])
def deleteCatalogItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedCatalogItem = session.query(CatalogItem).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(deletedCatalogItem)
        session.commit()
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('deletecatalogitem.html', items = deletedCatalogItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
