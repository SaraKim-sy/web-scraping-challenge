# Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Reoute to render index.html template using data from Mongo
@app.route("/")
def home():
 
    mars_data = mongo.db.scraped_mars_data.find_one()
    print(mars_data)
    # Return template and data
    return render_template('index.html', mars_data=mars_data)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.scraped_mars_data.update({}, mars_data, upsert=True)

    # Redirect back to homepage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)