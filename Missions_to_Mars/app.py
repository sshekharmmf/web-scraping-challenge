# import necessary libraries
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#  create route that renders index.html template
@app.route("/")
def index():
    mars_dat = mongo.db.mars_dat.find_one()
    return render_template("index.html", mars_dat=mars_dat)


@app.route("/scrape")
def scrape():
    mars_dat = mongo.db.mars_dat
    mars_d = scrape_mars.scrape()
    mars_dat.update(
        {},
        mars_d,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)