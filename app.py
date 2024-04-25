"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Milagros@localhost/pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)