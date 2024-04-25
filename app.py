"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Milagros@localhost/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

with app.app_context():
   connect_db(app)


@app.route('/')
def show_home_page():
   cupcakes = Cupcake.query.all()
   return render_template("base.html", cupcakes = cupcakes)

from flask import jsonify  

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "image": cupcake.image,
        "rating": cupcake.rating, 
        "size": cupcake.size
    }

@app.route("/api/cupcakes") 
def list_all_cupcakes():
    """Return JSON {cupcakes:[{id, flavor, size, rating, image}, ...]}"""
    cupcakes = Cupcake.query.all()
    serialized_cupcakes = [serialize_cupcake(cupcake) for cupcake in cupcakes]

    return jsonify(cupcakes=serialized_cupcakes)  


@app.route("/api/cupcakes/<cupcake_id>") 
def list_single_cupcake(cupcake_id):
    """Return JSON {cupcakes:[{id, flavor, size, rating, image}, ...]}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized_cupcake)



@app.route("/api/cupcakes", methods=["POST"]) 
def create_cupcake():
    """Return JSON {cupcakes:[{id, flavor, size, rating, image}, ...]}"""
    flavor = request.json['flavor']
    size = request.json['size']
    image = request.json['image']
    rating = request.json['rating']

    new_cupcake = Cupcake(flavor = flavor, size = size, image = image, rating = rating)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized_cupcake = serialize_cupcake(new_cupcake)

    return (jsonify(cupcake = serialized_cupcake), 201)


@app.route("/api/cupcakes/<cupcake_id>", methods=["PATCH"]) 
def update_cupcake(cupcake_id):
    """Return JSON {cupcakes:[{id, flavor, size, rating, image}, ...]}"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized_cupcake = serialize_cupcake(cupcake)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.image = request.json['image']
    cupcake.rating = request.json['rating']

    db.session.commit()

    serialized_cupcake = serialize_cupcake(cupcake)

    return jsonify(cupcake = serialized_cupcake)

@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"]) 
def delete_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    message = {"message":"Deleted"}

    return jsonify(message)