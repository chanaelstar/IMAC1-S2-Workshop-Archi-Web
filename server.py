from flask import Flask, render_template, request, jsonify
import random 
myapp = Flask("--name--")

@myapp.route("/")
def formulaire():
    return render_template('accueil.html')