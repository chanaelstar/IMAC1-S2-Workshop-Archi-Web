from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random 
import mysql.connector
myapp = Flask(__name__)

mydB = mysql.connector.connect (
    host="localhost",
    user="root",
    #password="",
    #database="test"
)

@myapp.route("/")
def formulaire():
    return render_template('accueil.html')