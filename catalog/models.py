'''
Created on 14/01/2016

@author: Jessica
'''
from catalog.core import db
import datetime

class Composer(db.Model): 
    __tablename__ = "composer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    dateOfBirth = db.Column(db.Date, nullable=False)
    dateOfDeath = db.Column(db.Date)
    musicItems = db.relationship("MusicItem")
    
    def to_json(self):
        
        if self.dateOfDeath is None:
            deathDate = "";
        else:
            deathDate = self.dateOfDeath.isoformat()
             
        return dict(id=self.id, name=self.name, dateOfBirth=self.dateOfBirth.isoformat(),
                    dateOfDeath=deathDate)
   
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
    
    def to_json(self):
        return dict(id=self.id, path=self.path)
    
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
    
    def to_json(self):
        
        if self.dateAdded is None:
            dateAdded = "";
        else:
            dateAdded = self.dateAdded.isoformat()
            
        if self.dateOfComposition is None:
            dateOfComposition = "";
        else:
            dateOfComposition = self.dateAdded.isoformat()
        
        return dict(id=self.id, name=self.name, number=self.number,
                    key=self.key, dateAdded=dateAdded, dateOfComposition=dateOfComposition,
                    files=[f.to_json() for f in self.files])
    

