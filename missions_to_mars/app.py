from flask import Flask, render_template, jsonify, redirect
import psycopg2
from flask_pymongo import PyMongo
import scrape_mars
import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd


app = Flask(__name__)


# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

mars_data = mongo.db.mars_data
mars_data.drop()


@app.route("/")
def index():
    
    mars_results = mars_data.find()
    return render_template("index.html", mars_results=mars_results)
    

@app.route("/scrape")
def scraper():
    
    data = scrape_mars.scrape()
    mongo.db.mars_data.insert(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
