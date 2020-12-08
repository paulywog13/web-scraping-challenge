from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_facts
import mars_news
import mars_space_images
import mars_hemispheres

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data=mongo.db.mars_facts_html.find_one()
    print(mars_data)
    
    # Return template and data
    return render_template("index.html", mars_mission=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to variables
     
    mars_mission = mongo.db.mars_facts_html
    mars_new_news = mars_news.scrape_info()
    mars_info = mars_facts.scrape_info()
    mars_hemis = mars_hemispheres.scrape_info()
    mars_img = mars_space_images.scrape_info()
    data = {
        "news_title": mars_new_news["latest_title"],
        "news_teaser": mars_new_news["latest_teaser"],
        "mars_facts": mars_info,
        "featured_image": mars_img["featured_image"],
        "mars_hemispheres": mars_hemis
    }
    mars_mission.update({}, data, upsert=True)
    
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
