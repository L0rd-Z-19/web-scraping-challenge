from flask import Flask, render_template, redirect, url_for
import pymongo
from scrape_mars import scrape

app = Flask(__name__)
#configure mongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
mars_db = db.mars_db.find()


@app.route('/scrape')
def index():
    package = scrape()
    mars_data = [{'_id': 0,'news':[package[0],package[1]]}, {'_id': 1,'image': package[2]}, {'_id': 2,'weather': package[3]}, {'_id': 3,'facts': package[4]}, {'_id': 4,'hemis': package[5]}]
    db.mars_db.insert_many(mars_data)

    return redirect('/')

@app.route('/')
def result():
    
    title ='insert title'# mars_db.find_one({'_id': 0})
    para ='insert teaser'# mars_db.find_one({'_id': 0})
    featured = db.mars_db.find_one({'_id': 1})
    weather = db.mars_db.find_one({'_id': 2})
    #fix the html
    facts = 'insert html'#mars_db.find_one({'_id': 3})
    hemi = db.mars_db.find_one({'_id': 4})

    return render_template('index.html')#,title=title,para=para,featured=featured['image'],weather=weather['weather'],facts=facts['facts'])#,Cerberus=hemi['hemis'][0]['Cerberus Hemisphere Enhanced'],Cerberus_img=hemi[0][1])

if __name__ == '__main__':
   app.run(debug = True)