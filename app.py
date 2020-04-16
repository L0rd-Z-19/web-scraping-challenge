from flask import Flask, render_template, request
import pymongo
from scrape_mars import scrape

app = Flask(__name__)
#configure mongo
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
mars_collection = db.mars_collection.find()


@app.route('/scrape')
def index():
    mars_title,mars_para,featured_image_url,mars_weather,mars_fact,mars_hemispheres = scrape()
    mars_dict = {'news':[mars_title,mars_para], 'image': featured_image_url, 'weather': mars_weather, 'facts': mars_fact, 'hemis': mars_hemispheres}
    db.mars_db.insert_one(mars_dict)

    return render_template('index.html')

@app.route('/')
def result():
    title = mars_collection.find_one({"news": mars_title})
    para = mars_collection.find_one({"news": mars_para})
    featured = mars_collection.find_one({"image": featured_image_url})
    weather = mars_collection.find_one({"weather": mars_weather})
    #fix the html
    #facts = mars_collection.find_one({"facts": mars_fact})
    hemi = mars_collection.find_one({"hemis": mars_hemispheres})
    
    return render_template('index.html',title=title)

if __name__ == '__main__':
   app.run(debug = True)