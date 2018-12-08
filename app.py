#Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars



app = Flask(__name__)

# setup mongo connection
#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars_db"
mongo = PyMongo(app)


# connect to mongo db and collection
#db = client.scrape_mars_db

#everything works except the database connection

# Drops collection if available to remove duplicates
#db.mars_info.drop()

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    data_mars = mongo.db.scrape_mars_collection.find_one()

    # Return template and data
    return render_template("index.html", mars= data_mars)




# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_collection = mongo.db.scrape_mars_collection
    scraped_mars = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_collection.update({}, scraped_mars, upsert=True)

    # Redirect back to home page
    return redirect("/")






if __name__ == "__main__":
    app.run(debug=True)

