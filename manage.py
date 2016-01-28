from catalog import app
from catalog.models import db, MusicItem, Composer, Instrument, MusicFile
import datetime

    
'''Seed the database with test data'''
def setUp(self):
 
    #create the composers
    today = datetime.date.today()
    composer1 = Composer(name="Chopin", dateOfBirth=today, dateOfDeath=today)
    composer2 = Composer(name="Rachmaninoff", dateOfBirth=today, dateOfDeath=today)
    composer3 = Composer(name="Prokovief", dateOfBirth=today, dateOfDeath=today)
    composer4 = Composer(name="Schubert", dateOfBirth=today, dateOfDeath=today)
    composer5 = Composer(name="Glass", dateOfBirth=today)
     
    db.session.add(composer1)
    db.session.add(composer2)
    db.session.add(composer3)
    db.session.add(composer4)
    db.session.add(composer5)
    db.session.commit()
 
    #create file objects where music item files will be stored
    file1 = MusicFile(path="http://fileserver/nocturneop2no3.pdf")
    file2 = MusicFile(path="http://fileserver/nocturneop2no4.pdf")
    file3 = MusicFile(path="http://fileserver/triopg1.jpg")
    file4 = MusicFile(path="http://fileserver/triopg2.jpg")
    file5 = MusicFile(path="http://fileserver/triopg3.jpg")
    
    db.session.add(file1)
    db.session.add(file2)
    db.session.add(file3)
    db.session.add(file4)
    db.session.add(file5)
    db.session.commit()
 
    #create each music item
    musicitem1 = MusicItem(name='Nocturne', number='Op. 2, no. 3', key='C minor', composer=composer1)
    musicitem2 = MusicItem(name='Nocturne', number='Op. 2, no. 4', key='C major', composer=composer1)
    musicitem3 = MusicItem(name='Piano Trio', number='Op. 62, no. 1', key='D major', composer=composer2)
 
    #add instruments to the database
    instrument1 = Instrument(name='Piano')
    instrument2 = Instrument(name='Violin')
    instrument3 = Instrument(name='Cello')
 
    db.session.add(instrument1)
    db.session.add(instrument2)
    db.session.add(instrument3)
    db.session.commit()
     
    #add the required intruments and files to each music item
    musicitem1.instruments.append(instrument1)
    musicitem2.instruments.append(instrument1)
    musicitem3.instruments.append(instrument1)
    musicitem3.instruments.append(instrument2)
    musicitem3.instruments.append(instrument3)
     
    db.session.add(musicitem1)
    db.session.add(musicitem2)
    db.session.add(musicitem3)
    db.session.commit()
 
    musicitem1.files.append(file1)
    musicitem2.files.append(file2)
    musicitem3.files.append(file3)
    musicitem3.files.append(file4)
    musicitem3.files.append(file5)
    db.session.commit()

    
if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        setUp(db)
        
        #List all music items belonging to each composer
        query = db.session.query(Composer)
        for c in query:
            for m in c.musicItems:
                print "%s composed %s %s in the key of %s" % (c.name, m.name, m.number, m.key)

        #List all files belonging to each music item
        query = db.session.query(MusicItem)
        for m in query:
            for f in m.files:
                print "%s is associated with %s" % (m.name, f.path)
