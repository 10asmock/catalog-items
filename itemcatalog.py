from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import User, Category, CatalogItem, Base

app = Flask(__name__)

engine = create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#NEEDS TO BE FIXED. It appears Category didn't take any of the items into the list.
@app.route('/categories/JSON')
def showcategoriesJSON():
    category = session.query(Category).all()
    return jsonify(Category = [i.serialize for i in category])


#NEEDS TO BE FIXED. It appears CatalogItem didn't take any of the items into the list.
@app.route('/categories/<int:category_id>/items/JSON')
def showCatalogJSON(category_id):
    category = session.query(Category).filter_by(id = category_id)
    items = session.query(CatalogItem).filter_by(category_id=category_id)
    return jsonify(CatalogItem = [i.serialize for i in items])


#NEEDS TO BE FIXED.
@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def catalogItemJSON(category_id, item_id):
    catalogItem = session.query(CatalogItem).filter_by(id = item_id).one()
    return jsonify(catalogItem = catalogItem.serialize)


#NEEDS TO BE FIXED.
@app.route('/')
@app.route('/categories/', methods=['GET','POST'])
def showCategories():
    category = session.query(Category).all()
    return render_template('categories.html', category = category)


#COMPLETED!
@app.route('/categories/new/', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(name = request.form['name'])
            session.add(newCategory)
            session.commit()
            flash("New category created!")
            return redirect(url_for('showCategories', category = newCategory))
    else:
            return render_template('newCategory.html', category = id)


#COMPLETED!
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        session.add(editedCategory)
        session.commit()
        flash("Category has been edited!")
        return redirect(url_for('showCategories', category_id = category_id))
    else:
        return render_template('editCategory.html', category_id = category_id, category = editedCategory)
    #return "This page will be for editing restaurant %s." % restaurants_id


#CRUD WORKS, NEED TO FIX FLASH
@app.route('/categories/<int:category_id>/delete/',
            methods = ['GET','POST'])
def deleteCategory(category_id):
    deletedCategory = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(deletedCategory)
        session.commit()
        flash("Category has been deleted!")
        return redirect(url_for('showCategories', category = category_id))
    else:
        return render_template('deleteCategory.html', category = deletedCategory)
    #return "This page will be for deleting restaurant %s." % restaurant_id


#NEEDS TO BE FIXED.
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/', methods = ['GET','POST'])
def showCatalogItems(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(CatalogItem).filter_by(category_id=category_id)
    return render_template('catalog.html', category = category, items = items, category_id = category_id)
    #return "This page is the menu for restaurant %s." % restaurant_id


#NEEDS TO BE FIXED.
@app.route('/catagories/<int:category_id>/items/new/',
            methods = ['GET','POST'])
def newCatalogItem(category_id):
    if request.method == 'POST':
        if request.form["name"]:
            newCatalogItem = CatalogItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], category_id = category_id)
        session.add(newCatalogItem)
        session.commit()
        flash("Catalog item has been created!")
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('newcatalogitem.html', category_id = category_id)
    #return "This page is for making a new menu item for restaurant %s." % restaurant_id


#NEEDS TO BE FIXED.
@app.route('/categories/<int:catagory_id>/items/<int:item_id>/edit/',
            methods = ['GET','POST'])
def editCatalogItem(category_id, item_id):
    editedCatalogItem = session.query(CatalogItem).filter_by(id = catalog_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedCatalogItem)
        session.commit()
        flash("Catalog item has been edited!")
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('editcatalogitem.html', category_id=category_id, item_id = item_id, item = editedCatalogItem)
    #return "This page is for editing menu item %s." % menu_id


#NEEDS TO BE FIXED.
@app.route('/categories/<int:catagory_id>/items/<int:item_id>/delete/',
            methods = ['GET','POST'])
def deleteCatalogItem(category_id, item_id):
    deletedCatalogItem = session.query(CatalogItem).filter_by(id = catalog_id).one()
    if request.method == 'POST':
        session.delete(deletedCatalogItem)
        session.commit()
        flash("Catalog item has been deleted!")
        return redirect(url_for('showCatalogItems', category_id = category_id))
    else:
        return render_template('deletecatalogitem.html', items = deletedCatalogItem)
    #return "This page is for deleting menu item %s." % restaurant_id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
