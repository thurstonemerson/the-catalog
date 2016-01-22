import os

from flask import send_file, jsonify, request
from catalog import app, client_path
from catalog.authentication.controllers import login_required
from catalog.models import Composer
from catalog.core import db

# Route
@app.route('/')
def index():
    return send_file(os.path.join(client_path, 'index.html'))

@app.route('/api/catalog/composers/JSON')
@login_required
def allComposersJSON():
    composers = Composer.query.all()
    return jsonify(composers=[c.to_json() for c in composers])


@app.route('/api/catalog/<int:composer_id>/JSON')
@login_required
def composerJSON(composer_id):
    composer = Composer.query.filter_by(id=composer_id).first()
    return jsonify(composer.to_json())

@app.route('/api/catalog/<int:composer_id>/musicitems/JSON')
@login_required
def composerMusicItemsJSON(composer_id):
    composer = Composer.query.filter_by(id=composer_id).first()
    return jsonify(musicItems=[i.to_json() for i in composer.musicItems])

@app.route('/api/catalog/updatecomposer', methods=['POST'])
@login_required
def updateComposer():
    composer = Composer.query.filter_by(id=request.json['id']).first()

    if not composer:
        response = jsonify(message="Couldn't find composer")
        response.status_code = 401
        return response
    
    composer.name = request.json['name']
    composer.dateOfBirth = request.json['dateOfBirth']
    composer.dateOfDeath = request.json['dateOfDeath']
    db.session.commit()
    
    response = jsonify(message="Composer %s updated"%composer.name)
    response.status_code = 200
    return response
        
#     user = User(email=request.json['email'], password=request.json['password'])
#     db.session.add(user)
#     db.session.commit()
#     token = create_token(user)
#     return jsonify(token=token)

#JSON APIs to view catalog information
# @app.route('/restaurant/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#      restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#      items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
#      return jsonify(MenuItems=[i.serialize for i in items])
 
 
# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
# def menuItemJSON(restaurant_id, menu_id):
#     Menu_Item = session.query(MenuItem).filter_by(id = menu_id).one()
#     return jsonify(Menu_Item = Menu_Item.serialize)
# 
# @app.route('/restaurant/JSON')
# def restaurantsJSON():
#     restaurants = session.query(Restaurant).all()
#     return jsonify(restaurants= [r.serialize for r in restaurants])


# #Show all restaurants
# @app.route('/')
# @app.route('/restaurant/')
# def showRestaurants():
#     restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
#     
#     return render_template('restaurants.html', restaurants = restaurants)
# 
# #Create a new restaurant
# @app.route('/restaurant/new/', methods=['GET','POST'])
# def newRestaurant():
#     if request.method == 'POST':
#         newRestaurant = Restaurant(name = request.form['name'])
#         session.add(newRestaurant)
#         flash('New Restaurant %s Successfully Created' % newRestaurant.name)
#         session.commit()
#         return redirect(url_for('showRestaurants'))
#     else:
#         return render_template('newRestaurant.html')
# 
# #Edit a restaurant
# @app.route('/restaurant/<int:restaurant_id>/edit/', methods = ['GET', 'POST'])
# def editRestaurant(restaurant_id):
#     editedRestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedRestaurant.name = request.form['name']
#             flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
#             return redirect(url_for('showRestaurants'))
#         else:
#             return render_template('editRestaurant.html', restaurant = editedRestaurant)
# 
# 
# #Delete a restaurant
# @app.route('/restaurant/<int:restaurant_id>/delete/', methods = ['GET','POST'])
# def deleteRestaurant(restaurant_id):
#     restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     if request.method == 'POST':
#         session.delete(restaurantToDelete)
#         flash('%s Successfully Deleted' % restaurantToDelete.name)
#         session.commit()
#         return redirect(url_for('showRestaurants', restaurant_id = restaurant_id))
#     else:
#         return render_template('deleteRestaurant.html',restaurant = restaurantToDelete)
# 
# #Show a restaurant menu
# @app.route('/restaurant/<int:restaurant_id>/')
# @app.route('/restaurant/<int:restaurant_id>/menu/')
# def showMenu(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     creator = getUserInfo(restaurant.user_id)
#     items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
#     return render_template('menu.html', items = items, restaurant = restaurant, creator=creator)
#      
# 
# 
# #Create a new menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
# def newMenuItem(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     if request.method == 'POST':
#         newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
#         session.add(newItem)
#         session.commit()
#         flash('New Menu %s Item Successfully Created' % (newItem.name))
#         return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#     else:
#         return render_template('newmenuitem.html', restaurant_id = restaurant_id)
# 
# #Edit a menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
# def editMenuItem(restaurant_id, menu_id):
# 
#     editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         if request.form['description']:
#             editedItem.description = request.form['description']
#         if request.form['price']:
#             editedItem.price = request.form['price']
#         if request.form['course']:
#             editedItem.course = request.form['course']
#         session.add(editedItem)
#         session.commit() 
#         flash('Menu Item Successfully Edited')
#         return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#     else:
#         return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
# 
# 
# #Delete a menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
# def deleteMenuItem(restaurant_id,menu_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one() 
#     if request.method == 'POST':
#         session.delete(itemToDelete)
#         session.commit()
#         flash('Menu Item Successfully Deleted')
#         return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#     else:
#         return render_template('deleteMenuItem.html', item = itemToDelete)




    
