from flask import Flask, render_template, redirect, url_for
import pymongo
from scrape_mars import scrape

app = Flask(__name__)
#connect to mongo database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.mars_database
collection = db.mars_collection
posts = db.posts

@app.route('/')
def index():
#Loads the temlate page for the first time    
    return render_template('landing.html')





@app.route('/scrape')
def scraping():
#drop the last database
    db.posts.drop()

#call the scrape function in the last file
    package = scrape()

#put the data from that section into a mongo database  
    posts.insert_one({'_id':0,'title':package[0]})
    posts.insert_one({'_id':1,'paragraph':package[1]})
    posts.insert_one({'_id':2,'image':package[2]})
    posts.insert_one({'_id':3,'weather':package[3]})
    posts.insert_one({'_id':4,'facts':package[4]})
    posts.insert_one({'_id':5,'hemispheres':package[5]})

#go to the next page with all the content
    return redirect(url_for('complete'))



@app.route('/complete')
def complete():
#pull the information out of the data base
    title = posts.find_one({'_id':0})
    para = posts.find_one({'_id':1})
    feature = posts.find_one({'_id':2})
    weather = posts.find_one({'_id':3})
    facts = posts.find_one({'_id':4})
    hemispheres = posts.find_one({'_id':5})
    facts = "fix html page"
#feed the information to the index template
    return render_template('index.html',title=title['title'],para=para['paragraph'],feature=feature['image'],weather=weather['weather'],facts=facts,Astropedia=hemispheres['hemispheres'][0]['titles'],Astropedia_img=hemispheres['hemispheres'][0]['images'],Cerberus=hemispheres['hemispheres'][1]['titles'],Cerberus_img=hemispheres['hemispheres'][1]['images'],Schiaparelli=hemispheres['hemispheres'][2]['titles'],Schiaparelli_img=hemispheres['hemispheres'][2]['images'],Valles=hemispheres['hemispheres'][3]['titles'],Valles_img=hemispheres['hemispheres'][3]['images'])




if __name__ == '__main__':
   app.run(debug = True)