'''
Created on 14/01/2016

Controller for the catalog server containing helper functions and rest API to perform CRUD operations
on the composer database. Route to the app index is forwarded to angular.js framework routing.

@author: Jessica
'''

import os
import json

from flask import send_file, jsonify, request
from catalog import app, client_path
from catalog.authentication.controllers import login_required, getUser
from catalog.models import Composer, MusicItem, MusicFile
from catalog.core import db
from werkzeug import secure_filename

#Helper functions
def createMusicFile(musicItem, filename):
    musicFile = MusicFile(path=filename)
    musicFile.music_item = musicItem
    db.session.add(musicFile)
    db.session.commit()
    
def createMusicItem(user_id, name, number, key, dateOfComposition, dateAdded, composer):
    musicItem = MusicItem(user_id=user_id, name=name, number=number, key=key, dateOfComposition=dateOfComposition, dateAdded=dateAdded)
    musicItem.composer = composer
    db.session.add(musicItem)
    db.session.commit()
    return musicItem

def uploadFileToServer(uploadFile, musicItem):
    filename = secure_filename(uploadFile.filename)
    uploadFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

#API Routes
@app.route('/')
def index():
    #forward to angular routing
    return send_file(os.path.join(client_path, 'index.html'))


@app.route('/api/catalog/uploadfile', methods=['POST'])
@login_required
def uploadFileToMusicItem():
    uploadFile = request.files['file']
    
    if uploadFile:
        
        musicItem = MusicItem.query.filter_by(id=request.form['id']).first()
        
        if not musicItem:
            response = jsonify(message="Couldn't find music item")
            response.status_code = 401
            return response
         
        filename = uploadFileToServer(uploadFile, musicItem)
        createMusicFile(musicItem, filename)
        
        response = jsonify(message="File has been saved %s"% filename)
        response.status_code = 200
        return response
         
    response = jsonify(message="File could not be saved")
    response.status_code = 500
    return response

'''
Return composer data in JSON format for the current logged in user
'''
@app.route('/api/catalog/composers/JSON')
@login_required
def allComposersJSON():
    user = getUser()
    composers = Composer.query.filter_by(user_id=user.id).order_by(Composer.name).all()
    return jsonify(composers=[c.to_json() for c in composers])

'''
Return music item data for a particular composer in JSON format for the current logged in user
'''
@app.route('/api/catalog/composer/<int:composer_id>/musicitems/JSON')
@login_required
def composerMusicItemsJSON(composer_id):
    user = getUser()
    composer = Composer.query.filter_by(id=composer_id, user_id=user.id).first()
    return jsonify(musicItems=[i.to_json() for i in composer.musicItems])

'''
Update a composer, passing in JSON parameters containing the new model
'''
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

'''
Update a music item, passing in JSON parameters containing the new model
'''
@app.route('/api/catalog/updatemusicitem', methods=['POST'])
@login_required
def updateMusicItem():
    musicItem = MusicItem.query.filter_by(id=request.json['id']).first()
 
    if not musicItem:
        response = jsonify(message="Couldn't find music item")
        response.status_code = 401
        return response
     
    musicItem.name = request.json['name']
    musicItem.dateAdded = request.json['dateAdded']
    musicItem.dateOfComposition = request.json['dateOfComposition']
    musicItem.number = request.json['number'] 
    musicItem.key = request.json['key']
    db.session.commit()

    response = jsonify(message="Music item %s updated"% musicItem.name)
    response.status_code = 200
    return response

'''
Add a composer, passing in JSON parameters containing the new model
'''
@app.route('/api/catalog/addcomposer', methods=['POST'])
@login_required
def addComposer():
    user = getUser()
    composer = Composer(user_id=user.id, name=request.json['name'], dateOfBirth=request.json['dateOfBirth'], dateOfDeath=request.json['dateOfDeath'])
    db.session.add(composer)
    db.session.commit()
   
    response = jsonify(message="Added composer %s"%composer.name)
    response.status_code = 200
    return response

'''
Add a music item, passing in JSON parameters containing the new model
'''
@app.route('/api/catalog/addmusicitem', methods=['POST'])
@login_required
def addMusicItem():
    
    user = getUser()
    composer_id = request.form['composer_id']
    musicItemData = json.loads(request.form['music_item'])
    
    composer = Composer.query.filter_by(id=composer_id, user_id=user.id).first()
    
    if not composer:
        response = jsonify(message="Couldn't find composer")
        response.status_code = 401
        return response
    
    musicItem = createMusicItem(user_id=user.id, name=musicItemData['name'], number=musicItemData['number'], key=musicItemData['key'], dateOfComposition=musicItemData['dateOfComposition'], dateAdded=musicItemData['dateAdded'], composer=composer)
  
    if 'file' in request.files:
        uploadFile = request.files['file']
        filepath = uploadFileToServer(uploadFile, musicItem)
        createMusicFile(musicItem, filepath)
        print "uploading a file"
    else:
        print "no file to upload"

    response = jsonify(message="Added music item %s"%musicItem.name)
    response.status_code = 200
    return response

'''
Delete a composer, passing in JSON parameters containing the id
'''
@app.route('/api/catalog/deletecomposer', methods=['POST'])
@login_required
def deleteComposer():
    composer = Composer.query.filter_by(id=request.json['id']).first()

    if not composer:
        response = jsonify(message="Couldn't find composer")
        response.status_code = 401
        return response
    
    db.session.delete(composer)
    db.session.commit()
   
    response = jsonify(message="Deleted composer %s"%composer.name)
    response.status_code = 200
    return response

'''
Delete a music item, passing in JSON parameters containing the id
'''
@app.route('/api/catalog/deletemusicitem', methods=['POST'])
@login_required
def deleteMusicItem():
    musicItem = MusicItem.query.filter_by(id=request.json['id']).first()

    if not musicItem:
        response = jsonify(message="Couldn't find music item")
        response.status_code = 401
        return response
    
    db.session.delete(musicItem)
    db.session.commit()
   
    response = jsonify(message="Deleted music item %s"%musicItem.name)
    response.status_code = 200
    return response

'''
Delete a music file, passing in JSON parameters containing the id
'''
@app.route('/api/catalog/deletemusicfile', methods=['POST'])
@login_required
def deleteMusicFile():
    musicFile = MusicFile.query.filter_by(id=request.json['id']).first()

    if not musicFile:
        response = jsonify(message="Couldn't find music file")
        response.status_code = 401
        return response

    db.session.delete(musicFile)
    db.session.commit()
   
    response = jsonify(message="Deleted music file %s"%musicFile.path)
    response.status_code = 200
    return response


    
