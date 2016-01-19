'''
Created on 14/01/2016

@author: Jessica
'''
from catalog.core import db
from catalog import app
import datetime

class Composer(db.Model): 
    __tablename__ = "composer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    dateOfDeath = db.Column(db.Date, nullable=False)
   
class Instrument(db.Model): 
    __tablename__ = "instrument"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

class MusicFile(db.Model): 
    __tablename__ = "music_file"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), nullable=False)
    musicitem_id = db.Column(db.Integer, db.ForeignKey('music_item.id'))
    music_item = db.relationship("MusicItem")
    
musicitem_instruments = db.Table('musicitem_instruments', 
    db.Column('musicitem_id', db.Integer, db.ForeignKey('music_item.id')),
    db.Column('instrument_id', db.Integer, db.ForeignKey('instrument.id')))

class MusicItem(db.Model): 
    __tablename__ = "music_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    number = db.Column(db.String(120))
    key = db.Column(db.String(50))
    dateAdded = db.Column(db.Date, default=datetime.date.today())
    dateOfComposition = db.Column(db.Date)
    composer_id = db.Column(db.Integer, db.ForeignKey('composer.id'))
    composer = db.relationship(Composer)
    instruments = db.relationship(Instrument, secondary=musicitem_instruments)
    files = db.relationship(MusicFile)
    
    


# models for which we want to create API endpoints
app.config['API_MODELS'] = {'catalog': MusicItem}

